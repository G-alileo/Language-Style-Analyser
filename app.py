import streamlit as st
import plotly.express as px

from utilities.text_cleaner import TextCleaner
from core.tokeniser import Tokeniser
from core.vocabulary import VocabularyAnalyser
from core.pos_analyser import POSAnalyser
from core.ngram_analyser import NGramAnalyser
from core.style_interpretor import StyleInterpretor


def aggregate_features(stats, vocab, pos, bigrams, trigrams, style):
    return {
        "basic_statistics": stats,
        "vocabulary": vocab,
        "pos_distribution": pos,
        "ngrams": {
            "bigrams": bigrams,
            "trigrams": trigrams
        },
        "style_interpretation": style
    }


def display_basic_statistics(stats):
    st.subheader("Basic Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Sentences", stats["sentence_count"])
    col2.metric("Words", stats["word_count"])
    col3.metric("Avg Length", stats["avg_sentence_length"])

    col4, col5 = st.columns(2)
    col4.metric("Min Sentence", stats["min_sentence_length"])
    col5.metric("Max Sentence", stats["max_sentence_length"])


def display_vocabulary(vocab):
    st.subheader("Vocabulary Analysis")
    col1, col2 = st.columns(2)
    col1.metric("Lexical Diversity", vocab["lexical_diversity"])
    col2.metric("Stopword Ratio", vocab["stopword_ratio"])

    st.write("**Top Words:**")
    if vocab["top_words"]:
        words_data = [{"Word": w, "Count": c} for w, c in vocab["top_words"]]
        st.table(words_data)


def display_pos_distribution(pos):
    st.subheader("Part-of-Speech Distribution")
    st.write(f"**Dominant POS:** {pos.get('dominant_pos', 'N/A')}")

    percentages = pos.get("pos_percentages", {})
    if percentages:
        fig = px.pie(
            names=list(percentages.keys()),
            values=list(percentages.values()),
            title="POS Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)


def display_ngrams(ngrams):
    st.subheader("N-Gram Patterns")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Bigrams:**")
        if ngrams["bigrams"]:
            bigram_data = [{"Phrase": p, "Count": c} for p, c in ngrams["bigrams"]]
            st.table(bigram_data)

    with col2:
        st.write("**Trigrams:**")
        if ngrams["trigrams"]:
            trigram_data = [{"Phrase": p, "Count": c} for p, c in ngrams["trigrams"]]
            st.table(trigram_data)


def display_style_interpretation(style):
    st.subheader("Style Interpretation")

    complexity = style.get("complexity", {})
    vocabulary = style.get("vocabulary_assessment", {})

    col1, col2 = st.columns(2)
    col1.metric("Complexity", complexity.get("label", "N/A"), f"Score: {complexity.get('score', 0)}")
    col2.metric("Vocabulary", vocabulary.get("label", "N/A"), f"Score: {vocabulary.get('score', 0)}")

    st.write(f"**Dominant Style:** {style.get('dominant_style', 'N/A')}")

    scores = style.get("style_scores", {})
    if scores:
        fig = px.bar(
            x=list(scores.keys()),
            y=list(scores.values()),
            labels={"x": "Style", "y": "Score"},
            title="Style Scores"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.info(style.get("summary", ""))


def main():
    st.set_page_config(
        page_title="Language Style Fingerprint Analyzer",
        page_icon="📝",
        layout="wide"
    )

    st.title("Language Style Fingerprint Analyzer")
    st.write("Analyze the linguistic characteristics of your text.")

    text_input = st.text_area(
        "Enter your text:",
        height=200,
        placeholder="Paste your text here..."
    )

    if st.button("Analyze", type="primary"):
        if not text_input.strip():
            st.warning("Please enter some text to analyze.")
            return

        with st.spinner("Analyzing text..."):
            cleaner = TextCleaner()
            clean_text = cleaner.clean(text_input)

            tokeniser = Tokeniser()
            tokeniser.tokenise(clean_text)
            stats = tokeniser.get_statistics()
            words = tokeniser.get_words()

            vocab_analyser = VocabularyAnalyser()
            vocab = vocab_analyser.analyse(words)

            pos_analyser = POSAnalyser()
            pos_analyser.process(clean_text)
            pos = pos_analyser.analyse()

            ngram_analyser = NGramAnalyser()
            bigrams = ngram_analyser.get_bigrams(words, top_k=5)
            trigrams = ngram_analyser.get_trigrams(words, top_k=5)

            style_features = {
                "avg_sentence_length": stats["avg_sentence_length"],
                "lexical_diversity": vocab["lexical_diversity"],
                "stopword_ratio": vocab["stopword_ratio"],
                "pos_percentages": pos.get("pos_percentages", {})
            }
            style_interpretor = StyleInterpretor()
            style = style_interpretor.interpret(style_features)

            fingerprint = aggregate_features(stats, vocab, pos, bigrams, trigrams, style)

        st.success("Analysis complete!")
        st.divider()

        display_basic_statistics(fingerprint["basic_statistics"])
        st.divider()

        display_vocabulary(fingerprint["vocabulary"])
        st.divider()

        display_pos_distribution(fingerprint["pos_distribution"])
        st.divider()

        display_ngrams(fingerprint["ngrams"])
        st.divider()

        display_style_interpretation(fingerprint["style_interpretation"])


if __name__ == "__main__":
    main()
