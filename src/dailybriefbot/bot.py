"""Discord bot setup with message_content intent."""

import asyncio
from datetime import datetime, timedelta, timezone
from typing import Optional

import discord
from discord.ext import tasks
from .collector import MessageCollector
from .preprocessor import Preprocessor
from .engine import Engine
from .publisher import Publisher
from .job_history import JobHistory
from .scheduler import Scheduler

class DailyBriefBot(discord.Client):
    """Main bot class handling summary scheduling and execution."""
    
    def __init__(self, token: str, config):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        
        self.token = token
        self.config = config
        self.job_history = None
        
        # Initialize components
        self.collector = MessageCollector(config.api_call_budget)
        self.preprocessor = Preprocessor()
        self.engine = Engine(
            strategy_name=config.summarization.strategy,
            sentences_per_n_msgs=config.summarization.sentences_per_n_messages,
            min_sentences=config.summarization.min_sentences,
            max_sentences=config.summarization.max_sentences
        )
        self.publisher = Publisher(max_chars=6000)
    
    async def on_ready(self):
        """Bot startup - load job history and start scheduler."""
        print(f"✅ Logged in as {self.user}")
        
        self.job_history = JobHistory()
        self.scheduler = Scheduler(self, self.config)
        await self.scheduler.start()
    
    async def run_summary_job(self, channel_config):
        """Execute a single summary job for a channel configuration."""
        since = datetime.now(timezone.utc) - timedelta(hours=channel_config.window_hours)
        
        try:
            # Collect messages
            messages = await self.collector.collect(
                channel_id=channel_config.source,
                since=since,
                bot=self
            )
            
            if not messages or len(messages) < self.config.summarization.min_messages:
                return
            
            # Process through pipeline
            text, metadata = self.preprocessor.process(messages)
            summaries = self.engine.summarize(text, len(messages))
            
            # Format and send
            embed_data = self.publisher.format(
                summary_text=summaries[0][1] if summaries else "",
                channel_name=channel_config.source,  # Would fetch proper name from API
                window_hours=channel_config.window_hours,
                metadata=metadata
            )
            
            await self.send_embed(channel_config.target, embed_data)
            
        except Exception as e:
            print(f"❌ Summary job failed for channel {channel_config.source}: {e}")
            raise
    
    async def send_embed(self, channel_id: int, embed_data: dict):
        """Send formatted embed to target channel."""
        try:
            channel = self.get_channel(channel_id)
            if not channel or not isinstance(channel, discord.TextChannel):
                return
            
            msg = await channel.send(embed=discord.Embed(**embed_data))
            
            # Record success
            if self.job_history:
                self.job_history.record(
                    channel_id=channel_id,
                    success=True,
                    messages_processed=len(msg.content.split(".")),  # Count sentences as proxy for message coverage
                    sentences_generated=len(msg.content),
                    duration_ms=0
                )
        except Exception as e:
            print(f"Failed to send embed to {channel_id}: {e}")
