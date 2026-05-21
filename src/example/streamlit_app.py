import streamlit as st
from main import run_from_streamlit

# Page settings
st.set_page_config(page_title="Fake News Debunker MAS", page_icon="🕵️‍♂️")

st.title("🕵️‍♂️ Fake News Debunker MAS")
st.markdown("Graphical user interface for the multi-agent system debunking workflow.")

# User text input
news_input = st.text_area(
    "Paste the news text to analyze here:", 
    height=150,
    placeholder="Example: The Ministry of Health just approved a secret decree stating that..."
)

if st.button("Start Analysis", type="primary"):
    if not news_input.strip():
        st.warning("⚠️ Please enter some text before running the analysis.")
    else:
        with st.spinner("Agents are debating and verifying sources..."):
            try:
                # Call the mock orchestrator function
                result = run_from_streamlit(news_input)
                
                st.success("Analysis Completed!")
                st.divider()
                
                # Dynamic verdict coloring based on result
                if result.final_verdict == "FAKE":
                    st.error(f"## Verdict: {result.final_verdict}")
                elif result.final_verdict == "REAL":
                    st.success(f"## Verdict: {result.final_verdict}")
                else:
                    st.warning(f"## Verdict: {result.final_verdict}")
                    
                st.markdown(f"### 📝 Jury Reasoning\n{result.reasoning}")
                
                # Expandable details section
                with st.expander("📊 Individual Judge Votes"):
                    for idx, vote in enumerate(result.judge_votes, 1):
                        st.write(f"• Judge {idx}: **{vote}**")
                        
            except Exception as e:
                st.error(f"An error occurred in the UI layer: {e}")