from typing import List, Dict
import numpy as np


class ComparisonGenerator:

    def generate_heatmap_data(self, similarity_matrix: np.ndarray, labels: List[str]) -> dict:
        return {
            'z': similarity_matrix,
            'x': labels,
            'y': labels,
            'hovertemplate': '%{y} vs %{x}: %{z:.1f}<extra></extra>'
        }

    def generate_comparison_report(self, fingerprints: List[dict]) -> dict:
        if not fingerprints:
            return {}

        dominant_styles = {}
        for fp in fingerprints:
            name = fp['metadata']['name']
            style = fp['style_interpretation']['dominant_style']
            dominant_styles[name] = style

        all_bigrams = []
        for fp in fingerprints:
            bigrams = [p for p, _ in fp['ngrams']['bigrams']]
            all_bigrams.extend(bigrams)

        from collections import Counter
        bigram_freq = Counter(all_bigrams)
        common_patterns = [phrase for phrase, count in bigram_freq.most_common(5) if count > 1]

        featured_texts = {}
        lexical_divs = {fp['metadata']['name']: fp['vocabulary']['lexical_diversity']
                       for fp in fingerprints}
        highest_div_name = max(lexical_divs, key=lexical_divs.get)
        featured_texts['highest_lexical_diversity'] = (highest_div_name, lexical_divs[highest_div_name])

        complexity_scores = {fp['metadata']['name']: fp['style_interpretation']['complexity']['score']
                           for fp in fingerprints}
        most_complex = max(complexity_scores, key=complexity_scores.get)
        featured_texts['most_complex'] = (most_complex, complexity_scores[most_complex])

        summary = f"Analysis of {len(fingerprints)} text(s). "
        if len(set(dominant_styles.values())) == 1:
            summary += f"All texts share a {list(dominant_styles.values())[0]} style."
        else:
            summary += f"Texts exhibit diverse styles: {', '.join(set(dominant_styles.values()))}."

        return {
            'summary': summary,
            'text_count': len(fingerprints),
            'dominant_styles': dominant_styles,
            'common_patterns': common_patterns,
            'featured_texts': featured_texts,
            'style_diversity': len(set(dominant_styles.values()))
        }

    def generate_recommendation(self, fp1: dict, fp2: dict, similarity: float) -> str:
        name1 = fp1['metadata']['name']
        name2 = fp2['metadata']['name']
        style1 = fp1['style_interpretation']['dominant_style']
        style2 = fp2['style_interpretation']['dominant_style']

        if similarity >= 90:
            tier_text = f"Nearly identical style profiles."
        elif similarity >= 75:
            tier_text = f"Very similar writing styles with minor variations."
        elif similarity >= 50:
            tier_text = f"Moderate style overlap with some distinguishing features."
        elif similarity >= 25:
            tier_text = f"Different writing styles with limited similarities."
        else:
            tier_text = f"Distinctly different styles with minimal overlap."

        differ = [] if style1 == style2 else [f"{name1} favors {style1}, while {name2} leans toward {style2}."]

        vocab1 = fp1['vocabulary']['lexical_diversity']
        vocab2 = fp2['vocabulary']['lexical_diversity']
        if abs(vocab1 - vocab2) > 0.15:
            vocab_comment = f"{name1 if vocab1 > vocab2 else name2} uses richer vocabulary."
            differ.append(vocab_comment)

        recommendation = tier_text
        if differ:
            recommendation += " " + " ".join(differ)

        return recommendation.strip()
