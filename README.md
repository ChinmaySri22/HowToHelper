
# GenAI HowToHelper

GenAI HowToHelper is an AI-powered desktop assistant that captures your screen, detects the active app, and uses Google’s Gemini Pro LLM to provide contextual, step-by-step instructions. It simplifies software learning and task execution by giving personalized, real-time guidance — no web search needed!

## ✨ Features

- 📸 Captures your screen to understand current context
- 🪟 Detects the active app from window title
- 🧠 Integrates with **Gemini Pro** to generate app-specific instructions
- 🖥️ Simple Streamlit-based UI
- 🔤 Auto-augments user queries with app context for more accurate results

## 🚀 Demo Flow

1. Launch the app
2. Capture current screen
3. Detect active app (e.g. VS Code, Photoshop)
4. Enter a natural query: _"How to add a new file?"_
5. App sends: `[App: Visual Studio Code] How to add a new file?` to Gemini
6. Get back step-by-step instructions tailored to the detected app
7. Display results on-screen

## 🛠️ Tech Stack

| Component              | Technology / Library        |
|------------------------|-----------------------------|
| Frontend UI            | Streamlit                   |
| Screenshot Capture     | pyautogui                   |
| Active Window Title    | pygetwindow                 |
| LLM Integration        | Google Gemini Pro (google.generativeai) |
| Language               | Python                      |

## 🧑‍💻 Installation

### Prerequisites

- Python 3.8+
- Google API Key for Gemini Pro (`GOOGLE_API_KEY`)

### Clone this repo

```bash
git clone https://github.com/yourusername/GenAI-HowToHelper.git
cd GenAI-HowToHelper
```

### Create and activate a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Install dependencies

```bash
pip install -r requirements.txt
```

**Example `requirements.txt`:**

```txt
streamlit
pyautogui
pygetwindow
google-generativeai
pytesseract  # Optional (was used for earlier OCR attempts)
Pillow
```

### Setup your Gemini API key

Export your API key as an environment variable:

```bash
export GOOGLE_API_KEY='your-gemini-api-key'    # Linux/Mac
set GOOGLE_API_KEY=your-gemini-api-key         # Windows
```

Alternatively, create a `.env` file and load it in your app.

## ▶️ How to Run the Project

```bash
streamlit run app.py
```

This will open the app in your browser (default: `http://localhost:8501`).

## 📌 Project Structure

```
GenAI-HowToHelper/
├── app.py                # Main Streamlit app
├── requirements.txt      # Project dependencies
├── README.md             # Project README
└── screenshots/          # (Optional) saved screenshots
```

## 🤖 How It Works

- **Capture Screen** → Get a current screenshot using `pyautogui`.
- **Detect Active App** → Use `pygetwindow.getActiveWindow().title`.
- **Prompt Augmentation** → Prepend detected app name to user query.
- **LLM Call** → Send prompt to **Gemini Pro** using `google-generativeai`.
- **Display Instructions** → Show results in Streamlit app.

## 🌟 Future Improvements

- Better app detection using icons or image hashing.
- Manual screenshot upload support.
- Plugin system for app-specific modules.
- Multi-turn interaction with memory.
- Voice command integration.

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

**Built with ❤️ by Chinmay Srivastava**

---
