import pygetwindow as gw
import pytesseract
import cv2
import numpy as np
from PIL import Image

# ——— Known apps for title keyword matching ————————————————
KNOWN_APPS = {
    "vscode":      ["visual studio code", "vs code", "vscode"],
    "chrome":      ["google chrome", "chrome"],
    "word":        ["microsoft word", ".docx", "word"],
    "excel":       ["microsoft excel", ".xlsx", "excel"],
    "powerpoint":  ["powerpoint", ".pptx"],
    "notepad":     ["notepad"],
    "terminal":    ["powershell", "cmd", "terminal", "bash"],
    # …add any other apps you want to support…
}

def detect_app_raw() -> str:
    """
    Returns the exact title of the currently active window,
    as reported by the OS. If it fails, returns an empty string.
    """
    try:
        win = gw.getActiveWindow()
        return win.title or ""
    except Exception:
        return ""

def detect_app() -> str:
    """
    Maps the raw active-window title to one of our KNOWN_APPS keys.
    Returns the matching key (e.g. "vscode") or "unknown" if no match.
    """
    raw = detect_app_raw().lower()
    for app_key, keywords in KNOWN_APPS.items():
        for kw in keywords:
            if kw in raw:
                return app_key
    return "unknown"

import os

def extract_text_from_image(pil_image: Image.Image, out_path: str = None) -> str:
    """
    Uses Tesseract OCR to extract all visible text from a PIL screenshot.
    If out_path is given, also saves the result to that file.
    Returns the extracted text string.
    """
    # Convert PIL -> BGR OpenCV image
    np_img = np.array(pil_image.convert("RGB"))
    bgr   = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)

    # Preprocess to grayscale
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    # (You could add thresholding/denoise here)

    # Run Tesseract OCR
    text = pytesseract.image_to_string(gray, lang="eng").strip()

    # If an output path was provided, write to disk
    if out_path:
        # Ensure directory exists
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)

    return text
