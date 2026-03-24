from nltk import ngrams
from collections import Counter


class NGramAnalyser:

    def analyse(self, tokens, n=2, top_k=10):
        lower_tokens = [t.lower() for t in tokens]
        grams = list(ngrams(lower_tokens, n))
        counter = Counter(grams)
        top_grams = counter.most_common(top_k)
        return [(" ".join(gram), count) for gram, count in top_grams]

    def get_bigrams(self, tokens, top_k=10):
        return self.analyse(tokens, n=2, top_k=top_k)

    def get_trigrams(self, tokens, top_k=10):
        return self.analyse(tokens, n=3, top_k=top_k)
