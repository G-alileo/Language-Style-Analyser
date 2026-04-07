import streamlit as st
import plotly.express as px
from core.batch_processor import BatchProcessor
from utilities.export_formatter import ExportFormatter


st.set_page_config(page_title="Batch Analysis", page_icon="📁", layout="wide")

st.title("🧬 Batch Analysis")
st.write("Analyze multiple texts at once and export results.")

# Initialize processors
batch_processor = BatchProcessor()
export_formatter = ExportFormatter()

# Tabs for input method
tab_upload, tab_paste = st.tabs(["📤 Upload Files", "📝 Paste Text"])

with tab_upload:
    st.subheader("Upload Multiple Text Files")
    uploaded_files = st.file_uploader(
        "Choose .txt files",
        type=["txt"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.success(f"Uploaded {len(uploaded_files)} file(s)")

        if st.button("Analyze Batch", type="primary", key="analyze_upload"):
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
                with st.spinner("Analyzing texts..."):
                    fingerprints = batch_processor.analyze_multiple(texts, names)
                    st.session_state.batch_results = fingerprints

                st.success(f"Analysis complete! {len(fingerprints)} texts analyzed.")

with tab_paste:
    st.subheader("Paste Multiple Texts")
    st.info("Enter one text per section, separated by text names.")

    num_texts = st.number_input("Number of texts", min_value=1, max_value=10, value=2)

    texts = []
    names = []

    for i in range(num_texts):
        col1, col2 = st.columns([3, 1])
        with col1:
            text_input = st.text_area(
                f"Text {i+1}:",
                height=150,
                key=f"text_{i}",
                placeholder=f"Enter text {i+1}..."
            )
            texts.append(text_input)
        with col2:
            name_input = st.text_input(
                f"Name {i+1}:",
                value=f"Text {i+1}",
                key=f"name_{i}"
            )
            names.append(name_input)

    if st.button("Analyze Batch", type="primary", key="analyze_paste"):
        # Filter empty texts
        filled_texts = [(t, n) for t, n in zip(texts, names) if t.strip()]

        if not filled_texts:
            st.error("Please enter at least one text.")
        else:
            texts_to_analyze = [t for t, _ in filled_texts]
            names_to_analyze = [n for _, n in filled_texts]

            with st.spinner("Analyzing texts..."):
                fingerprints = batch_processor.analyze_multiple(texts_to_analyze, names_to_analyze)
                st.session_state.batch_results = fingerprints

            st.success(f"Analysis complete! {len(fingerprints)} texts analyzed.")

# Display results if available
if 'batch_results' in st.session_state and st.session_state.batch_results:
    st.divider()
    st.subheader("📊 Analysis Results")

    fingerprints = st.session_state.batch_results

    # Summary table
    st.write("**Summary Table:**")
    summary_data = []
    for fp in fingerprints:
        summary_data.append({
            'Name': fp['metadata']['name'],
            'Words': fp['basic_statistics']['word_count'],
            'Sentences': fp['basic_statistics']['sentence_count'],
            'Avg Length': f"{fp['basic_statistics']['avg_sentence_length']:.2f}",
            'Complexity': fp['style_interpretation']['complexity']['label'],
            'Vocabulary': fp['style_interpretation']['vocabulary_assessment']['label'],
            'Dominant Style': fp['style_interpretation']['dominant_style']
        })

    st.table(summary_data)

    # Expandable sections for each text
    st.write("**Detailed Analysis:**")
    for fp in fingerprints:
        with st.expander(f"📄 {fp['metadata']['name']}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Words", fp['basic_statistics']['word_count'])
            with col2:
                st.metric("Sentences", fp['basic_statistics']['sentence_count'])
            with col3:
                st.metric("Lexical Diversity", f"{fp['vocabulary']['lexical_diversity']:.2f}")

            st.write("**Style Scores:**")
            style_scores = fp['style_interpretation']['style_scores']
            if style_scores:
                fig = px.bar(
                    x=list(style_scores.keys()),
                    y=list(style_scores.values()),
                    title=f"Style Scores - {fp['metadata']['name']}"
                )
                st.plotly_chart(fig, use_container_width=True)

            st.write(f"**Summary:** {fp['style_interpretation'].get('summary', 'N/A')}")

    # Export options
    st.divider()
    st.subheader("📥 Export Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        json_data = export_formatter.to_json(fingerprints)
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name="batch_analysis.json",
            mime="application/json"
        )

    with col2:
        csv_data = export_formatter.to_csv(fingerprints)
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="batch_analysis.csv",
            mime="text/csv"
        )

    with col3:
        html_data = export_formatter.to_html(fingerprints)
        st.download_button(
            label="Download HTML",
            data=html_data,
            file_name="batch_analysis.html",
            mime="text/html"
        )

    st.info("💡 Tip: HTML reports can be printed to PDF from your browser (Ctrl+P / Cmd+P)")
