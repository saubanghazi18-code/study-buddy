import streamlit as st
import time

st.set_page_config(page_title="Study Buddy", layout="wide")

# Attractive Dark Theme + Background
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
    }
    .main-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid #334155;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(103, 232, 249, 0.1);
    }
    .timer-text {
        font-size: 6.5rem;
        font-weight: 700;
        font-family: monospace;
        color: #67e8f9;
        text-shadow: 0 0 30px rgba(103, 232, 249, 0.6);
    }
    .section-title {
        color: #a5f3fc;
        font-size: 1.8rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align:center; font-size:3.2rem; background: linear-gradient(to right, #67e8f9, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Study Buddy</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8; font-size:1.3rem;'>Your focused AI companion</p>", unsafe_allow_html=True)
st.markdown("---")

# Main Layout
col1, col2 = st.columns([1.1, 1.9])

with col1:
    # Timer
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("<p class='section-title'>⏱️ Focus Timer</p>", unsafe_allow_html=True)
    
    if 'time_left' not in st.session_state:
        st.session_state.time_left = 50 * 60
        st.session_state.is_running = False

    minutes, seconds = divmod(st.session_state.time_left, 60)
    st.markdown(f"<div class='timer-text text-center'>{minutes:02d}:{seconds:02d}</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    if c1.button("▶️ Start", use_container_width=True, type="primary"):
        st.session_state.is_running = True
    if c2.button("⏸️ Pause", use_container_width=True):
        st.session_state.is_running = False
    if c3.button("🔄 Reset", use_container_width=True):
        st.session_state.time_left = 50 * 60
        st.session_state.is_running = False

    if st.session_state.is_running and st.session_state.time_left > 0:
        time.sleep(1)
        st.session_state.time_left -= 1
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Tasks
    st.markdown("<div class='main-card mt-6'>", unsafe_allow_html=True)
    st.markdown("<p class='section-title'>✅ Tasks</p>", unsafe_allow_html=True)
    
    task = st.text_input("New Task", placeholder="What will you complete?")
    if st.button("Add Task", use_container_width=True):
        if 'tasks' not in st.session_state:
            st.session_state.tasks = []
        if task:
            st.session_state.tasks.append({"text": task, "done": False})

    if 'tasks' in st.session_state:
        for i, t in enumerate(st.session_state.tasks):
            col_a, col_b = st.columns([4,1])
            st.session_state.tasks[i]["done"] = col_a.checkbox(t["text"], t["done"], key=f"task{i}")
            if col_b.button("Delete", key=f"del{i}"):
                del st.session_state.tasks[i]
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    # AI Chat
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("<p class='section-title'>💬 AI Study Companion</p>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi! Ready to study? Ask me anything."}]

    chat_container = st.container(height=380)
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if prompt := st.chat_input("Ask for explanation, quiz, motivation..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    import openai
                    openai.api_key = st.secrets["OPENAI_API_KEY"]
                    response = openai.ChatCompletion.create(model="gpt-4o-mini", messages=st.session_state.messages)
                    reply = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.rerun()
                except:
                    st.error("Check your API key in Secrets")
    st.markdown("</div>", unsafe_allow_html=True)

    # Notes
    st.markdown("<div class='main-card mt-6'>", unsafe_allow_html=True)
    st.markdown("<p class='section-title'>📝 Quick Notes</p>", unsafe_allow_html=True)
    notes = st.text_area("Write here...", height=180, value=st.session_state.get("notes", ""))
    if st.button("Save Notes", use_container_width=True):
        st.session_state.notes = notes
        st.success("Notes saved!")
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("Study Buddy • AI Hive Project")
