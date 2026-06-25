import streamlit as st
import time

st.set_page_config(page_title="Study Buddy", page_icon="📚", layout="wide")

# OpenAI Key Check
if "OPENAI_API_KEY" in st.secrets:
    import openai
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    st.success("✅ AI Connected", icon="🔗")
else:
    st.warning("OpenAI key not found in Secrets", icon="⚠️")

# ====================== HEADER ======================
st.markdown("""
    <h1 style='text-align: center; color: #67e8f9; font-size: 2.8rem; margin-bottom: 0.5rem;'>
        Study Buddy
    </h1>
    <p style='text-align: center; color: #a1a1aa;'>Stay focused • Dark Mode</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ====================== LAYOUT ======================
col_left, col_center, col_right = st.columns([1.2, 1.8, 1.2])

# ================= LEFT COLUMN - TASKS =================
with col_left:
    st.subheader("✅ Today's Tasks")
    
    if 'tasks' not in st.session_state:
        st.session_state.tasks = [
            {"text": "Complete Math Chapter 5", "done": False},
            {"text": "Revise Physics Notes", "done": False}
        ]

    task_input = st.text_input("Add new task", placeholder="e.g. Solve 10 questions")
    if st.button("Add", use_container_width=True):
        if task_input:
            st.session_state.tasks.append({"text": task_input, "done": False})
            st.rerun()

    for i, task in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([4,1])
        st.session_state.tasks[i]["done"] = col1.checkbox(task["text"], task["done"], key=f"task{i}")
        if col2.button("🗑️", key=f"del{i}"):
            del st.session_state.tasks[i]
            st.rerun()

# ================= CENTER COLUMN - POMODORO =================
with col_center:
    st.subheader("⏱️ Pomodoro Timer")
    
    if 'time_left' not in st.session_state:
        st.session_state.time_left = 50 * 60
        st.session_state.is_running = False

    # Big Timer Display
    minutes, seconds = divmod(st.session_state.time_left, 60)
    st.markdown(f"""
        <div style='text-align: center; font-size: 6.5rem; font-family: monospace; font-weight: bold; color: #67e8f9;'>
            {minutes:02d}:{seconds:02d}
        </div>
    """, unsafe_allow_html=True)

    # Buttons
    btn1, btn2, btn3 = st.columns(3)
    if btn1.button("▶️ Start", use_container_width=True, type="primary"):
        st.session_state.is_running = True
    if btn2.button("⏸️ Pause", use_container_width=True):
        st.session_state.is_running = False
    if btn3.button("🔄 Reset", use_container_width=True):
        st.session_state.time_left = 50 * 60
        st.session_state.is_running = False

    # Timer Logic
    if st.session_state.is_running and st.session_state.time_left > 0:
        time.sleep(1)
        st.session_state.time_left -= 1
        st.rerun()

    if st.session_state.time_left <= 0:
        st.success("🎉 Session Complete! Take a 10 min break.")
        st.session_state.is_running = False

# ================= RIGHT COLUMN - AI CHAT =================
with col_right:
    st.subheader("💬 Study Buddy AI")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! How can I help you study better today?"}
        ]

    chat_container = st.container(height=420)

    with chat_container:
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
                    st.error("AI Error - Check your API key in Secrets")

# ====================== NOTES SECTION (Bottom) ======================
st.markdown("---")
st.subheader("📝 Quick Notes")
notes = st.text_area("Write your notes here...", height=180, value=st.session_state.get("notes", ""))
if st.button("💾 Save Notes"):
    st.session_state.notes = notes
    st.success("Notes Saved!")

st.caption("Made for AI Hive • Study Buddy")
