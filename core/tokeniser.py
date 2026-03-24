from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize


class Tokeniser:

    def __init__(self):
        self._text = None
        self._sentences = None
        self._words = None

    def tokenise(self, text):
        if text == self._text:
            return
        self._text = text
        self._sentences = sent_tokenize(text)
        all_words = []
        for sentence in self._sentences:
            tokens = word_tokenize(sentence)
            alpha_tokens = [t for t in tokens if t.isalpha()]
            all_words.extend(alpha_tokens)
        self._words = all_words

    def get_sentences(self):
        return self._sentences if self._sentences else []

    def get_words(self):
        return self._words if self._words else []

    def get_sentence_lengths(self):
        if not self._sentences:
            return []
        lengths = []
        for sentence in self._sentences:
            tokens = word_tokenize(sentence)
            alpha_tokens = [t for t in tokens if t.isalpha()]
            lengths.append(len(alpha_tokens))
        return lengths

    def get_statistics(self):
        sentences = self.get_sentences()
        words = self.get_words()
        lengths = self.get_sentence_lengths()

        sentence_count = len(sentences)
        word_count = len(words)
        avg_length = sum(lengths) / len(lengths) if lengths else 0.0
        min_length = min(lengths) if lengths else 0
        max_length = max(lengths) if lengths else 0
        variance = self._calculate_variance(lengths, avg_length)

        return {
            "sentence_count": sentence_count,
            "word_count": word_count,
            "avg_sentence_length": round(avg_length, 2),
            "min_sentence_length": min_length,
            "max_sentence_length": max_length,
            "sentence_length_variance": round(variance, 2)
        }

    def _calculate_variance(self, lengths, avg):
        if len(lengths) < 2:
            return 0.0
        squared_diffs = [(l - avg) ** 2 for l in lengths]
        return sum(squared_diffs) / len(lengths)

    def reset(self):
        self._text = None
        self._sentences = None
        self._words = None
