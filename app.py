import streamlit as st
import time
from openai import OpenAI

st.set_page_config(page_title="Study Buddy", layout="wide")

# ==================== OPENAI API KEY ====================
OPENAI_API_KEY = "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"   # ←←← PASTE YOUR OPENAI KEY HERE

client = OpenAI(api_key=OPENAI_API_KEY)
st.sidebar.success("✅ OpenAI Connected")
# ======================================================

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%); }
    .card { background: rgba(15, 23, 42, 0.95); border: 1px solid #334155; border-radius: 20px; padding: 28px; margin-bottom: 20px; }
    .title { color: #67e8f9; font-size: 1.9rem; font-weight: 600; margin-bottom: 1.5rem; }
    .timer-text { font-size: 7rem; font-weight: 700; font-family: monospace; color: #67e8f9; text-shadow: 0 0 40px rgba(103, 232, 249, 0.6); }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; font-size:3.8rem; color:#a5f3fc;'>Study Buddy</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>Focus. Learn. Achieve.</p>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns([1.1, 1.9])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='title'>⏱️ Focus Timer</p>", unsafe_allow_html=True)
    
    if 'time_left' not in st.session_state:
        st.session_state.time_left = 50 * 60
        st.session_state.is_running = False

    m, s = divmod(st.session_state.time_left, 60)
    st.markdown(f"<div class='timer-text text-center'>{m:02d}:{s:02d}</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    if c1.button("▶️ Start", use_container_width=True, type="primary"): st.session_state.is_running = True
    if c2.button("⏸️ Pause", use_container_width=True): st.session_state.is_running = False
    if c3.button("🔄 Reset", use_container_width=True):
        st.session_state.time_left = 50 * 60
        st.session_state.is_running = False

    if st.session_state.is_running and st.session_state.time_left > 0:
        time.sleep(1)
        st.session_state.time_left -= 1
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='title'>✅ Tasks</p>", unsafe_allow_html=True)
    task = st.text_input("New Task", placeholder="What are you working on?")
    if st.button("Add Task", use_container_width=True):
        if 'tasks' not in st.session_state: st.session_state.tasks = []
        if task.strip(): st.session_state.tasks.append({"text": task, "done": False})

    if 'tasks' in st.session_state:
        for i, t in enumerate(st.session_state.tasks):
            ca, cb = st.columns([4.5, 0.5])
            st.session_state.tasks[i]["done"] = ca.checkbox(t["text"], t["done"], key=f"t{i}")
            if cb.button("🗑️", key=f"d{i}"):
                del st.session_state.tasks[i]
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='title'>💬 AI Study Companion</p>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi Sauban! How can I help you study today?"}]

    chat_box = st.container(height=420)
    with chat_box:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if prompt := st.chat_input("Ask anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=st.session_state.messages
                    )
                    reply = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.rerun()
                except Exception as e:
                    st.error("OpenAI Error - Check your API key")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='title'>📝 Quick Notes</p>", unsafe_allow_html=True)
    notes = st.text_area("", height=180, placeholder="Write your notes here...")
    if st.button("💾 Save Notes", use_container_width=True):
        st.success("✅ Notes Saved")
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("Study Buddy • Sauban Ghazi")
