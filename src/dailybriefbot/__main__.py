"""Entry point: load config and start bot."""

import asyncio
from dailybriefbot.bot import DailyBriefBot
from dailybriefbot.config import load_config_and_validate


async def main():
    """Main entry point for the bot."""
    try:
        config = load_config_and_validate()
        
        bot = DailyBriefBot(config.discord_token, config)
        await bot.start(config.discord_token)
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
