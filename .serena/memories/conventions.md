# Conventions — DailyBriefBot

## Code Style

- **Indentation:** 4 spaces (no tabs)
- **Line length:** ≤100 chars (PEP 8 compliant)
- **Imports:** Standard library → third-party → local modules; grouped alphabetically within groups
- **Type hints:** Full type annotations on all function signatures; `list[int]`, not `List[int]`
- **String quotes:** Single quotes for f-strings, double quotes for docstrings
- **Comments:** One-line comments end with period only if sentence. Docstrings use Google style.

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Modules/packages | lowercase_with_underscores | `config.py`, `src/dailybriefbot/collector.py` |
| Classes | PascalCase | `Collector`, `SummaryStrategy` |
| Functions/methods | snake_case | `collect_messages()`, `summarize_text()` |
| Variables | snake_case | `source_channel_id`, `window_hours` |
| Constants | UPPER_SNAKE_CASE | `MIN_MESSAGES`, `DEFAULT_STRATEGY` |
| Discord objects | PascalCase (discord.py convention) | `Message`, `Channel` |

## Design Patterns

- **Strategy pattern:** Summarization engines pluggable via `SummaryStrategy` protocol/interface
- **Singleton:** Bot instance, Scheduler instance
- **Protocol/ABC:** For strategy implementations and future extensibility

## Documentation

| Location | Purpose | Style |
|----------|---------|-------|
| docstrings | Function/class signatures | Google style |
| architecture.md | System design, data flow, Mermaid diagrams | Markdown + code blocks |
| config.yaml comments | Inline config explanations | YAML block comments |

## Error Handling

- Discord API errors: let discord.py handle 429s automatically; add delays between bulk fetches
- Summarization failures: catch exception → log error → skip job → continue other channels
- Config validation errors: fail fast on startup with clear error message to stderr

## Logging

```python
import logging
logger = logging.getLogger(__name__)

# Standard levels
logger.debug("DEBUG: detailed info")
logger.info("INFO: general workflow")
logger.warning("WARNING: unexpected but recoverable")
logger.error("ERROR: failed operation", exc_info=True)  # Include traceback on errors
```

## File Organization

```
src/dailybriefbot/
├── __init__.py           # Package metadata, version
├── __main__.py           # Entry point (config load → start bot)
├── config.py             # Config schema + validation
├── bot.py                # Discord client setup, event handlers
├── collector.py          # Message fetching
├── preprocessor.py       # Text cleaning pipeline
├── engine.py             # Summarization strategy dispatch
├── heuristics.py         # Tier 3 scoring logic
├── topics.py             # Tier 2 spaCy extraction
├── publisher.py          # Embed builder + Discord send
└── scheduler.py          # APScheduler job registration
```
