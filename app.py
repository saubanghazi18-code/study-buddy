import streamlit as st
import time
from datetime import datetime
import openai

st.set_page_config(page_title="Study Buddy", page_icon="📚", layout="wide")

# Secure OpenAI Key
if "openai_key" not in st.secrets:
    st.warning("OpenAI API key not set. Add it in Streamlit Secrets.")
else:
    openai.api_key = st.secrets["OPENAI_API_KEY"]

# Sidebar Navigation
st.sidebar.title("Study Buddy")
page = st.sidebar.radio("Go to", ["Dashboard", "Pomodoro Timer", "Tasks", "AI Chat", "Notes"])

# Dashboard
if page == "Dashboard":
    st.title("Welcome back, Student 👋")
    col1, col2, col3 = st.columns(3)
    col1.metric("Focus Time Today", "2h 15m")
    col2.metric("Tasks Completed", "4")
    col3.metric("Streak", "7 days 🔥")

# Pomodoro Timer
elif page == "Pomodoro Timer":
    st.title("⏱️ Pomodoro Timer")
    
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
        st.session_state.time_left = 50 * 60  # 50 minutes

    col1, col2 = st.columns([2,1])
    
    with col1:
        minutes, seconds = divmod(st.session_state.time_left, 60)
        st.markdown(f"<h1 style='text-align: center; font-size: 5rem;'>{minutes:02d}:{seconds:02d}</h1>", unsafe_allow_html=True)
    
    if st.button("Start Focus Session", type="primary"):
        st.session_state.timer_running = True
        # Simple countdown logic (Streamlit reruns on interaction)

    if st.button("Pause"):
        st.session_state.timer_running = False

    if st.button("Reset"):
        st.session_state.time_left = 50 * 60
        st.session_state.timer_running = False

# Tasks
elif page == "Tasks":
    st.title("✅ Tasks")
    task = st.text_input("New Task")
    if st.button("Add Task"):
        if 'tasks' not in st.session_state:
            st.session_state.tasks = []
        st.session_state.tasks.append({"task": task, "done": False})
    
    if 'tasks' in st.session_state:
        for i, t in enumerate(st.session_state.tasks):
            col1, col2 = st.columns([4,1])
            col1.checkbox(t["task"], value=t["done"], key=i)
            if col2.button("Delete", key=f"del{i}"):
                del st.session_state.tasks[i]

# AI Chat
elif page == "AI Chat":
    st.title("💬 Study Buddy AI")
    st.caption("Ask anything — math, science, motivation, summaries...")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm your Study Buddy. How can I help you focus today?"}]

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
                    response = openai.ChatCompletion.create(
                        model="gpt-4o-mini",
                        messages=st.session_state.messages
                    )
                    reply = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.markdown(reply)
                except Exception as e:
                    st.error("Make sure your OpenAI key is set correctly.")

# Notes
elif page == "Notes":
    st.title("📝 Quick Notes")
    notes = st.text_area("Write your notes here", height=400)
    if st.button("Save Notes"):
        st.success("Notes saved! (In full version we can save to file or database)")

# Footer
st.sidebar.caption("Made with ❤️ for AI Hive")
