"""Clean and normalize Discord messages for summarization."""

import re
from typing import Optional


class Preprocessor:
    """Preprocess raw Discord messages into clean text."""
    
    def __init__(self):
        self.mention_pattern = re.compile(r'<@!?(\d+)>')
        self.emoji_pattern = re.compile(r'<:(\w+):\d+>')
        self.url_pattern = re.compile(r'https?://\S+', re.IGNORECASE)
    
    def process(self, messages: list[dict]) -> tuple[str, dict]:
        """Process message list into cleaned text and metadata."""
        texts = []
        metadata = {"total_messages": len(messages), "unique_authors": set()}
        
        for msg in messages:
            if not msg.get('content', '').strip():
                continue
            
            content = self._clean_message(msg['content'], msg)
            text = f"\n\n{content}" if texts else content
            texts.append(text)
            
            author_id = str(msg.get('author', {}).get('id', ''))
            if author_id:
                metadata["unique_authors"].add(author_id)
        
        return "".join(texts), metadata
    
    def _clean_message(self, content: str, msg: dict) -> str:
        """Clean a single message."""
        # Strip mentions but keep usernames
        content = self.mention_pattern.sub(r'@\g<1>', content)
        
        # Remove custom emoji
        content = self.emoji_pattern.sub('', content)
        
        # Preserve URLs but normalize whitespace around them  
        content = re.sub(self.url_pattern, r'\g<0>', content)
        
        return content.strip()
