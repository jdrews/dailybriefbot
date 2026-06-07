# Commands — DailyBriefBot

## Development & Deployment

```bash
# Install dependencies ( Poetry or pip)
pip install -e .
# or
poetry install

# Run bot locally (reads config.yaml from cwd)
python -m dailybriefbot

# Start Docker container
docker-compose up -d

# View logs
docker-compose logs -f dailybriefbot

# Build Docker image
docker build -t dailybriefbot:latest .
```

## Configuration

```bash
# Validate config.yaml syntax (PyYAML)
python -c "import yaml; yaml.safe_load(open('config.yaml'))"

# Dry-run scheduler jobs (check cron expressions)
echo "0 8 * * *" | cron.d Validate format: crontab -e

# Test sumy summarization locally
python -c "from sumy.parsers.plaintext import PlaintextParser; from sumy.nlp.tokenizers import Tokenizer; from sumy.summarizers.lex_rank import LexRankSummarizer; p = PlaintextParser.from_string('test sentence here', Tokenizer('english')); s = LexRankSummarizer(); print(list(s.p.document))"

# Check spaCy model (if enabled)
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); doc = nlp('hello world'); print([ent.text for ent in doc.ents])"
```

## Discord Setup

```bash
# Enable privileged intents in Discord Developer Portal:
# Bot → Privileged Gateway Intents → [x] Message Content Intent
```

## Git Workflow

```bash
git pull origin main
pip install -e .  # Reinstall after code changes
python -m dailybriefbot
```
