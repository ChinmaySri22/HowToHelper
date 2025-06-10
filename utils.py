#utils.py

import io
import base64
from PIL import Image
import speech_recognition as sr
from gtts import gTTS

def pil_to_base64(img: Image.Image) -> str:
    """Convert PIL image to a base64 data URI (used if needed elsewhere)."""
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    data = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{data}"

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # raise energy threshold and allow more calibration time
        r.energy_threshold = 400
        r.dynamic_energy_threshold = True
        r.adjust_for_ambient_noise(source, duration=2)  
        try:
            print("🎙️ Listening…")
            audio = r.listen(source, timeout=10, phrase_time_limit=7)
            print("🧠 Recognizing…")
            return r.recognize_google(audio)
        except sr.WaitTimeoutError:
            return "⚠️ No speech detected. Please try again."
        except sr.UnknownValueError:
            return "⚠️ Sorry, I couldn't understand that. (try speaking more clearly or closer to the mic)"
        except sr.RequestError:
            return "⚠️ Network error. Please check your connection."

def generate_tts_audio(text: str) -> bytes:
    """Generate MP3 audio from text using gTTS for browser playback in Streamlit."""
    tts = gTTS(text)
    mp3_buffer = io.BytesIO()
    tts.write_to_fp(mp3_buffer)
    mp3_buffer.seek(0)
    return mp3_buffer.read()
