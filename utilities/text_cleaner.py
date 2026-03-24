import re
import unicodedata


class TextCleaner:

    def clean(self, text):
        text = self._normalize_unicode(text)
        text = self._normalize_whitespace(text)
        return text.strip()

    def normalize(self, text):
        return text.lower()

    def remove_special_characters(self, text):
        return re.sub(r'[^a-zA-Z0-9\s.,!?;:\'"()-]', '', text)

    def _normalize_unicode(self, text):
        return unicodedata.normalize('NFKC', text)

    def _normalize_whitespace(self, text):
        return re.sub(r'\s+', ' ', text)
