
# Med Scheduler

This project integrates a hospital appointment scheduling system using an LLM API (OpenAI) with voice functionality for users. The system allows users to interact via chat or voice to schedule or cancel appointments.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Execution](#execution)
4. [Linux Setup](#linux-setup)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Ensure that you have the following tools installed on your system:

- Python 3.12+ (recommended)
- `pip` package manager
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- `pyttsx3` (for voice integration)
- `requests` (to send requests to the FastAPI backend)
- `gTTS` or `espeak` (if you choose to use Google or eSpeak for text-to-speech functionality)
- `mpg321` or similar audio player (to play audio on Linux)

---

## Installation Steps

### 1. Clone the repository

```bash
git clone https://github.com/Jacobgokul/Med-Scheduler.git
cd Med-Scheduler
```

### 2. Set up a virtual environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
```

### 3. Install required dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the environment variables

Create a `.env` file in the project root directory and include your OpenAI API key:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Install additional packages for text-to-speech

To use voice functionality, install either `pyttsx3` (for eSpeak) or `gTTS` (Google Text-to-Speech):

#### For `pyttsx3` (eSpeak)

```bash
sudo apt install espeak
pip install pyttsx3
```

---

## Execution

### 1. Start the FastAPI backend

The backend handles the logic for appointment scheduling. Run it using `uvicorn`:

```bash
uvicorn backend:app --reload
```

This will start the server locally at `http://127.0.0.1:8000`.

### 2. Run the Streamlit frontend

Once the backend is running, open another terminal and run the Streamlit app:

```bash
streamlit run app.py
```

This will open the app in your browser, allowing you to interact with the appointment scheduler via chat or voice.

---

## Linux Setup

To ensure the system works smoothly on Linux, follow these additional steps:

1. **Install required dependencies**:

   Ensure that all necessary libraries for text-to-speech and audio playback are installed:

   ```bash
   sudo apt install espeak
   ```