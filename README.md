# 🌿 OutsideQuest

### The world is the interface.

**OutsideQuest** is a local-AI-powered outdoor discovery application that encourages people to put their phones away and explore the world through guided observation missions.

Instead of scrolling, users investigate sounds, light and shadows, urban nature, and overlooked details in their surroundings.

## ✨ Features

- **AI-generated missions:** Create outdoor investigations based on the selected mission type, environment, and available time.
- **Local AI:** Generate missions using Ollama and the `qwen3.5:4b` model.
- **Discovery journal:** Record observations and save field notes locally in `discoveries.json`.
- **Follow-up investigations:** Turn a field observation into new hypotheses and a follow-up experiment.
- **Safety-focused guidance:** Encourage direct observation without requiring special equipment or photography.

## 🛠️ Tech Stack

- Python
- Streamlit
- Ollama
- Qwen 3.5 4B
- Requests
- JSON for local field-note storage

## ⚙️ Prerequisites

- Python installed on your computer
- [Ollama](https://ollama.com/) installed and running
- The `qwen3.5:4b` model downloaded

## 🚀 Run Locally

**1. Clone the repository**

```bash
git clone https://github.com/pratyushmishra9920-ship-it/outsidequest-ai.git
cd outsidequest-ai
```

**2. Create and activate a virtual environment**

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**3. Install dependencies**

```powershell
python -m pip install streamlit requests
```

**4. Download the model**

```powershell
ollama pull qwen3.5:4b
```

Ensure Ollama is running before starting the application.

**5. Start OutsideQuest**

```powershell
python -m streamlit run app.py
```

Open the local URL shown in your terminal, usually `http://localhost:8501`.

## 📝 Field Notes

Observations are saved locally in `discoveries.json` on the computer running the application. They are not automatically uploaded to a cloud database.

## 🌱 Vision

OutsideQuest aims to turn everyday outdoor experiences into small investigations that build curiosity, observation skills, and evidence-based thinking.

---

*OutsideQuest — Local AI, real-world curiosity.*