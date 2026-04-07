import json
import csv
import io
from typing import List, Optional, Dict
import plotly.express as px
import plotly.graph_objects as go


class ExportFormatter:

    def to_json(self, fingerprints: List[dict], pretty: bool = True) -> str:
        if isinstance(fingerprints, dict):
            fingerprints = [fingerprints]

        if pretty:
            return json.dumps(fingerprints, indent=2, default=str)
        else:
            return json.dumps(fingerprints, default=str)

    def to_csv(self, fingerprints: List[dict]) -> str:
        if isinstance(fingerprints, dict):
            fingerprints = [fingerprints]

        output = io.StringIO()
        fieldnames = [
            'name', 'word_count', 'sentence_count', 'avg_sentence_length',
            'complexity_label', 'complexity_score',
            'vocabulary_label', 'vocabulary_score',
            'lexical_diversity', 'stopword_ratio',
            'dominant_style',
            'academic', 'conversational', 'descriptive', 'narrative',
            'technical', 'persuasive', 'journalistic', 'creative'
        ]

        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for fp in fingerprints:
            stats = fp['basic_statistics']
            style = fp['style_interpretation']
            style_scores = style.get('style_scores', {})

            row = {
                'name': fp['metadata']['name'],
                'word_count': stats['word_count'],
                'sentence_count': stats['sentence_count'],
                'avg_sentence_length': stats['avg_sentence_length'],
                'complexity_label': style['complexity']['label'],
                'complexity_score': style['complexity']['score'],
                'vocabulary_label': style['vocabulary_assessment']['label'],
                'vocabulary_score': style['vocabulary_assessment']['score'],
                'lexical_diversity': fp['vocabulary']['lexical_diversity'],
                'stopword_ratio': fp['vocabulary']['stopword_ratio'],
                'dominant_style': style['dominant_style'],
                'academic': style_scores.get('academic', 0),
                'conversational': style_scores.get('conversational', 0),
                'descriptive': style_scores.get('descriptive', 0),
                'narrative': style_scores.get('narrative', 0),
                'technical': style_scores.get('technical', 0),
                'persuasive': style_scores.get('persuasive', 0),
                'journalistic': style_scores.get('journalistic', 0),
                'creative': style_scores.get('creative', 0),
            }
            writer.writerow(row)

        return output.getvalue()

    def to_html(self, fingerprints: List[dict], comparison_data: Optional[dict] = None) -> str:
        if isinstance(fingerprints, dict):
            fingerprints = [fingerprints]

        html_parts = []

        html_parts.append("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Language Style Analysis Report</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
            padding-top: 15px;
            border-top: 1px solid #ecf0f1;
        }
        .text-card {
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }
        .metric-box {
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 4px;
            text-align: center;
        }
        .metric-label {
            color: #7f8c8d;
            font-size: 12px;
            text-transform: uppercase;
            font-weight: bold;
        }
        .metric-value {
            color: #2c3e50;
            font-size: 24px;
            font-weight: bold;
            margin-top: 5px;
        }
        .chart-container {
            margin: 20px 0;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 4px;
        }
        .summary-text {
            background-color: #e8f4f8;
            padding: 15px;
            border-radius: 4px;
            margin: 15px 0;
            border-left: 4px solid #3498db;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ecf0f1;
        }
        th {
            background-color: #34495e;
            color: white;
        }
        tr:hover {
            background-color: #f8f9fa;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>🧬 Language Style Fingerprint Analysis</h1>
""")

        html_parts.append(f"""
    <div class="text-card">
        <strong>Report Generated:</strong> Analysis of {len(fingerprints)} text(s)
    </div>
""")

        for i, fp in enumerate(fingerprints):
            meta = fp['metadata']
            stats = fp['basic_statistics']
            style = fp['style_interpretation']
            vocab = fp['vocabulary']

            html_parts.append(f"""
    <h2>{meta['name']}</h2>
    <div class="text-card">
        <strong>Text Length:</strong> {meta['text_length']} characters<br>
        <strong>Words:</strong> {stats['word_count']}<br>
        <strong>Sentences:</strong> {stats['sentence_count']}
    </div>

    <h3>📊 Basic Metrics</h3>
    <div class="metrics-grid">
        <div class="metric-box">
            <div class="metric-label">Avg Sentence Length</div>
            <div class="metric-value">{stats['avg_sentence_length']}</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Lexical Diversity</div>
            <div class="metric-value">{vocab['lexical_diversity']:.2f}</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Stopword Ratio</div>
            <div class="metric-value">{vocab['stopword_ratio']:.2f}</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Complexity</div>
            <div class="metric-value">{style['complexity']['label'].title()}</div>
        </div>
    </div>

    <h3>🎨 Style Analysis</h3>
    <div class="metrics-grid">
        <div class="metric-box">
            <div class="metric-label">Dominant Style</div>
            <div class="metric-value">{style['dominant_style']}</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Vocabulary</div>
            <div class="metric-value">{style['vocabulary_assessment']['label'].title()}</div>
        </div>
    </div>

    <div class="summary-text">
        <strong>Summary:</strong> {style.get('summary', 'No summary available')}
    </div>
""")

            if style.get('style_scores'):
                fig = px.bar(
                    x=list(style['style_scores'].keys()),
                    y=list(style['style_scores'].values()),
                    labels={'x': 'Style', 'y': 'Score'},
                    title=f'Style Scores - {meta["name"]}'
                )
                fig.update_layout(showlegend=False, height=400)
                chart_html = fig.to_html(include_plotlyjs=False, div_id=f'chart_styles_{i}')
                html_parts.append(f'<div class="chart-container">{chart_html}</div>')

        if comparison_data and len(fingerprints) > 1:
            html_parts.append('<h2>📈 Comparison Heatmap</h2>')
            matrix = comparison_data['matrix']
            labels = comparison_data['labels']

            fig = go.Figure(data=go.Heatmap(
                z=matrix,
                x=labels,
                y=labels,
                colorscale='Viridis',
                text=matrix.round(1),
                texttemplate='%{text:.0f}',
                textfont={"size": 10},
                hovertemplate='%{y} vs %{x}: %{z:.1f}<extra></extra>'
            ))
            fig.update_layout(title='Similarity Matrix', height=500)
            chart_html = fig.to_html(include_plotlyjs=False, div_id='chart_heatmap')
            html_parts.append(f'<div class="chart-container">{chart_html}</div>')

        html_parts.append("""
</div>
</body>
</html>
""")

        return '\n'.join(html_parts)
