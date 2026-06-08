"""Lightweight job history tracking using JSON file."""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


class JobHistory:
    """Track bot execution history in a small JSON file (<1KB)."""
    
    def __init__(self, data_dir: str = "./logs"):
        self.data_path = Path(data_dir) / "job_history.json"
        self._ensure_file()
    
    def _ensure_file(self):
        """Initialize empty history file if it doesn't exist."""
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_path.exists():
            with open(self.data_path, 'w') as f:
                json.dump([], f)
    
    def _load(self) -> list[dict]:
        with open(self.data_path, 'r') as f:
            return json.load(f)
    
    def _save(self, history: list[dict]) -> None:
        with open(self.data_path, 'w') as f:
            json.dump(history, f, indent=2)
    
    def get_last_successful(self, channel_id: int = 0) -> dict | None:
        """Get last successful job entry."""
        history = self._load()
        relevant = [h for h in reversed(history) 
                   if h.get('success', False) and (channel_id == 0 or h.get('channel_id') == channel_id)]
        return relevant[0] if relevant else None
    
    def record(self, channel_id: int, success: bool, **kwargs) -> None:
        """Record a job execution."""
        history = self._load()
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "channel_id": channel_id,
            "success": success,
            "messages_processed": kwargs.get("messages_processed", 0),
            "sentences_generated": kwargs.get("sentences_generated", 0),
            "duration_ms": kwargs.get("duration_ms", 0),
            "error_message": kwargs.get("error_message") if not success else None
        }
        history.append(entry)
        
        # Keep only last 100 entries (~1KB limit)
        if len(history) > 100:
            history = history[-100:]
        
        self._save(history)
