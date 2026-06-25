import streamlit as st
import time

st.set_page_config(page_title="Study Buddy", page_icon="📚", layout="wide")

# ====================== OPENAI KEY CHECK ======================
if "OPENAI_API_KEY" in st.secrets:
    import openai
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    st.sidebar.success("✅ OpenAI Connected")
else:
    st.sidebar.error("❌ OpenAI API Key not found!")
    st.sidebar.info("Go to Settings → Secrets and add OPENAI_API_KEY")

# ====================== SIDEBAR ======================
st.sidebar.title("Study Buddy")
st.sidebar.caption("Dark Mature Theme • AI Hive")

page = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "⏱️ Pomodoro", "✅ Tasks", "💬 AI Study Buddy", "📝 Notes"]
)

# ====================== PAGES ======================
if page == "📊 Dashboard":
    st.title("Good evening, Student 👋")
    col1, col2, col3 = st.columns(3)
    col1.metric("Focus Time", "2h 45m")
    col2.metric("Tasks Done", "4")
    col3.metric("Streak", "8 days 🔥")

elif page == "⏱️ Pomodoro":
    st.title("⏱️ Pomodoro Timer")
    if 'time_left' not in st.session_state:
        st.session_state.time_left = 50 * 60
        st.session_state.is_running = False

    minutes, seconds = divmod(st.session_state.time_left, 60)
    st.markdown(f"<h1 style='text-align:center;font-size:5.5rem;font-family:monospace'>{minutes:02d}:{seconds:02d}</h1>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    if c1.button("Start", use_container_width=True):
        st.session_state.is_running = True
    if c2.button("Pause", use_container_width=True):
        st.session_state.is_running = False
    if c3.button("Reset", use_container_width=True):
        st.session_state.time_left = 50 * 60
        st.session_state.is_running = False

    if st.session_state.is_running and st.session_state.time_left > 0:
        time.sleep(1)
        st.session_state.time_left -= 1
        st.rerun()

elif page == "✅ Tasks":
    st.title("✅ Tasks")
    task = st.text_input("New Task")
    if st.button("Add Task"):
        if 'tasks' not in st.session_state:
            st.session_state.tasks = []
        st.session_state.tasks.append({"text": task, "done": False})

    if 'tasks' in st.session_state:
        for i, t in enumerate(st.session_state.tasks):
            col1, col2 = st.columns([4,1])
            st.session_state.tasks[i]["done"] = col1.checkbox(t["text"], t["done"], key=i)
            if col2.button("Delete", key=f"d{i}"):
                del st.session_state.tasks[i]
                st.rerun()

elif page == "💬 AI Study Buddy":
    st.title("💬 AI Study Buddy")
    st.caption("Your personal study assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi! How can I help you study today?"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask anything..."):
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
                    st.rerun()
                except:
                    st.error("API Error - Check your key in Secrets")

elif page == "📝 Notes":
    st.title("📝 Notes")
    notes = st.text_area("Write here...", height=400, value=st.session_state.get("notes", ""))
    if st.button("Save Notes"):
        st.session_state.notes = notes
        st.success("Notes Saved!")

st.sidebar.caption("Made for AI Hive")
