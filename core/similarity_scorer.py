from typing import List, Dict, Tuple
import numpy as np


class SimilarityScorer:

    def compute_style_similarity(self, fingerprint1: dict, fingerprint2: dict) -> float:
        styles1 = fingerprint1['style_interpretation']['style_scores']
        styles2 = fingerprint2['style_interpretation']['style_scores']

        keys = sorted(styles1.keys())
        v1 = np.array([styles1[k] for k in keys])
        v2 = np.array([styles2[k] for k in keys])

        dot_product = np.dot(v1, v2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))

    def compute_comprehensive_similarity(self, fp1: dict, fp2: dict) -> dict:
        style_sim = self.compute_style_similarity(fp1, fp2) * 100

        comp1 = fp1['style_interpretation']['complexity']['score']
        comp2 = fp2['style_interpretation']['complexity']['score']
        complexity_match = 100 - abs(comp1 - comp2)

        vocab1 = fp1['style_interpretation']['vocabulary_assessment']['score']
        vocab2 = fp2['style_interpretation']['vocabulary_assessment']['score']
        vocabulary_match = 100 - abs(vocab1 - vocab2)

        bigrams1 = set([p for p, _ in fp1['ngrams']['bigrams']])
        bigrams2 = set([p for p, _ in fp2['ngrams']['bigrams']])
        if bigrams1 or bigrams2:
            intersection = len(bigrams1 & bigrams2)
            union = len(bigrams1 | bigrams2)
            ngram_overlap = (intersection / union * 100) if union > 0 else 0
        else:
            ngram_overlap = 0

        overall = (
            style_sim * 0.40 +
            complexity_match * 0.25 +
            vocabulary_match * 0.20 +
            ngram_overlap * 0.15
        )

        return {
            'overall': overall,
            'style_match': style_sim,
            'complexity_match': complexity_match,
            'vocabulary_match': vocabulary_match,
            'ngram_overlap': ngram_overlap
        }

    def compare_all_pairs(self, fingerprints: List[dict]) -> dict:
        n = len(fingerprints)
        matrix = np.zeros((n, n))
        labels = [fp['metadata']['name'] for fp in fingerprints]

        for i in range(n):
            for j in range(n):
                if i == j:
                    matrix[i][j] = 100.0
                elif i > j:
                    matrix[i][j] = matrix[j][i]
                else:
                    sim_data = self.compute_comprehensive_similarity(fingerprints[i], fingerprints[j])
                    matrix[i][j] = sim_data['overall']

        pairs = []
        for i in range(n):
            for j in range(i + 1, n):
                sim_data = self.compute_comprehensive_similarity(fingerprints[i], fingerprints[j])
                pairs.append({
                    'text1_id': i,
                    'text1_name': labels[i],
                    'text2_id': j,
                    'text2_name': labels[j],
                    'overall_similarity': sim_data['overall'],
                    'details': sim_data
                })

        return {
            'matrix': matrix,
            'labels': labels,
            'pairs': pairs,
            'matrix_size': n,
            'large_batch_warning': n > 15
        }
