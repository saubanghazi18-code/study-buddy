import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards
import os

st.set_page_config(
    page_title="Study Buddy - Your AI Learning Companion",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern look
st.markdown("""
<style>
    .main {background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);}
    .stButton>button {width: 100%; height: 3em; background: #1E5A3F; color: white; border-radius: 12px;}
    .stButton>button:hover {background: #2E7C5A;}
    .card {background: white; padding: 20px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

colored_header(
    label="📚 Study Buddy",
    description="Turn PDFs & syllabi into smart study resources instantly",
    color_name="green-70"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("### Your Personal AI Tutor Powered by OpenAI + Web Search")

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/200x200/1E5A3F/FFFFFF?text=📖", use_column_width=True)
    st.title("Features")
    st.markdown("• PDF/DOCX Upload & Summarization\n• Smart Quizzes\n• YouTube Recommendations\n• Web Research\n• Progress Tracking")

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["📄 Upload & Summarize", "❓ Quiz Me", "🎥 Video Resources", "🔍 Research"])

with tab1:
    uploaded_file = st.file_uploader("Upload Syllabus / Notes (PDF or DOCX)", type=["pdf", "docx"])
    if uploaded_file:
        st.success("File processed successfully!")
        st.markdown("### Key Summary")
        st.write("AI-generated summary would appear here...")  # Integrate your backend here
        st.download_button("Download Summary", "summary.txt")

# Add more tabs with placeholders for your existing logic

st.markdown("---")
st.caption("Built with ❤️ using Streamlit + OpenAI + SerpAPI")
