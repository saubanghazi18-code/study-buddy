import streamlit as st
import time
from datetime import datetime

st.set_page_config(page_title="Study Buddy", page_icon="📚", layout="wide")

# ====================== OPENAI API KEY SETUP ======================
if "openai_key" not in st.secrets:
    st.sidebar.error("⚠️ OpenAI API Key not set. Add it in Streamlit Secrets.")
    st.sidebar.info("Go to: Settings → Secrets → Add OPENAI_API_KEY")
else:
    import openai
    openai.api_key = st.secrets["OPENAI_API_KEY"]

# ====================== SIDEBAR ======================
st.sidebar.title("Study Buddy")
st.sidebar.caption("Mature Dark Theme • AI Hive Project")

page = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "⏱️ Pomodoro", "✅ Tasks", "💬 AI Study Buddy", "📝 Notes"]
)

# ====================== MAIN CONTENT ======================
if page == "📊 Dashboard":
    st.title("Good evening, Student 👋")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Focus", "50:00", "Focus Mode")
    col2.metric("Tasks Today", "3 / 5")
    col3.metric("Study Streak", "7 days 🔥")

elif page == "⏱️ Pomodoro":
    st.title("⏱️ Pomodoro Timer")
    
    if 'time_left' not in st.session_state:
        st.session_state.time_left = 50 * 60
        st.session_state.is_running = False
        st.session_state.is_break = False

    # Timer Display
    minutes, seconds = divmod(st.session_state.time_left, 60)
    st.markdown(f"""
        <h1 style='text-align: center; font-size: 6rem; font-family: monospace;'>
            {minutes:02d}:{seconds:02d}
        </h1>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    if col1.button("▶️ Start", use_container_width=True):
        st.session_state.is_running = True
    if col2.button("⏸️ Pause", use_container_width=True):
        st.session_state.is_running = False
    if col3.button("🔄 Reset", use_container_width=True):
        st.session_state.time_left = 50 * 60
        st.session_state.is_running = False

    # Simple countdown simulation
    if st.session_state.is_running and st.session_state.time_left > 0:
        time.sleep(1)
        st.session_state.time_left -= 1
        st.rerun()

    if st.session_state.time_left <= 0:
        st.success("Time's up! Take a break." if not st.session_state.is_break else "Break over! Back to focus.")
        st.session_state.is_running = False

elif page == "✅ Tasks":
    st.title("✅ Tasks")
    
    # Add new task
    task_input = st.text_input("Add new task")
    if st.button("Add Task"):
        if 'tasks' not in st.session_state:
            st.session_state.tasks = []
        if task_input:
            st.session_state.tasks.append({"text": task_input, "done": False})

    # Show tasks
    if 'tasks' in st.session_state:
        for i, task in enumerate(st.session_state.tasks):
            col1, col2 = st.columns([4, 1])
            done = col1.checkbox(task["text"], value=task["done"], key=f"task_{i}")
            st.session_state.tasks[i]["done"] = done
            if col2.button("Delete", key=f"del_{i}"):
                del st.session_state.tasks[i]
                st.rerun()

elif page == "💬 AI Study Buddy":
    st.title("💬 AI Study Buddy")
    st.caption("Ask anything — explanations, quizzes, summaries, motivation")

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hey! I'm your Study Buddy. How can I help you stay focused today?"}
        ]

    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Type your question here..."):
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
                    st.error("Error: Make sure your OpenAI key is correctly added in Secrets.")

elif page == "📝 Notes":
    st.title("📝 Quick Notes")
    notes = st.text_area("Write your study notes here...", height=500, value=st.session_state.get("notes", ""))
    
    if st.button("💾 Save Notes"):
        st.session_state.notes = notes
        st.success("Notes saved successfully!")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Built for AI Hive • Dark Mature Theme")
