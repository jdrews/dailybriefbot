# Task Completion — DailyBriefBot

## After Any Coding Task

Run the following to ensure code quality:

```bash
# Type checking (mypy)
mypy src/dailybriefbot --strict

# Formatting check (black)
black --check src/

# Linting (flake8 or ruff)
ruff check src/  # or flake8 src/

# Run tests if present
pytest
```

## Pre-Commit Checklist

- [ ] Code passes `mypy --strict`
- [ ] Code formatted by black (`black src/`)
- [ ] No linting errors (`ruff check src/`)
- [ ] Tests pass (if applicable)
- [ ] Config.yaml is valid YAML and type-checked
- [ ] No secrets committed (.env files in .gitignore)

## Post-Merge Verification

```bash
# Pull latest and test locally
git pull origin main
pip install -e .
python -m dailybriefbot  # Verify bot starts without errors

# Check scheduled jobs registered correctly
from src.dailybriefbot.scheduler import scheduler
print(scheduler.get_job_id('test_job'))  # Should not raise
```

## Release Checklist

- [ ] Update version in `src/dailybriefbot/__init__.py`
- [ ] Tag release: `git tag v1.0.0 && git push --tags`
- [ ] Build wheel: `python -m build`
- [ ] Test Docker image: `docker run dailybriefbot:latest python -c "import discord; print(discord.__version__)"`
