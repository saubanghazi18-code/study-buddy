import streamlit as st
import time

st.set_page_config(page_title="Study Buddy", layout="wide", initial_sidebar_state="collapsed")

# Dark Mature Theme
st.markdown("""
<style>
    .stApp {
        background-color: #0a0a0a;
        color: #e5e5e5;
    }
    h1, h2, h3 {
        color: #67e8f9;
    }
    .big-timer {
        font-size: 7rem;
        font-weight: bold;
        font-family: monospace;
        text-align: center;
        color: #67e8f9;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align:center; margin-bottom:0;'>Study Buddy</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>Your focused AI study companion</p>", unsafe_allow_html=True)
st.markdown("---")

# Main Layout
col1, col2 = st.columns([1, 1.8])

# Left Column - Timer + Tasks
with col1:
    # Pomodoro Timer
    st.subheader("⏱️ Focus Timer")
    
    if 'time_left' not in st.session_state:
        st.session_state.time_left = 50 * 60
        st.session_state.is_running = False

    minutes, seconds = divmod(st.session_state.time_left, 60)
    st.markdown(f"<div class='big-timer'>{minutes:02d}:{seconds:02d}</div>", unsafe_allow_html=True)

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

    if st.session_state.time_left <= 0:
        st.success("Session Complete! Take a short break.")

    # Tasks
    st.subheader("✅ Tasks")
    task = st.text_input("New Task", placeholder="What do you want to accomplish?")
    if st.button("Add Task", use_container_width=True):
        if 'tasks' not in st.session_state:
            st.session_state.tasks = []
        if task:
            st.session_state.tasks.append({"text": task, "done": False})

    if 'tasks' in st.session_state:
        for i, t in enumerate(st.session_state.tasks[:]):
            col_a, col_b = st.columns([4,1])
            done = col_a.checkbox(t["text"], t["done"], key=f"cb{i}")
            st.session_state.tasks[i]["done"] = done
            if col_b.button("🗑️", key=f"del{i}"):
                del st.session_state.tasks[i]
                st.rerun()

# Right Column - AI Chat + Notes
with col2:
    st.subheader("💬 Talk to Study Buddy AI")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm your Study Buddy. What are we working on today?"}]

    chat_area = st.container(height=380)
    with chat_area:
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
                    response = openai.ChatCompletion.create(
                        model="gpt-4o-mini",
                        messages=st.session_state.messages
                    )
                    reply = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.rerun()
                except:
                    st.error("Check your OpenAI key in Secrets")

    # Quick Notes
    st.subheader("📝 Quick Notes")
    notes = st.text_area("", height=180, placeholder="Write important points, formulas, etc.", value=st.session_state.get("notes", ""))
    if st.button("Save Notes"):
        st.session_state.notes = notes
        st.toast("Notes saved ✅")

st.caption("Study Buddy • Built by Sauban Ghazi")
