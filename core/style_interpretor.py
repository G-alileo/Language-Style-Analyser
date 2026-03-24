class StyleInterpretor:

    MINIMUM_WORDS = 10
    LOW_CONFIDENCE_THRESHOLD = 30
    INDETERMINATE_THRESHOLD = 25
    MIXED_STYLE_MARGIN = 8
    VARIED_STYLE_MARGIN = 12

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

    def _gradient_score(self, value, low, high, max_points):
        if value <= low:
            return 0
        if value >= high:
            return max_points
        return int(((value - low) / (high - low)) * max_points)

    def _inverse_gradient(self, value, low, high, max_points):
        if value >= high:
            return 0
        if value <= low:
            return max_points
        return int(((high - value) / (high - low)) * max_points)

    def _range_score(self, value, ideal_low, ideal_high, tolerance, max_points):
        if ideal_low <= value <= ideal_high:
            return max_points
        if value < ideal_low:
            diff = ideal_low - value
            return max(0, max_points - int((diff / tolerance) * max_points))
        else:
            diff = value - ideal_high
            return max(0, max_points - int((diff / tolerance) * max_points))

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
        aux_ratio = pos_percentages.get("AUX", 0)

        academic = self._score_academic(
            avg_length, noun_ratio, verb_ratio, lexical_diversity, stopword_ratio, adj_ratio
        )
        conversational = self._score_conversational(
            avg_length, stopword_ratio, lexical_diversity, pron_ratio, aux_ratio, verb_ratio, noun_ratio
        )
        descriptive = self._score_descriptive(
            adj_ratio, adv_ratio, lexical_diversity, noun_ratio, verb_ratio, avg_length
        )
        narrative = self._score_narrative(
            verb_ratio, pron_ratio, avg_length, noun_ratio, aux_ratio, sentence_length_variance
        )
        technical = self._score_technical(
            noun_ratio, stopword_ratio, lexical_diversity, avg_length, verb_ratio, adj_ratio
        )
        persuasive = self._score_persuasive(
            verb_ratio, pron_ratio, avg_length, stopword_ratio, aux_ratio, noun_ratio
        )
        journalistic = self._score_journalistic(
            avg_length, noun_ratio, verb_ratio, lexical_diversity, stopword_ratio
        )
        creative = self._score_creative(
            lexical_diversity, sentence_length_variance, adj_ratio, adv_ratio, avg_length
        )

        return {
            "academic": max(0, min(100, academic)),
            "conversational": max(0, min(100, conversational)),
            "descriptive": max(0, min(100, descriptive)),
            "narrative": max(0, min(100, narrative)),
            "technical": max(0, min(100, technical)),
            "persuasive": max(0, min(100, persuasive)),
            "journalistic": max(0, min(100, journalistic)),
            "creative": max(0, min(100, creative))
        }

    def _score_academic(self, avg_length, noun_ratio, verb_ratio, lexical_diversity, stopword_ratio, adj_ratio):
        score = 0
        score += self._gradient_score(avg_length, 15, 28, 30)
        score += self._gradient_score(noun_ratio, 20, 40, 25)
        score += self._gradient_score(lexical_diversity, 0.55, 0.8, 20)
        score += self._inverse_gradient(stopword_ratio, 0.25, 0.45, 15)
        if verb_ratio < noun_ratio:
            score += 10
        if avg_length > 20:
            score += 15
        if avg_length < 12:
            score -= 25
        if stopword_ratio > 0.5:
            score -= 15
        if noun_ratio < 18:
            score -= 15
        return score

    def _score_conversational(self, avg_length, stopword_ratio, lexical_diversity, pron_ratio, aux_ratio, verb_ratio, noun_ratio):
        score = 0
        score += self._inverse_gradient(avg_length, 5, 12, 30)
        score += self._gradient_score(stopword_ratio, 0.45, 0.6, 25)
        score += self._gradient_score(pron_ratio, 10, 25, 20)
        score += self._gradient_score(aux_ratio, 6, 15, 15)
        if verb_ratio >= noun_ratio:
            score += 10
        if lexical_diversity > 0.75:
            score += 5
        if avg_length > 14:
            score -= 30
        if stopword_ratio < 0.4:
            score -= 25
        if pron_ratio < 8:
            score -= 15
        if aux_ratio < 4:
            score -= 10
        return score

    def _score_descriptive(self, adj_ratio, adv_ratio, lexical_diversity, noun_ratio, verb_ratio, avg_length):
        score = 0
        score += self._gradient_score(adj_ratio, 12, 22, 35)
        score += self._gradient_score(adv_ratio, 6, 15, 25)
        score += self._gradient_score(lexical_diversity, 0.5, 0.7, 15)
        if noun_ratio > verb_ratio:
            score += 10
        if 12 < avg_length < 20:
            score += 10
        if adj_ratio < 10:
            score -= 25
        if adv_ratio < 4:
            score -= 15
        if avg_length > 22:
            score -= 20
        return score

    def _score_narrative(self, verb_ratio, pron_ratio, avg_length, noun_ratio, aux_ratio, variance):
        score = 0
        score += self._gradient_score(verb_ratio, 18, 28, 25)
        score += self._gradient_score(pron_ratio, 8, 20, 20)
        score += self._range_score(avg_length, 10, 16, 4, 20)
        if noun_ratio > 12 and noun_ratio < 25:
            score += 15
        if aux_ratio > 5 and aux_ratio < 12:
            score += 10
        if pron_ratio < 6:
            score -= 30
        if verb_ratio < 15:
            score -= 20
        if avg_length < 8:
            score -= 20
        if avg_length > 20:
            score -= 10
        return score

    def _score_technical(self, noun_ratio, stopword_ratio, lexical_diversity, avg_length, verb_ratio, adj_ratio):
        score = 0
        score += self._gradient_score(noun_ratio, 30, 50, 30)
        score += self._inverse_gradient(stopword_ratio, 0.2, 0.4, 25)
        score += self._gradient_score(lexical_diversity, 0.6, 0.8, 20)
        score += self._gradient_score(avg_length, 12, 20, 15)
        if verb_ratio < 20:
            score += 10
        if adj_ratio < 10:
            score += 5
        if noun_ratio < 25:
            score -= 25
        if stopword_ratio > 0.5:
            score -= 20
        return score

    def _score_persuasive(self, verb_ratio, pron_ratio, avg_length, stopword_ratio, aux_ratio, noun_ratio):
        score = 0
        score += self._gradient_score(verb_ratio, 18, 28, 30)
        score += self._inverse_gradient(avg_length, 6, 12, 25)
        score += self._gradient_score(pron_ratio, 8, 18, 20)
        score += self._gradient_score(aux_ratio, 6, 14, 15)
        if verb_ratio > noun_ratio:
            score += 15
        if stopword_ratio > 0.38:
            score += 5
        if avg_length > 14:
            score -= 25
        if verb_ratio < 18:
            score -= 15
        if pron_ratio < 8:
            score -= 15
        return score

    def _score_journalistic(self, avg_length, noun_ratio, verb_ratio, lexical_diversity, stopword_ratio):
        score = 0
        score += self._range_score(avg_length, 12, 18, 4, 25)
        score += self._range_score(noun_ratio, 25, 38, 8, 25)
        score += self._range_score(verb_ratio, 15, 25, 5, 20)
        score += self._range_score(lexical_diversity, 0.5, 0.68, 0.1, 15)
        score += self._range_score(stopword_ratio, 0.35, 0.5, 0.1, 10)
        if avg_length < 8 or avg_length > 25:
            score -= 20
        return score

    def _score_creative(self, lexical_diversity, variance, adj_ratio, adv_ratio, avg_length):
        score = 0
        score += self._gradient_score(lexical_diversity, 0.65, 0.85, 30)
        score += self._gradient_score(variance, 8, 20, 25)
        score += self._gradient_score(adj_ratio, 8, 18, 15)
        score += self._gradient_score(adv_ratio, 4, 12, 10)
        if variance > 10:
            score += 10
        if lexical_diversity < 0.55:
            score -= 25
        if variance < 4:
            score -= 20
        return score

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
            if top_score - score <= self.VARIED_STYLE_MARGIN and score >= self.INDETERMINATE_THRESHOLD
        ]

        if len(styles_within_varied_margin) >= 3:
            top_three = [s.capitalize() for s in styles_within_varied_margin[:3]]
            return f"Varied ({', '.join(top_three)})"

        if len(sorted_scores) >= 2:
            second_score = sorted_scores[1][1]
            second_style = sorted_scores[1][0]
            if top_score - second_score <= self.MIXED_STYLE_MARGIN and second_score >= self.INDETERMINATE_THRESHOLD:
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
