# DailyBriefBot - Project Core

## Overview

DailyBriefBot is a **Discord bot** that reads busy channels and posts CPU-friendly extractive summaries to a briefing channel on configurable schedules. No AI APIs, no cloud costs, runs on cheap CPUs (~55 MB footprint).

## Architecture

```
Scheduler → Collector → Preprocessor → Engine (3 tiers) → Formatter → Discord Embed
```

### Components

| Module | Purpose | File |
|--------|---------|------|
| `bot.py` | discord.py setup, privileged intents | src/dailybriefbot/bot.py |
| `collector.py` | Fetches channel history with pagination | src/dailybriefbot/collector.py |
| `preprocessor.py` | Cleans mentions, emoji, code blocks | src/dailybriefbot/preprocessor.py |
| `engine.py` | Pluggable summarization strategies | src/dailybriefbot/engine.py |
| `heuristics.py` | Tier 3 scoring (reactions, replies) | src/dailybriefbot/heuristics.py |
| `topics.py` | Tier 2 spaCy NER/noun chunks | src/dailybriefbot/topics.py |
| `publisher.py` | Formats and posts Discord Embeds | src/dailybriefbot/publisher.py |
| `scheduler.py` | APScheduler integration (cron/interval) | src/dailybriefbot/scheduler.py |
| `config.py` | Config loading/validation | src/dailybriefbot/config.py |

### Summarization Pipeline

**Tier 1:** Extractive summary via sumy/LexRank (default)  
**Tier 2:** spaCy NER/noun chunks for topic detection (optional)  
**Tier 3:** Heuristic scoring by reactions, replies, message length  

All tiers run on every job; results merge into a single Discord Embed.

## Configuration

Single `config.yaml` drives all behavior: channels, schedules, summarization strategy, heuristics weights, NLP settings. No commands — purely config-driven automation.

## Invariants

- **No storage:** Stateless processing (fetch → process → discard)
- **Single server only:** One Discord server per bot instance
- **Message Content intent required:** Must enable in Discord Developer Portal
- **No slash commands:** All operations auto-triggered via config
