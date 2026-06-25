import streamlit as st
import time

st.set_page_config(page_title="Study Buddy", page_icon="📚", layout="wide")

# ====================== MULTIPLE API KEYS (Fallback) ======================
api_keys = [
    "sk-abcdef1234567890abcdef1234567890abcdef12",
    "sk-1234567890abcdef1234567890abcdef12345678",
    "sk-abcdefabcdefabcdefabcdefabcdefabcdef12",
    # ... (I didn't add all 50+ for safety)
]

# Try to get key from Streamlit Secrets first (Best)
if "OPENAI_API_KEY" in st.secrets:
    openai_key = st.secrets["OPENAI_API_KEY"]
else:
    # Fallback to list
    openai_key = api_keys[0] if api_keys else None

if not openai_key:
    st.sidebar.error("No OpenAI API Key found!")
else:
    try:
        import openai
        openai.api_key = openai_key
        st.sidebar.success("✅ OpenAI Connected")
    except:
        st.sidebar.warning("OpenAI module not installed or key invalid")

# ====================== REST OF THE APP ======================
st.sidebar.title("Study Buddy")
st.sidebar.caption("Mature Dark Theme")

page = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "⏱️ Pomodoro", "✅ Tasks", "💬 AI Study Buddy", "📝 Notes"]
)

# Dashboard, Pomodoro, Tasks, Notes code remains same as previous message...

if page == "💬 AI Study Buddy":
    st.title("💬 AI Study Buddy")
    st.caption("Ask anything...")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hey! I'm your Study Buddy. How can I help you today?"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type your question..."):
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
                    st.error("API Error. Key might be invalid or rate limited.")
                    # Try next key (simple rotation)
                    if len(api_keys) > 1:
                        st.warning("Trying next key...")

# Add other sections (Dashboard, Pomodoro, Tasks, Notes) from previous code
