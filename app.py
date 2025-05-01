import streamlit as st
import pygetwindow as gw

from capture import capture_screen
from detector import detect_app_raw
from gemini_generator import ask_gemini
from utils import recognize_speech, generate_tts_audio, pil_to_base64

# Streamlit page configuration
st.set_page_config(
    page_title="HowToHelper",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🖥️ HowToHelper")
st.write("Capture your screen, pick a window, ask questions, and get step-by-step guidance.")

# 1️⃣ Capture Screenshot
if st.button("📸 Capture Screenshot"):
    img = capture_screen()
    st.session_state.img = img

    # Display the screenshot
    st.image(pil_to_base64(img), caption="Latest Screenshot", use_container_width=True)
    
    # Gather window titles
    all_windows = []
    for w in gw.getAllWindows():
        title = w.title.strip()
        if title and not getattr(w, "isMinimized", False):
            all_windows.append(title)

    st.session_state.window_list = all_windows

# 2️⃣ Select Target Window and Ask Question
if st.session_state.get("img") and st.session_state.get("window_list"):
    # Detect and display the raw active window title
    raw_title = detect_app_raw()
    st.info(f"🔎 OS reports active window title: `{raw_title}`")

    # Window selection
    choice = st.selectbox(
        "Select the application window you want help with:",
        st.session_state.window_list,
        index=st.session_state.window_list.index(raw_title) if raw_title in st.session_state.window_list else 0
    )
    st.session_state.selected_title = choice

    # User question input and speech
    st.markdown("### ❓ Ask your question")
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🎙️ Speak your question"):
            spoken = recognize_speech()
            if "⚠️" not in spoken:
                st.session_state.spoken_input = spoken
                preview_audio = generate_tts_audio("You said: " + spoken)
                st.audio(preview_audio, format="audio/mp3")
            else:
                st.warning(spoken)
    with col1:
        user_question = st.text_input(
            "Type your question here:",
            value=st.session_state.get("spoken_input", ""),
            key="text_input_question"
        )

    # Ask Gemini
    if user_question and st.button("🚀 Ask HowToHelper"):
        with st.spinner("🧠 Thinking..."):
            full_question = f"[App: {st.session_state.selected_title}] {user_question}"
            desc = f"Screenshot size: {st.session_state.img.size}"
            answer = ask_gemini(
                app=st.session_state.selected_title,
                question=full_question,
                screenshot_desc=desc
            )
        st.session_state.last_answer = answer

    # Display answer & play audio
    if st.session_state.get("last_answer"):
        st.markdown("### 🧠 Gemini says:")
        for line in st.session_state.last_answer.splitlines():
            st.write(line)

        if st.button("🔊 Play Response", key="play_btn"):
            st.session_state.play_audio = True

        if st.session_state.get("play_audio"):
            audio_bytes = generate_tts_audio(st.session_state.last_answer)
            st.audio(audio_bytes, format="audio/mp3")
