"""Fake collector that reads messages from JSON file."""

import json


class FakeMessageCollector:
    """Reads messages from file, mimicking Discord collector output.
    
    This class provides the same interface as MessageCollector but loads
    data from a local JSON file instead of fetching from Discord API.
    Used for testing without Discord integration.
    """
    
    def __init__(self, api_budget: int = 100):
        self.api_budget = api_budget
    
    def collect_from_file(self, filepath: str) -> list[dict]:
        """Load messages from JSON file. Returns newest-first order like real collector.
        
        Args:
            filepath: Path to JSON file containing message data
            
        Returns:
            List of normalized message dictionaries matching Discord API structure
            
        Raises:
            ValueError: If input format is invalid or required fields missing
            FileNotFoundError: If file doesn't exist
        """
        messages = []
        
        with open(filepath, 'r') as f:
            raw_data = json.load(f)
            
        # Validate input structure - fail on bad input
        if not isinstance(raw_data, list):
            raise ValueError("Input must be a JSON array of messages")
        
        for idx, msg in enumerate(raw_data):
            self._validate_message(idx, msg)
            
            # Normalize to match collector.py output format
            normalized = {
                "id": str(msg.get('id', f'unknown_{idx}')),
                "content": msg.get('content', ''),
                "author": {"id": str(msg.get('author', {}).get('id', ''))},
                "created_at": msg.get('created_at'),  # Optional, preserved if present
                "reactions": [],  # Excluded for MVP
                "reply_count": 0,   # Excluded for MVP
            }
            
            messages.append(normalized)
        
        return messages
    
    def _validate_message(self, idx: int, msg: dict):
        """Ensure required fields exist; fail on bad input."""
        if not isinstance(msg, dict):
            raise ValueError(f"Message {idx} must be an object")
        
        if 'content' not in msg or not msg['content']:
            raise ValueError(f"Message {idx} requires non-empty content field")
