class StyleInterpretor:

    MINIMUM_WORDS = 10
    LOW_CONFIDENCE_THRESHOLD = 30
    INDETERMINATE_THRESHOLD = 30
    MIXED_STYLE_MARGIN = 10
    VARIED_STYLE_MARGIN = 15

    def interpret(self, features):
        word_count = features.get("word_count", 0)
        sentence_count = features.get("sentence_count", 1)

        edge_case = self._check_edge_cases(word_count)
        if edge_case.get("status") == "insufficient_text":
            return edge_case

        avg_length = features.get("avg_sentence_length", 0)
        lexical_diversity = features.get("lexical_diversity", 0)
        stopword_ratio = features.get("stopword_ratio", 0)
        pos_percentages = features.get("pos_percentages", {})
        sentence_length_variance = features.get("sentence_length_variance", 0)

        complexity = self.classify_complexity(avg_length)
        vocabulary = self.classify_vocabulary(lexical_diversity, stopword_ratio)
        style_scores = self.calculate_style_scores(features)
        dominant_style = self.determine_dominant_style(style_scores)
        summary = self._generate_summary(complexity, vocabulary, dominant_style)

        result = {
            "complexity": complexity,
            "vocabulary_assessment": vocabulary,
            "style_scores": style_scores,
            "dominant_style": dominant_style,
            "summary": summary
        }

        if edge_case.get("status") == "low_confidence":
            result["confidence"] = "low"
            result["confidence_warning"] = edge_case.get("message")

        return result

    def _check_edge_cases(self, word_count):
        if word_count < self.MINIMUM_WORDS:
            return {
                "status": "insufficient_text",
                "message": f"Text has only {word_count} words. Minimum {self.MINIMUM_WORDS} words required for analysis.",
                "complexity": {"label": "unknown", "score": 0},
                "vocabulary_assessment": {"label": "unknown", "score": 0},
                "style_scores": {},
                "dominant_style": "Insufficient Text",
                "summary": "Unable to analyze. Please provide more text."
            }

        if word_count < self.LOW_CONFIDENCE_THRESHOLD:
            return {
                "status": "low_confidence",
                "message": f"Text has only {word_count} words. Results may be unreliable."
            }

        return {"status": "ok"}

    def calculate_style_scores(self, features):
        avg_length = features.get("avg_sentence_length", 0)
        lexical_diversity = features.get("lexical_diversity", 0)
        stopword_ratio = features.get("stopword_ratio", 0)
        pos_percentages = features.get("pos_percentages", {})
        sentence_length_variance = features.get("sentence_length_variance", 0)

        noun_ratio = pos_percentages.get("NOUN", 0)
        verb_ratio = pos_percentages.get("VERB", 0)
        adj_ratio = pos_percentages.get("ADJ", 0)
        adv_ratio = pos_percentages.get("ADV", 0)
        pron_ratio = pos_percentages.get("PRON", 0)

        academic = 0
        if avg_length > 18:
            academic += 25
        if noun_ratio > 30:
            academic += 25
        if lexical_diversity > 0.6:
            academic += 25
        if stopword_ratio < 0.4:
            academic += 25

        conversational = 0
        if avg_length < 12:
            conversational += 25
        if verb_ratio > noun_ratio:
            conversational += 25
        if stopword_ratio > 0.5:
            conversational += 25
        if lexical_diversity < 0.5:
            conversational += 25

        descriptive = 0
        if adj_ratio > 15:
            descriptive += 35
        if adv_ratio > 10:
            descriptive += 35
        if lexical_diversity > 0.5:
            descriptive += 30

        narrative = 0
        if verb_ratio > 25:
            narrative += 30
        if 12 <= avg_length <= 18:
            narrative += 25
        if pron_ratio > 8:
            narrative += 25
        if verb_ratio > 20:
            narrative += 20

        technical = 0
        if noun_ratio > 35:
            technical += 30
        if stopword_ratio < 0.35:
            technical += 30
        if lexical_diversity > 0.65:
            technical += 20
        if avg_length > 15:
            technical += 20

        persuasive = 0
        if verb_ratio > 20:
            persuasive += 35
        if avg_length < 15:
            persuasive += 25
        if pron_ratio > 5:
            persuasive += 20
        if stopword_ratio > 0.4:
            persuasive += 20

        journalistic = 0
        if 12 <= avg_length <= 18:
            journalistic += 30
        if 25 <= noun_ratio <= 35:
            journalistic += 25
        if 15 <= verb_ratio <= 25:
            journalistic += 25
        if 0.5 <= lexical_diversity <= 0.7:
            journalistic += 20

        creative = 0
        if lexical_diversity > 0.7:
            creative += 35
        if sentence_length_variance > 5:
            creative += 25
        if adj_ratio > 10:
            creative += 20
        if adv_ratio > 5:
            creative += 20

        return {
            "academic": min(academic, 100),
            "conversational": min(conversational, 100),
            "descriptive": min(descriptive, 100),
            "narrative": min(narrative, 100),
            "technical": min(technical, 100),
            "persuasive": min(persuasive, 100),
            "journalistic": min(journalistic, 100),
            "creative": min(creative, 100)
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
            return "Indeterminate"

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_score = sorted_scores[0][1]
        top_style = sorted_scores[0][0]

        if top_score < self.INDETERMINATE_THRESHOLD:
            return "Indeterminate"

        styles_within_varied_margin = [
            s for s, score in sorted_scores
            if top_score - score <= self.VARIED_STYLE_MARGIN
        ]

        if len(styles_within_varied_margin) >= 3:
            top_three = [s.capitalize() for s in styles_within_varied_margin[:3]]
            return f"Varied ({', '.join(top_three)})"

        if len(sorted_scores) >= 2:
            second_score = sorted_scores[1][1]
            second_style = sorted_scores[1][0]
            if top_score - second_score <= self.MIXED_STYLE_MARGIN:
                return f"Mixed ({top_style.capitalize()}/{second_style.capitalize()})"

        return top_style.capitalize()

    def _generate_summary(self, complexity, vocabulary, dominant_style):
        comp_label = complexity.get("label", "moderate")
        vocab_label = vocabulary.get("label", "moderate")

        if "Insufficient" in dominant_style:
            return "Unable to generate summary. Please provide more text."

        if "Indeterminate" in dominant_style:
            return (
                f"This text exhibits {comp_label} complexity with {vocab_label} vocabulary. "
                "No dominant writing style could be determined."
            )

        if "Varied" in dominant_style or "Mixed" in dominant_style:
            return (
                f"This text exhibits {comp_label} complexity with {vocab_label} vocabulary. "
                f"The writing style is {dominant_style.lower()}."
            )

        return (
            f"This text exhibits {comp_label} complexity with {vocab_label} vocabulary. "
            f"The dominant writing style is {dominant_style}."
        )
