import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from core.batch_processor import BatchProcessor
from core.similarity_scorer import SimilarityScorer
from utilities.comparison_generator import ComparisonGenerator
from utilities.export_formatter import ExportFormatter


st.set_page_config(page_title="Comparison Tool", page_icon="📈", layout="wide")

st.title("🧬 Comparison Tool")
st.write("Compare multiple texts and analyze their similarities.")

# Initialize processors
batch_processor = BatchProcessor()
similarity_scorer = SimilarityScorer()
comparison_generator = ComparisonGenerator()
export_formatter = ExportFormatter()

# Input method tabs
tab_upload, tab_previous = st.tabs(["📤 Upload Files", "📚 Use Previous Analysis"])

with tab_upload:
    st.subheader("Upload Texts to Compare")
    uploaded_files = st.file_uploader(
        "Choose 2+ .txt files",
        type=["txt"],
        accept_multiple_files=True,
        key="comparison_upload"
    )

    if uploaded_files:
        if len(uploaded_files) < 2:
            st.warning("Please upload at least 2 texts to compare.")
        else:
            st.success(f"Uploaded {len(uploaded_files)} file(s)")

            if st.button("Compare Texts", type="primary", key="compare_upload"):
                texts = []
                names = []

                for file in uploaded_files:
                    try:
                        text = file.read().decode('utf-8')
                        texts.append(text)
                        names.append(file.name.replace('.txt', ''))
                    except Exception as e:
                        st.error(f"Error reading {file.name}: {e}")

                if texts:
                    with st.spinner("Analyzing and comparing texts..."):
                        fingerprints = batch_processor.analyze_multiple(texts, names)
                        st.session_state.comparison_fingerprints = fingerprints

                    st.success("Comparison complete!")

with tab_previous:
    st.subheader("Compare Previous Batch Analysis")

    if 'batch_results' not in st.session_state or not st.session_state.batch_results:
        st.info("No previous batch analysis found. Upload files in the 'Batch Analysis' page first, or upload here.")
    else:
        batch_results = st.session_state.batch_results

        # Let user select which texts to compare
        available_names = [fp['metadata']['name'] for fp in batch_results]

        if len(available_names) < 2:
            st.warning("Need at least 2 texts to compare.")
        else:
            selected_names = st.multiselect(
                "Select texts to compare:",
                available_names,
                default=available_names[:min(2, len(available_names))]
            )

            if len(selected_names) < 2:
                st.warning("Please select at least 2 texts.")
            elif st.button("Compare Selected Texts", type="primary", key="compare_previous"):
                selected_fps = [fp for fp in batch_results if fp['metadata']['name'] in selected_names]
                st.session_state.comparison_fingerprints = selected_fps
                st.success("Texts loaded for comparison!")

# Display comparison results
if 'comparison_fingerprints' in st.session_state and len(st.session_state.comparison_fingerprints) >= 2:
    fingerprints = st.session_state.comparison_fingerprints

    with st.spinner("Computing similarities..."):
        comparison_data = similarity_scorer.compare_all_pairs(fingerprints)

    # Large batch warning
    if comparison_data.get('large_batch_warning'):
        st.warning(f"⚠️ Comparing {comparison_data['matrix_size']} texts ({comparison_data['matrix_size']**2} comparisons). This may be slow.")

    st.divider()
    st.subheader("📊 Comparison Results")

    # Display heatmap
    st.write("**Similarity Heatmap:**")
    heatmap_data = comparison_generator.generate_heatmap_data(
        comparison_data['matrix'],
        comparison_data['labels']
    )

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data['z'],
        x=heatmap_data['x'],
        y=heatmap_data['y'],
        colorscale='Viridis',
        text=heatmap_data['z'].round(1),
        texttemplate='%{text:.0f}',
        textfont={"size": 10},
        hovertemplate=heatmap_data['hovertemplate']
    ))
    fig.update_layout(
        title='Overall Similarity Score Matrix',
        height=500,
        xaxis_title='Text',
        yaxis_title='Text'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Display pairwise details
    st.write("**Pairwise Comparisons:**")

    for pair in comparison_data['pairs']:
        text1 = pair['text1_name']
        text2 = pair['text2_name']
        sim = pair['overall_similarity']

        with st.expander(f"🔍 {text1} ↔ {text2} (Similarity: {sim:.1f}/100)"):
            # Recommendation
            recommendation = comparison_generator.generate_recommendation(
                fingerprints[pair['text1_id']],
                fingerprints[pair['text2_id']],
                sim
            )
            st.info(recommendation)

            # Detailed scores
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Overall", f"{sim:.0f}")
            with col2:
                st.metric("Style Match", f"{pair['details']['style_match']:.0f}")
            with col3:
                st.metric("Complexity", f"{pair['details']['complexity_match']:.0f}")
            with col4:
                st.metric("Vocabulary", f"{pair['details']['vocabulary_match']:.0f}")
            with col5:
                st.metric("N-grams", f"{pair['details']['ngram_overlap']:.0f}")

            # Side-by-side style scores
            st.write("**Style Profile Comparison:**")
            col_l, col_r = st.columns(2)

            fp1 = fingerprints[pair['text1_id']]
            fp2 = fingerprints[pair['text2_id']]

            with col_l:
                st.write(f"**{text1}**")
                scores1 = fp1['style_interpretation']['style_scores']
                fig1 = px.bar(
                    x=list(scores1.keys()),
                    y=list(scores1.values()),
                    title=f"Styles - {text1}",
                    color=list(scores1.values()),
                    color_continuous_scale="Blues"
                )
                fig1.update_layout(showlegend=False, height=350)
                st.plotly_chart(fig1, use_container_width=True)

            with col_r:
                st.write(f"**{text2}**")
                scores2 = fp2['style_interpretation']['style_scores']
                fig2 = px.bar(
                    x=list(scores2.keys()),
                    y=list(scores2.values()),
                    title=f"Styles - {text2}",
                    color=list(scores2.values()),
                    color_continuous_scale="Oranges"
                )
                fig2.update_layout(showlegend=False, height=350)
                st.plotly_chart(fig2, use_container_width=True)

    # Overall comparison report
    st.divider()
    st.subheader("📋 Overall Comparison Report")

    report = comparison_generator.generate_comparison_report(fingerprints)

    st.write(f"**Summary:** {report['summary']}")

    if report.get('common_patterns'):
        st.write("**Common Patterns Found:**")
        for i, pattern in enumerate(report['common_patterns'], 1):
            st.write(f"  {i}. \"{pattern}\"")

    st.write("**Style Distribution:**")
    for name, style in report['dominant_styles'].items():
        st.write(f"  • **{name}**: {style}")

    # Export options
    st.divider()
    st.subheader("📥 Export Comparison Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        json_data = export_formatter.to_json(fingerprints)
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name="comparison_results.json",
            mime="application/json"
        )

    with col2:
        csv_data = export_formatter.to_csv(fingerprints)
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="comparison_results.csv",
            mime="text/csv"
        )

    with col3:
        html_data = export_formatter.to_html(fingerprints, comparison_data)
        st.download_button(
            label="Download HTML",
            data=html_data,
            file_name="comparison_results.html",
            mime="text/html"
        )

    st.info("💡 Tip: HTML reports can be printed to PDF from your browser (Ctrl+P / Cmd+P)")
