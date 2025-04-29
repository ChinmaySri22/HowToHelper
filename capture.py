import pyscreenshot as ImageGrab
from datetime import datetime

def capture_screen(save_path: str = None):
    """
    Grabs a full-screen screenshot. 
    If save_path is provided, writes a PNG there.
    Returns a PIL.Image.
    """
    img = ImageGrab.grab()
    if save_path:
        img.save(save_path)
    return img