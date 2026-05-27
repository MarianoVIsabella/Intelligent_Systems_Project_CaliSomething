import streamlit as st
from main import run_from_streamlit

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Fake News Debunker MAS",
    page_icon="🕵️‍♂️",
    layout="wide"
)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.header("ℹ️ Project Info")

    st.write("""
    Multi-Agent System for Fake News Debunking.

    Technologies used:
    - CrewAI
    - Python
    - Streamlit
    - NLP Classification
    - Multi-Agent Debate
    """)

    st.divider()

    st.subheader("🔄 Workflow")

    st.markdown("""
    User Input  
    ⬇️  
    Categorizer Agent  
    ⬇️  
    Expert Verification Agent  
    ⬇️  
    Judge Debate System  
    ⬇️  
    Final Verdict
    """)

# =====================================================
# MAIN PAGE
# =====================================================

st.title("🕵️‍♂️ Fake News Debunker MAS")

st.markdown("""
Graphical User Interface for the Multi-Agent Fake News Debunking System.
""")

st.divider()

# =====================================================
# EXAMPLE NEWS BUTTON
# =====================================================

example_news = """
Scientists discovered that drinking coffee triples human lifespan according to a secret WHO report leaked online.
"""

if st.button("📄 Load Example News"):
    st.session_state["example_news"] = example_news

# =====================================================
# USER INPUT
# =====================================================

news_input = st.text_area(
    "Paste the news text to analyze here:",
    value=st.session_state.get("example_news", ""),
    height=200,
    placeholder="Example: The Ministry of Health approved a secret decree stating that..."
)

# =====================================================
# ANALYSIS BUTTON
# =====================================================

if st.button("🚀 Start Analysis", type="primary"):

    if not news_input.strip():

        st.warning("⚠️ Please enter some text before running the analysis.")

    else:

        with st.spinner("🤖 Agents are debating and verifying sources..."):

            try:

                # Call orchestrator function
                result = run_from_streamlit(news_input)

                st.success("✅ Analysis Completed!")

                st.divider()

                # =====================================================
                # FINAL VERDICT
                # =====================================================

                st.subheader("🏁 Final Verdict")

                if result.final_verdict == "FAKE":
                    st.error(f"### {result.final_verdict}")

                elif result.final_verdict == "REAL":
                    st.success(f"### {result.final_verdict}")

                else:
                    st.warning(f"### {result.final_verdict}")

                # =====================================================
                # CONFIDENCE SCORE
                # =====================================================

                if hasattr(result, "confidence"):

                    confidence_percentage = result.confidence * 100

                    st.metric(
                        label="Confidence Score",
                        value=f"{confidence_percentage:.1f}%"
                    )

                # =====================================================
                # REASONING
                # =====================================================

                st.subheader("📝 Jury Reasoning")

                st.write(result.reasoning)

                # =====================================================
                # JUDGE VOTES
                # =====================================================

                with st.expander("📊 Individual Judge Votes"):

                    for idx, vote in enumerate(result.judge_votes, start=1):

                        st.write(f"• Judge {idx}: **{vote}**")

                # =====================================================
                # SOURCES
                # =====================================================

                if hasattr(result, "sources") and result.sources:

                    with st.expander("🔗 Trusted Sources Used"):

                        for source in result.sources:

                            st.write(f"• {source}")

            except Exception as e:

                st.error(f"❌ An error occurred in the UI layer:\n\n{e}")

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption("Fake News Debunking MAS — CrewAI Project")