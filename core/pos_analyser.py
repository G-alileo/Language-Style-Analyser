import spacy
from collections import Counter


class POSAnalyser:

    _nlp = None

    def __init__(self):
        self._text = None
        self._doc = None
        if POSAnalyser._nlp is None:
            POSAnalyser._nlp = spacy.load("en_core_web_sm")

    def process(self, text):
        if text == self._text:
            return
        self._text = text
        self._doc = POSAnalyser._nlp(text)

    def analyse(self):
        if self._doc is None:
            return {}
        pos_counts = self.get_pos_distribution()
        pos_percentages = self.get_pos_percentages()
        dominant = max(pos_counts, key=pos_counts.get) if pos_counts else ""
        return {
            "pos_counts": pos_counts,
            "pos_percentages": pos_percentages,
            "dominant_pos": dominant
        }

    def get_pos_tags(self):
        if self._doc is None:
            return []
        return [(token.text, token.pos_) for token in self._doc if token.is_alpha]

    def get_pos_distribution(self):
        if self._doc is None:
            return {}
        tags = [token.pos_ for token in self._doc if token.is_alpha]
        return dict(Counter(tags))

    def get_pos_percentages(self):
        distribution = self.get_pos_distribution()
        total = sum(distribution.values())
        if total == 0:
            return {}
        return {pos: round((count / total) * 100, 1) for pos, count in distribution.items()}

    def reset(self):
        self._text = None
        self._doc = None
