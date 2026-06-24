# app.py
import streamlit as st
from prompt import get_master_prompt
from utils import sanitize_html_output, convert_html_to_pdf, generate_safe_filename
from service import GeminiService
from topics import TOPIC_PRESETS


def main():
    st.set_page_config(page_title="Elite Indian Study Material Generator", layout="centered")
    st.title("🇮🇳 Premium Study Material Pipeline")
    st.caption("Generate ultra-clean, micro-styled CBSE/ICSE study guides exported to PDF.")

    # --- AUTHENTICATION ---
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
    if not api_key:
        st.warning("⚠️ Please enter your Gemini API Key in the left sidebar to begin.")
        st.stop() # Stops the script here; prevents nested 'if' blocks below.

    # --- USER INPUTS ---
    selected_topic = st.selectbox("Choose a target topic:", TOPIC_PRESETS)
    if selected_topic == "Custom Topic":
        selected_topic = st.text_input("Enter your custom topic (e.g., 'Photosynthesis for Class 10'):")

    # --- EXECUTION TRIGGER ---
    if selected_topic and selected_topic != "Select a topic...":
        if st.button("⚡ Generate Premium PDF Guide", type="primary"):
            execute_generation_pipeline(api_key, selected_topic)


def execute_generation_pipeline(api_key: str, topic: str):
    """The master orchestrator function."""
    with st.spinner("🧠 Constructing micro-styled curriculum... (takes ~15 seconds)"):
        try:
            # 1. Initialize API Service
            llm = GeminiService(api_key=api_key)

            # 2. Prepare Data
            prompt = get_master_prompt(topic)
            raw_response = llm.generate_study_material(prompt)
            clean_html = sanitize_html_output(raw_response)

            st.success("✨ Layout Compiled Successfully!")

            # 3. Render Web View Preview
            with st.expander("👁️ Inspect Raw Web Layout", expanded=False):
                st.components.v1.html(clean_html, height=450, scrolling=True)                    

            # 4. Compile PDF 
            pdf_buffer = convert_html_to_pdf(clean_html)

            if pdf_buffer:
                st.download_button(
                    label="📥 Download Production PDF",
                    data=pdf_buffer,
                    file_name=generate_safe_filename(topic),
                    mime="application/pdf",
                    type="primary"
                )
            else:
                st.error("❌ Pisa failed to compile the generated HTML into a byte buffer.")

        except Exception as e:
            st.error(f"⚠️ Generation Pipeline Error: {str(e)}")


if __name__ == "__main__":
    main()