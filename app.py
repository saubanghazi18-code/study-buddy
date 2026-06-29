import streamlit as st
import time
import google.generativeai as genai

st.set_page_config(page_title="Study Buddy", layout="wide")

# ====================== YOUR GEMINI KEY ======================
GEMINI_API_KEY = "AQ.Ab8RN6J3c2Oa-gTJnNLhtmts6cSO14ofCFooT_7uOA5CPPJJsw"   # ← Paste your full key here

genai.configure(api_key=GEMINI_API_KEY)
st.sidebar.success("✅ Gemini Configured")
# =========================================================

# Rest of your code (Theme + UI)
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%); }
    .card { background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-radius: 20px; padding: 24px; }
    .title { color: #67e8f9; font-size: 1.85rem; font-weight: 600; margin-bottom: 1.2rem; }
    .timer-text { font-size: 6.8rem; font-weight: 700; font-family: monospace; color: #67e8f9; text-shadow: 0 0 35px rgba(103, 232, 249, 0.5); }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; font-size:3.5rem; color:#a5f3fc;'>Study Buddy</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#64748b;'>Focus. Learn. Achieve.</p>", unsafe_allow_html=True)
st.markdown("---")

# ... (keep the rest of your layout code the same as before)
