# app.py

import streamlit as st
import pygetwindow as gw

from capture import capture_screen
from detector import detect_app_raw
from gemini_generator import ask_gemini
from utils import pil_to_base64

st.set_page_config(
    page_title="GenAI HowToHelper",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🖥️ GenAI HowToHelper")
st.write("Capture your screen, pick a window, ask questions, and get step-by-step guidance.")

# 1️⃣ Capture screenshot
if st.button("📸 Capture Screenshot"):
    img = capture_screen()
    st.session_state.img = img

    st.image(pil_to_base64(img), caption="Latest Screenshot", use_container_width=True)

    # 2️⃣ Gather all non-empty, non-minimized window titles
    all_windows = []
    for w in gw.getAllWindows():
        title = w.title.strip()
        if not title:
            continue
        # skip minimized windows if supported
        if getattr(w, "isMinimized", False):
            continue
        all_windows.append(title)

    st.session_state.window_list = all_windows

# 3️⃣ Once screenshot + list exist, let user pick the target window
if st.session_state.get("img") and st.session_state.get("window_list"):
    raw_title = detect_app_raw()
    st.info(f"🔎 OS reports active window title (focus may still be HowToHelper): `{raw_title}`")

    choice = st.selectbox(
        "Select the application window you want help with:",
        st.session_state.window_list,
        index=st.session_state.window_list.index(raw_title)
              if raw_title in st.session_state.window_list else 0
    )
    st.session_state.selected_title = choice

    # 4️⃣ Ask a question, prepending the selected window title
    question = st.text_input("❓ What would you like to do?", "")
    if question and st.button("🚀 Ask HowToHelper"):
        with st.spinner("🧠 Thinking..."):
            full_question = f"[App: {st.session_state.selected_title}] {question}"
            desc = f"Screenshot size: {st.session_state.img.size}"
            answer = ask_gemini(
                app=None,
                question=full_question,
                screenshot_desc=desc
            )

        st.markdown("**Answer:**")
        for line in answer.splitlines():
            st.write(line)
