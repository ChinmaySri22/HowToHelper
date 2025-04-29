import io
import base64
from PIL import Image

def pil_to_base64(img: Image.Image) -> str:
    """Convert PIL image to a base64 data URI for Streamlit display."""
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    data = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{data}"
