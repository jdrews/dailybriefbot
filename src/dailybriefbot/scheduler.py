"""APScheduler integration with global schedule and job history tracking."""

from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .job_history import JobHistory


class Scheduler:
    """Manage scheduled summary jobs using APScheduler."""
    
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
    
    async def start(self):
        """Initialize scheduler and register all channel jobs."""
        # Initialize job history on startup
        self.job_history = JobHistory()
        
        # Initialize global schedule (e.g., daily at 8 AM)
        self.scheduler = AsyncIOScheduler()
        
        for ch in self.config.channels:
            await self._add_job(ch)
        
        self.scheduler.start()
    
    async def _add_job(self, channel_config):
        """Add a summary job for a specific channel configuration."""
        last_run = self.job_history.get_last_successful(channel_config.source)
        
        if last_run:
            since = datetime.fromisoformat(last_run['timestamp'].replace('Z', '+00:00')) \
                     + timedelta(minutes=30)
        else:
            since = datetime.now(timezone.utc) - timedelta(hours=channel_config.window_hours)
        
        self.scheduler.add_job(
            self.bot.run_summary_job,
            'date',
            run_date=datetime.now(timezone.utc),
            args=[channel_config],
            kwargs={'since': since},
            id=f"summary_{channel_config.source}",
            executor='default'
        )
