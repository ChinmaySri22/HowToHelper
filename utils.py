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
    """Capture voice and return transcribed text using Google STT."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Say something...")
        r.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=5)
            print("🧠 Recognizing...")
            text = r.recognize_google(audio)
            return text

        except sr.WaitTimeoutError:
            return "⚠️ No speech detected. Please try again."
        except sr.UnknownValueError:
            return "⚠️ Sorry, I couldn't understand that."
        except sr.RequestError:
            return "⚠️ Network error. Please check your connection."

def generate_tts_audio(text: str) -> bytes:
    """Generate MP3 audio from text using gTTS for browser playback in Streamlit."""
    tts = gTTS(text)
    mp3_buffer = io.BytesIO()
    tts.write_to_fp(mp3_buffer)
    mp3_buffer.seek(0)
    return mp3_buffer.read()
