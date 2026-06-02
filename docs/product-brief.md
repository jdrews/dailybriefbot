# DailyBriefBot - Phase 1: Channel Briefs


## What

DailyBriefBot is a Discord bot that reads your busy channels and posts a short, readable summary into a briefing channel on a schedule you choose (e.g. nightly, weekly)

No AI APIs. No cloud costs. Runs on cheap CPUs (no costly GPUs for AI/LLMs needed). 

## Why

Active Discord servers generate hundreds of messages a day. Members who step away for a few hours, or a few days, come back to a wall of unread text and no easy way to catch up. Important decisions, shared links, and key discussions get buried.

DailyBriefBot solves this by distilling the noise into a brief you can read in 30 seconds. It's **free to run**, **privacy-respecting** (nothing is stored — messages are read, summarized, and discarded), and lightweight enough for a Raspberry Pi.

## How It Works

The bot pulls recent messages from your source channels, cleans them up, and runs three layers of analysis — all locally on CPU — before posting the result.

```mermaid
flowchart LR
    A["📨 Your Channels"] --> B["🧹 Clean & Prep"]
    B --> C["🧠 Analyze"]
    C --> D["📋 #daily-brief"]
```

**The three layers:**

| Layer | What it does | Produces |
|-------|-------------|----------|
| **Smart Extraction** | Identifies the most important sentences using proven ranking algorithms (LexRank/TextRank) | A concise written summary |
| **Topic Detection** | Pulls out key topics, names, and links using lightweight language analysis | A "Key Topics" list |
| **Highlight Scoring** | Surfaces messages that got the most reactions, replies, or community engagement | A "Highlights" section |

Every layer runs on every summary. Together they produce a single embed:

> **📋 Daily Brief — #general**
> *June 1, 2026 · Last 24 hours*
>
> **📝 Summary** — The team discussed the v2.0 migration plan and resolved two open bugs...
>
> **🏷️ Topics** — `v2.0 release` · `migration guide` · `Docker setup`
>
> **🔥 Highlights**
> - @alice shared the migration docs (8 👍)
> - @bob flagged a CLI bug that sparked 12 replies
>
> *142 messages from 23 members*
