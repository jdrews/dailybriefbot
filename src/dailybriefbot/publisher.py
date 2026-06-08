"""Format summaries as Discord Embeds with truncation support."""

from datetime import datetime, timezone


class Publisher:
    """Create and send Discord Embed messages."""
    
    def __init__(self, max_chars: int = 6000):
        self.max_chars = max_chars
    
    def format(self, summary_text: str, channel_name: str, 
               window_hours: int, metadata: dict) -> dict:
        """Create embed data structure."""
        timestamp = datetime.now(timezone.utc).strftime("%B %d, %Y • Last %d hour" + 
                          ("s" if window_hours != 1 else ""))
        
        summary = self._truncate_summary(summary_text)
        
        return {
            "title": f"📋 Daily Brief — #{channel_name}",
            "description": f"{timestamp}\n\n",
            "fields": [
                {"name": "📝 Summary", "value": summary, "inline": False}
            ],
            "footer": {
                "text": f"Summarizing {metadata.get('total_messages', 0)} messages → " + 
                         str(len(summary.split())) + " words\nBot • Now"
            }
        }
    
    def _truncate_summary(self, text: str) -> str:
        """Truncate summary to fit embed while preserving sentence structure."""
        if not text or len(text.strip()) == 0:
            return "No summary available."
        
        if len(text) <= self.max_chars - 200:
            return text
        
        # Remove last complete sentences until under limit
        sentences = [s for s in text.split(". ") if s.strip()]
        result = []
        current_len = 0
        
        for sent in reversed(sentences):
            test_len = current_len + len(sent) + 2
            if test_len < self.max_chars - 150:
                result.insert(0, sent)
                current_len = test_len
            elif not result and current_len + len(sent) <= self.max_chars - 100:
                result.insert(0, sent)
        
        return ". ".join(result) if result else text[:self.max_chars - 200]
