# detector.py

import pygetwindow as gw

# 1) Define your known applications and their title‐keywords
KNOWN_APPS = {
    "vscode": ["visual studio code", "vs code", "vscode"],
    "chrome": ["google chrome", "chrome"],
    "word": ["microsoft word", ".docx", "word"],
    "excel": ["microsoft excel", ".xlsx", "excel"],
    "powerpoint": ["powerpoint", ".pptx"],
    "notepad": ["notepad"],
    "terminal": ["powershell", "cmd", "terminal", "bash"],
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
    Uses detect_app_raw() to look up which KNOWN_APPS key
    matches the active window title. Returns the key (e.g. "vscode")
    or "unknown" if no match is found.
    """
    raw_title = detect_app_raw().lower()

    for app_key, keywords in KNOWN_APPS.items():
        for kw in keywords:
            if kw in raw_title:
                return app_key

    return "unknown"
