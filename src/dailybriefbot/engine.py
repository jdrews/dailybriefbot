"""Pluggable summarization engine with Tier 1 (LexRank) active, Tiers 2/3 stubbed."""

from abc import ABC, abstractmethod
from typing import Optional


class SummaryStrategy(ABC):
    """Abstract base for summary strategies."""
    
    @abstractmethod
    def summarize(self, text: str, num_sentences: int) -> str:
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass


class LexRankStrategy(SummaryStrategy):
    """Tier 1: Extractive summary using sumy/LexRank."""
    
    def __init__(self, sentences_per_n_msgs: int = 20, 
                 min_sentences: int = 3, max_sentences: int = 15):
        self.sentences_per_n_msgs = sentences_per_n_msgs
        self.min_sentences = min_sentences
        self.max_sentences = max_sentences
    
    def summarize(self, text: str, num_sentences: Optional[int] = None) -> str:
        from sumy.parsers.plaintext import PlaintextParser
        from sumy.nlp.tokenizers import Tokenizer
        from sumy.summarizers.lex_rank import LexRankSummarizer
        
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        sentences = list(summarizer(parser.document, self._calc_num(num_sentences or 10)))
        
        return " ".join(str(s) for s in sentences[:self.max_sentences])
    
    @property
    def name(self) -> str:
        return "lexrank"
    
    def _calc_num(self, n_messages: int = 10) -> int:
        ratio = self.sentences_per_n_msgs / max(n_messages, 1)
        num = int(ratio * n_messages)
        return max(self.min_sentences, min(num or self.min_sentences, self.max_sentences))


class Tier2Stub(SummaryStrategy):
    """Tier 2 stub - spaCy topics (not implemented in Phase 1)."""
    
    def summarize(self, text: str, num_sentences: int) -> str:
        return ""
    
    @property
    def name(self) -> str:
        return "tier2_stub"


class Tier3Stub(SummaryStrategy):
    """Tier 3 stub - heuristic scoring (not implemented in Phase 1)."""
    
    def summarize(self, text: str, num_sentences: int) -> str:
        return ""
    
    @property
    def name(self) -> str:
        return "tier3_stub"


class Engine:
    """Orchestrates summarization strategies."""
    
    def __init__(self, strategy_name: str = "lexrank", 
                 sentences_per_n_msgs: int = 20,
                 min_sentences: int = 3, max_sentences: int = 15):
        if strategy_name == "lexrank":
            self.strategies = [LexRankStrategy(sentences_per_n_msgs, min_sentences, max_sentences)]
        elif strategy_name in ("textrank", "luhn"):
            # Excluded for MVP; Placeholder - would implement similarly
            raise ValueError(f"{strategy_name} not implemented in Phase 1")
        else:
            self.strategies = [LexRankStrategy(sentences_per_n_msgs, min_sentences, max_sentences)]
    
    def summarize(self, text: str, num_messages: int) -> list[tuple[str, str]]:
        """Run all active strategies and return (strategy_name, sentences_str) tuples."""
        results = []
        for strat in self.strategies:
            sentences = strat.summarize(text, strat._calc_num(num_messages))
            if sentences:
                results.append((strat.name, sentences))
        return results
