# Tech Stack — DailyBriefBot

## Languages & Frameworks

| Layer | Technology | Version | Notes |
|-------|-----------|---------|-------|
| Language | Python 3.10+ | - | Type hints used throughout |
| Discord SDK | discord.py | ≥2.3 | Asynchronous, handles rate limits |
| Scheduler | APScheduler | ≥3.10 | AsyncIOScheduler for cron/interval triggers |
| NLP Extractive Summary | sumy | ≥0.11 | LexRank/TextRank/Luhn/LSA/KL-Sum algorithms |
| NLP Pipeline (optional) | spaCy | ≥3.7 | en_core_web_sm model (~12 MB) |
| Config Parser | PyYAML | ≥6.0 | Single config.yaml file |
| Text Processing | NLTK | ≥3.8 | Sentence tokenization for sumy |

## Build & Packaging

- **Package manager:** Poetry or pip (pyproject.toml / requirements.txt)
- **Entry point:** src/dailybriefbot/__main__.py
- **Distribution:** Wheel package, deployable via Docker

## Deployment Targets

| Target | Rationale |
|--------|-----------|
| Raspberry Pi 4 / 5 | Runs at ~200 MB RAM idle |
| $5/month VPS (DigitalOcean/Linode) | Meets CPU-only requirement |
| Docker container | Simplified deployment with all deps baked in |

## Size Footprint

- Installed packages: ~55 MB total
- spaCy model: +12 MB
- Runs comfortably on 512+ MB RAM systems
