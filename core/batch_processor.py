from typing import List, Optional
from datetime import datetime
from utilities.text_cleaner import TextCleaner
from core.tokeniser import Tokeniser
from core.vocabulary import VocabularyAnalyser
from core.pos_analyser import POSAnalyser
from core.ngram_analyser import NGramAnalyser
from core.style_interpretor import StyleInterpretor


class BatchProcessor:

    def __init__(self):
        self.cleaner = TextCleaner()
        self.tokeniser = Tokeniser()
        self.vocabulary = VocabularyAnalyser()
        self.pos = POSAnalyser()
        self.ngrams = NGramAnalyser()
        self.style = StyleInterpretor()

    def analyze_multiple(self, texts: List[str], names: Optional[List[str]] = None) -> List[dict]:

        if not names:
            names = [f"Text {i+1}" for i in range(len(texts))]

        results = []
        for i, (text, name) in enumerate(zip(texts, names)):
            fingerprint = self._analyze_single(text, name, i)
            results.append(fingerprint)

        return results

    def _analyze_single(self, text: str, name: str, text_id: int) -> dict:
        clean_text = self.cleaner.clean(text)
        self.tokeniser.reset()
        self.tokeniser.tokenise(clean_text)
        stats = self.tokeniser.get_statistics()
        words = self.tokeniser.get_words()
        vocab = self.vocabulary.analyse(words)
        self.pos.process(clean_text)
        pos = self.pos.analyse()

        bigrams = self.ngrams.get_bigrams(words, top_k=5)
        trigrams = self.ngrams.get_trigrams(words, top_k=5)

        style_features = {
            "word_count": stats["word_count"],
            "sentence_count": stats["sentence_count"],
            "avg_sentence_length": stats["avg_sentence_length"],
            "sentence_length_variance": stats["sentence_length_variance"],
            "lexical_diversity": vocab["lexical_diversity"],
            "stopword_ratio": vocab["stopword_ratio"],
            "pos_percentages": pos.get("pos_percentages", {})
        }
        style = self.style.interpret(style_features)

        return {
            "metadata": {
                "name": name,
                "text_id": text_id,
                "text_length": len(text),
                "timestamp": datetime.now().isoformat()
            },
            "basic_statistics": stats,
            "vocabulary": vocab,
            "pos_distribution": pos,
            "ngrams": {
                "bigrams": bigrams,
                "trigrams": trigrams
            },
            "style_interpretation": style
        }
