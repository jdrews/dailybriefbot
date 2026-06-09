"""Test harness CLI entry point."""

import argparse
import json
import sys
from pathlib import Path

# Import from dailybriefbot package
from dailybriefbot.fake_collector import FakeMessageCollector
from dailybriefbot.preprocessor import Preprocessor
from dailybriefbot.engine import Engine
from dailybriefbot.publisher import Publisher


def create_engine():
    """Create summarization engine with hardcoded test defaults."""
    return Engine(
        strategy_name="lexrank",
        sentences_per_n_msgs=20,
        min_sentences=3,
        max_sentences=15
    )


def main():
    parser = argparse.ArgumentParser(
        description='Test harness for message summarization - outputs embed_data without Discord'
    )
    parser.add_argument('--input', required=True, help='Path to JSON file with messages')
    parser.add_argument('--channel-id', default='123456789', help='Source channel ID (default: 123456789)')
    parser.add_argument('--window-hours', type=int, default=24, help='Time window in hours (default: 24)')
    
    args = parser.parse_args()
    
    # Validate input file exists - fail on bad input
    if not Path(args.input).exists():
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Step 1: Load messages from file (fake collector)
        collector = FakeMessageCollector(api_budget=100)
        messages = collector.collect_from_file(args.input)
        
        if not messages:
            raise ValueError("No valid messages loaded from input file")
        
        # Step 2: Preprocess - same as production pipeline
        preprocessor = Preprocessor()
        text, metadata = preprocessor.process(messages)
        
        # Step 3: Summarize - same as production pipeline  
        engine = create_engine()
        summaries = engine.summarize(text, len(messages))
        
        if not summaries:
            raise ValueError("No summary generated")
        
        # Step 4: Format embed_data - same as production publisher
        publisher = Publisher(max_chars=6000)
        embed_data = publisher.format(
            summary_text=summaries[0][1],
            channel_name=args.channel_id,
            window_hours=args.window_hours,
            metadata=metadata
        )
        
        # Step 5: Output as JSON to stdout (no Discord integration)
        print(json.dumps(embed_data, indent=2))
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
