class StyleInterpretor:

    def interpret(self, features):
        avg_length = features.get("avg_sentence_length", 0)
        lexical_diversity = features.get("lexical_diversity", 0)
        stopword_ratio = features.get("stopword_ratio", 0)
        pos_percentages = features.get("pos_percentages", {})

        complexity = self.classify_complexity(avg_length)
        vocabulary = self.classify_vocabulary(lexical_diversity, stopword_ratio)
        style_scores = self.calculate_style_scores(features)
        dominant_style = self.determine_dominant_style(style_scores)
        summary = self._generate_summary(complexity, vocabulary, dominant_style)

        return {
            "complexity": complexity,
            "vocabulary_assessment": vocabulary,
            "style_scores": style_scores,
            "dominant_style": dominant_style,
            "summary": summary
        }

    def calculate_style_scores(self, features):
        avg_length = features.get("avg_sentence_length", 0)
        lexical_diversity = features.get("lexical_diversity", 0)
        stopword_ratio = features.get("stopword_ratio", 0)
        pos_percentages = features.get("pos_percentages", {})

        noun_ratio = pos_percentages.get("NOUN", 0)
        verb_ratio = pos_percentages.get("VERB", 0)
        adj_ratio = pos_percentages.get("ADJ", 0)
        adv_ratio = pos_percentages.get("ADV", 0)
        pron_ratio = pos_percentages.get("PRON", 0)

        academic = 0
        if avg_length > 18:
            academic += 30
        if noun_ratio > 30:
            academic += 25
        if lexical_diversity > 0.6:
            academic += 20
        if stopword_ratio < 0.4:
            academic += 15

        conversational = 0
        if avg_length < 12:
            conversational += 30
        if verb_ratio > noun_ratio:
            conversational += 25
        if stopword_ratio > 0.5:
            conversational += 20
        if lexical_diversity < 0.5:
            conversational += 15

        descriptive = 0
        if adj_ratio > 15:
            descriptive += 40
        if adv_ratio > 10:
            descriptive += 30
        if lexical_diversity > 0.5:
            descriptive += 20

        narrative = 0
        if verb_ratio > 25:
            narrative += 35
        if 12 <= avg_length <= 18:
            narrative += 25
        if pron_ratio > 5:
            narrative += 20

        return {
            "academic": min(academic, 100),
            "conversational": min(conversational, 100),
            "descriptive": min(descriptive, 100),
            "narrative": min(narrative, 100)
        }

    def classify_complexity(self, avg_sentence_length):
        if avg_sentence_length < 10:
            label = "simple"
            score = 30
        elif avg_sentence_length < 18:
            label = "moderate"
            score = 60
        else:
            label = "complex"
            score = 90
        return {"label": label, "score": score}

    def classify_vocabulary(self, lexical_diversity, stopword_ratio):
        vocab_score = lexical_diversity * 100
        stopword_penalty = stopword_ratio * 20
        score = max(0, min(100, vocab_score - stopword_penalty))

        if lexical_diversity < 0.4:
            label = "limited"
        elif lexical_diversity < 0.6:
            label = "moderate"
        else:
            label = "rich"
        return {"label": label, "score": int(score)}

    def determine_dominant_style(self, scores):
        if not scores:
            return "Informational"
        dominant = max(scores, key=scores.get)
        return dominant.capitalize()

    def _generate_summary(self, complexity, vocabulary, dominant_style):
        comp_label = complexity.get("label", "moderate")
        vocab_label = vocabulary.get("label", "moderate")
        return (
            f"This text exhibits {comp_label} complexity with {vocab_label} vocabulary. "
            f"The dominant writing style is {dominant_style}."
        )
