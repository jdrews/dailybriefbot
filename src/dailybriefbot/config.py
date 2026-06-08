"""Configuration loading and validation for DailyBriefBot."""

import os
from dataclasses import dataclass, field
from typing import Optional
import yaml


@dataclass
class SummarizationConfig:
    strategy: str = "lexrank"
    min_messages: int = 5
    sentences_per_n_messages: int = 20
    min_sentences: int = 3
    max_sentences: int = 15
    
    reaction_weight: float = 3.0
    reply_depth_weight: float = 2.0
    length_weight: float = 1.0
    url_bonus: float = 1.5
    
    message_links_enabled: bool = False
    signal_threshold: float = 4.0
    max_links_per_summary: int = 5
    
    priority_users: dict = field(default_factory=dict)


@dataclass
class NLPConfig:
    spacy_model: str = "en_core_web_sm"
    max_topics: int = 5
    enable_ner: bool = True


@dataclass
class LoggingConfig:
    level: str = "INFO"


@dataclass
class ChannelConfig:
    source: int
    target: int
    schedule: str
    window_hours: int = 24


@dataclass
class Config:
    discord_token: str
    channels: list[ChannelConfig] = field(default_factory=list)
    api_call_budget: int = 100
    summarization: SummarizationConfig = field(default_factory=SummarizationConfig)
    nlp: NLPConfig = field(default_factory=NLPConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)


def load_config(path: str = "config.yaml") -> Config:
    """Load and validate configuration from YAML file."""
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    
    config_dict = {k: v for k, v in data.items() if k != 'channels'}
    channel_list = [ChannelConfig(**c) for c in data.get('channels', [])]
    
    return Config(
        discord_token=config_dict.get('discord', {}).get('token', ''),
        channels=channel_list,
        api_call_budget=config_dict.get('api_call_budget', 100),
        summarization=SummarizationConfig(**config_dict.get('summarization', {})),
        nlp=NLPConfig(**config_dict.get('nlp', {})),
        logging=LoggingConfig(**config_dict.get('logging', {}))
    )


def validate_config(config: Config) -> None:
    """Validate configuration values. Raises ValueError on invalid config."""
    discord_token = getattr(config, 'discord_token', '')
    if not discord_token or len(discord_token.strip()) < 10:
        raise ValueError("Invalid Discord token")
    
    if not config.channels:
        raise ValueError("No channels configured")
    
    for ch in config.channels:
        source = getattr(ch, 'source', 0)
        target = getattr(ch, 'target', 0)
        
        if not isinstance(source, int) or source <= 0:
            raise ValueError(f"Invalid source channel ID: {source}")
        if not isinstance(target, int) or target <= 0:
            raise ValueError(f"Invalid target channel ID: {target}")
        
        import croniter
        try:
            croniter.croniter(getattr(ch, 'schedule', ''))
        except Exception as e:
            raise ValueError(f"Invalid cron schedule '{getattr(ch, 'schedule', '')}': {e}")
    
    strat = getattr(config.summarization, 'strategy', 'lexrank')
    if strat not in ("lexrank", "textrank", "luhn", "heuristic"):
        raise ValueError(f"Unknown strategy: {strat}")
    
    priority_users = getattr(config.summarization, 'priority_users', {})
    for uid, mult in priority_users.items():
        if not isinstance(uid, str) or len(uid) != 18:
            raise ValueError(f"Invalid user ID: {uid}")
        try:
            float_mult = float(mult)
            if float_mult <= 0 or float_mult > 10:
                raise ValueError(f"Invalid multiplier for user {uid}: {mult}")
        except (ValueError, TypeError):
            raise ValueError(f"Invalid multiplier for user {uid}: {mult}")


def load_config_and_validate(path: str = "config.yaml") -> Config:
    """Load and validate configuration in one step."""
    config = load_config(path)
    validate_config(config)
    return config
