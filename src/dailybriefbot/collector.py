"""Fetch messages from Discord channels with pagination and rate limit handling."""

from datetime import datetime, timedelta
from typing import Optional


class MessageCollector:
    """Collect messages respecting API call budget and rate limits."""
    
    def __init__(self, api_budget: int = 100):
        self.api_budget = api_budget
    
    async def collect(self, channel_id: int, since: datetime, bot) -> list[dict]:
        """Fetch messages from a channel within time window."""
        if not hasattr(bot, 'get_channel'):
            return []
        
        channel = bot.get_channel(channel_id)
        if not channel:
            return []
        
        messages = []
        call_count = 0
        
        async for msg in channel.history(after=since, limit=None):
            if call_count >= self.api_budget:
                break
            
            # Skip bot and system messages
            if msg.author.bot or msg.type.name == "SYSTEM":
                continue
            
            if not msg.content.strip():
                continue
            
            msg_data = {
                "id": str(msg.id),
                "content": msg.content,
                "author": {"id": str(msg.author.id)},
                "created_at": msg.created_at.isoformat(),
                "reactions": [],  # Excluded for MVP; Could fetch separately if needed
                "reply_count": 0,   # Excluded for MVP; Would require additional API calls
            }
            
            messages.append(msg_data)
            call_count += 1
        
        messages.reverse()  # Newest first for signal scoring
        return messages
