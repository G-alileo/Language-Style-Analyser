import streamlit as st

st.set_page_config(
    page_title="Language Style Fingerprint Analyzer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.info(
    "🧬 **Navigation:**\n\n"
    "• **Home** — Analyze single text\n"
    "• **Batch** — Analyze multiple texts\n"
    "• **Comparison** — Compare texts side-by-side"
)
