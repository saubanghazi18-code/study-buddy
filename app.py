import streamlit as st
import time

st.set_page_config(page_title="Study Buddy", layout="wide", initial_sidebar_state="collapsed")

# ==================== PREMIUM DARK THEME ====================
st.markdown("""
<style>
    .stApp {
        background-color: #050505;
        color: #e0e0e0;
    }
    h1, h2, h3, .stSubheader {
        color: #a5f3fc;
    }
    .big-timer {
        font-size: 7.2rem;
        font-weight: 700;
        font-family: 'Courier New', monospace;
        text-align: center;
        color: #67e8f9;
        text-shadow: 0 0 20px rgba(103, 232, 249, 0.3);
    }
    .stButton>button {
        background-color: #1f2937;
        color: #e0f2fe;
        border: 1px solid #334155;
    }
    .stButton>button:hover {
        background-color: #334155;
        border-color: #67e8f9;
    }
    .stButton>button[kind="primary"] {
        background-color: #22d3ee;
        color: #0f172a;
    }
    .chat-container {
        background-color: #0f172a;
        border-radius: 16px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <h1 style='text-align:center; font-size: 3rem; margin: 0.5rem 0 0.2rem 0; letter-spacing: -1px;'>
        Study Buddy
    </h1>
    <p style='text-align:center; color:#64748b; font-size:1.1rem; margin-bottom:1.5rem;'>
        Deep focus. Real results.
    </p>
""", unsafe_allow_html=True)

st.markdown("---")

# Main Layout
col1, col2 = st.columns([1.1, 1.9])

# LEFT - Timer + Tasks
with col1:
    st.subheader("⏱️ Focus Session")
    
    if 'time_left' not in st.session_state:
        st.session_state.time_left = 50 * 60
        st.session_state.is_running = False

    minutes, seconds = divmod(st.session_state.time_left, 60)
    st.markdown(f"<div class='big-timer'>{minutes:02d}:{seconds:02d}</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    if c1.button("▶️ Start Focus", use_container_width=True, type="primary"):
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

    if st.session_state.time_left <= 0:
        st.success("Session Complete → Take 10 min break")

    # Tasks
    st.subheader("✅ Tasks")
    task = st.text_input("New Task", placeholder="What will you crush today?")
    if st.button("Add Task", use_container_width=True):
        if 'tasks' not in st.session_state:
            st.session_state.tasks = []
        if task.strip():
            st.session_state.tasks.append({"text": task, "done": False})
            st.rerun()

    if 'tasks' in st.session_state:
        for i, t in enumerate(st.session_state.tasks):
            col_a, col_b = st.columns([4.5, 0.5])
            st.session_state.tasks[i]["done"] = col_a.checkbox(t["text"], t["done"], key=f"cb{i}")
            if col_b.button("×", key=f"del{i}"):
                del st.session_state.tasks[i]
                st.rerun()

# RIGHT - AI + Notes
with col2:
    st.subheader("💬 AI Study Companion")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "I'm here to help you stay focused. What are we studying today?"}]

    chat_area = st.container(height=420)
    with chat_area:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    import openai
                    openai.api_key = st.secrets["OPENAI_API_KEY"]
                    response = openai.ChatCompletion.create(
                        model="gpt-4o-mini",
                        messages=st.session_state.messages
                    )
                    reply = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.rerun()
                except:
                    st.error("OpenAI Error - Check Secrets")

    st.subheader("📝 Quick Notes")
    notes = st.text_area("Write important points here...", height=160, value=st.session_state.get("notes", ""))
    if st.button("Save Notes", use_container_width=True):
        st.session_state.notes = notes
        st.toast("✅ Notes Saved", icon="💾")

st.caption("Study Buddy • AI Hive Project by Sauban Ghazi")
