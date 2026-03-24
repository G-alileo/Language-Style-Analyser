from collections import Counter
from nltk.corpus import stopwords


class VocabularyAnalyser:

    def __init__(self):
        self._stopwords = set(stopwords.words('english'))

    def analyse(self, tokens):
        lower_tokens = [t.lower() for t in tokens]
        return {
            "total_words": len(lower_tokens),
            "unique_words": self.get_unique_word_count(lower_tokens),
            "lexical_diversity": self.calculate_lexical_diversity(lower_tokens),
            "stopword_ratio": self.calculate_stopword_ratio(lower_tokens),
            "top_words": self.get_word_frequency(lower_tokens, 10)
        }

    def calculate_lexical_diversity(self, tokens):
        if not tokens:
            return 0.0
        unique = len(set(tokens))
        total = len(tokens)
        return round(unique / total, 2)

    def calculate_stopword_ratio(self, tokens):
        if not tokens:
            return 0.0
        lower_tokens = [t.lower() for t in tokens]
        stopword_count = sum(1 for t in lower_tokens if t in self._stopwords)
        return round(stopword_count / len(tokens), 2)

    def get_word_frequency(self, tokens, top_n=10):
        lower_tokens = [t.lower() for t in tokens]
        counter = Counter(lower_tokens)
        return counter.most_common(top_n)

    def get_unique_word_count(self, tokens):
        lower_tokens = [t.lower() for t in tokens]
        return len(set(lower_tokens))
