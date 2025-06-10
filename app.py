import os
import streamlit as st
import pygetwindow as gw

from capture import capture_screen
from detector import detect_app_raw, extract_text_from_image
from gemini_generator import ask_gemini
from utils import recognize_speech, generate_tts_audio, pil_to_base64

# Load .env (for GEMINI_API_KEY & FINE_TUNED_MODEL)
from dotenv import load_dotenv
load_dotenv()

# Streamlit page configuration
st.set_page_config(
    page_title="HowToHelper",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🖥️ HowToHelper")
st.write("Capture your screen, pick a window, ask questions, and get step-by-step guidance.")

# ─────────── Screenshot & OCR ───────────
if st.button("📸 Capture Screenshot"):
    img = capture_screen()
    st.session_state.img = img

    # Display the screenshot
    st.image(pil_to_base64(img), caption="Latest Screenshot", use_container_width=True)
    
    # Gather window titles
    all_windows = [
        w.title.strip()
        for w in gw.getAllWindows()
        if w.title.strip() and not getattr(w, "isMinimized", False)
    ]
    st.session_state.window_list = all_windows

    # OCR extraction and save
    ocr_output_dir = "outputs"
    os.makedirs(ocr_output_dir, exist_ok=True)
    ocr_path = os.path.join(ocr_output_dir, "latest_screenshot_text.txt")

    extracted_text = extract_text_from_image(img, out_path=ocr_path)
    st.success(f"OCR text extracted and saved to `{ocr_path}`")

    # Display a snippet
    st.markdown("**📄 Extracted text preview:**")
    st.code(extracted_text[:500] + ("..." if len(extracted_text) > 500 else ""))

# ─────────── Question & Answer ───────────
if st.session_state.get("img") and st.session_state.get("window_list"):
    # Show raw active window
    raw_title = detect_app_raw()
    st.info(f"🔎 OS reports active window title: `{raw_title}`")

    # Let user pick which window
    choice = st.selectbox(
        "Select the application window you want help with:",
        st.session_state.window_list,
        index=st.session_state.window_list.index(raw_title)
              if raw_title in st.session_state.window_list else 0
    )
    st.session_state.selected_title = choice

    # Speech‑to‑text
    st.markdown("### ❓ Ask your question")
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🎙️ Speak", key="mic"):
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
            key="text_input"
        )

    # Ask the (fine‑tuned) model
    if user_question and st.button("🚀 Ask HowToHelper"):
        with st.spinner("🧠 Thinking..."):
            full_q = f"[App: {st.session_state.selected_title}] {user_question}"
            desc   = f"Screenshot size: {st.session_state.img.size}"
            answer = ask_gemini(
                app=st.session_state.selected_title,
                question=full_q,
                screenshot_desc=desc
            )
        st.session_state.last_answer = answer

    # Show answer & TTS
    if st.session_state.get("last_answer"):
        st.markdown("### 🧠 Gemini says:")
        for line in st.session_state.last_answer.splitlines():
            st.write(line)

        if st.button("🔊 Play Response", key="play_btn"):
            audio_bytes = generate_tts_audio(st.session_state.last_answer)
            st.audio(audio_bytes, format="audio/mp3")
