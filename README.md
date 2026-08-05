# 🎥 VideoMate – AI-Powered Meeting Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live_App-FF4B4B.svg)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-LCEL-success.svg)](https://www.langchain.com/)
[![Whisper](https://img.shields.io/badge/OpenAI-Whisper-black.svg)](https://github.com/openai/whisper)
[![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-000000.svg)](https://ollama.com/)
[![Groq](https://img.shields.io/badge/Groq-Cloud_LLM-f55036.svg)](https://groq.com/)

## 🌐 Live Demo

**https://videomate.streamlit.app/**

## 📖 Overview

VideoMate is an AI-powered meeting assistant that transforms lengthy meetings, recorded lectures, podcasts, and YouTube videos into structured, actionable insights.

Simply upload a meeting recording or paste a YouTube URL, and VideoMate will automatically:

- 🎙️ Transcribe speech into text
- 📝 Generate concise meeting summaries
- 🏷️ Create an intelligent meeting title
- ✅ Extract action items
- 📌 Identify key decisions
- ❓ Find unanswered questions
- 💬 Allow semantic chat with the meeting using Retrieval-Augmented Generation (RAG)

Designed with a modular AI pipeline, VideoMate supports both **cloud-hosted LLMs (Groq)** and **local LLMs (Ollama)** for flexible development and deployment.


# ✨ Features

## 🎙️ Speech-to-Text

- OpenAI Whisper (Offline)
- Hindi/Hinglish transcription support
- Automatic English translation
- Audio chunking for long recordings
- YouTube audio extraction


## 📝 AI Meeting Summary

- Map-Reduce summarization pipeline
- Handles transcripts longer than LLM context windows
- Generates structured meeting notes


## 🏷️ Automatic Meeting Title

Generate a concise, professional meeting title based on transcript content.


## ✅ Action Item Extraction

Automatically extracts:

- Task Description
- Responsible Owner
- Deadline (if mentioned)


## 📌 Key Decision Extraction

Detects important decisions made during the meeting.


## ❓ Open Question Detection

Finds:

- Unanswered questions
- Follow-up topics
- Pending discussions


## 💬 Meeting Chat (RAG)

Ask questions such as:

> What deadline did John mention?

> Who is responsible for deployment?

> Summarize the discussion around authentication.

VideoMate retrieves only the relevant transcript chunks before generating an answer.


## 📥 Input Sources

Supports:

- 🎥 YouTube URLs
- 🎧 MP3
- 🎬 MP4
- 🎙️ WAV
- Local Audio Files
- Local Video Files


## 📤 Output

VideoMate generates:

- Meeting Title
- Complete Transcript
- AI Summary
- Action Items
- Key Decisions
- Open Questions
- Interactive RAG Chat


# 🛠 Tech Stack

## AI & LLM

- LangChain (LCEL)
- Groq
- Ollama


## Speech Processing

- OpenAI Whisper
- Sarvam AI


## Retrieval-Augmented Generation

- ChromaDB
- HuggingFace Embeddings
- Sentence Transformers


## Backend

- Python


## Media Processing

- yt-dlp
- FFmpeg
- pydub


## User Interface

- Streamlit


# 🏗 Project Architecture

```text
                Video / YouTube URL
                        │
                        ▼
             Download & Audio Extraction
                        │
                        ▼
                 Audio Chunking
                        │
        ┌───────────────┴────────────────┐
        │                                │
        ▼                                ▼
 Whisper (English)          Sarvam AI (Hindi/Hinglish)
        │                                │
        └───────────────┬────────────────┘
                        ▼
                 Full Transcript
                        │
        ┌───────────────┼──────────────────┐
        ▼               ▼                  ▼
     Summary      Information         Vector Store
                  Extraction               │
                        │                  ▼
                        │              ChromaDB
                        │                  │
                        ▼                  ▼
      Title • Action Items •        Similarity Search
      Decisions • Questions              │
                                         ▼
                                   Relevant Context
                                         │
                                         ▼
                                     LLM Response
```


# 📂 Project Structure

```text
VideoMate
│
├── app.py
├── main.py
├── test.py
├── requirements.txt
├── packages.txt
│
├── core
│   ├── extractor.py
│   ├── rag_engine.py
│   ├── summarizer.py
│   ├── transcriber.py
│   └── vector_store.py
│
├── utils
│   └── audio_processor.py
│
└── README.md
```


# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/VideoMate.git

cd VideoMate
```


## Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```


# 📦 Install Dependencies

Install all project dependencies.

```bash
pip install -r requirements.txt
```


# 🤖 LLM Providers

VideoMate supports two LLM providers.

## Option 1 — Groq (Recommended for Deployment)

```env
LLM_PROVIDER=groq

GROQ_API_KEY=your_api_key
```


## Option 2 — Ollama (Recommended for Local Development)

Install Ollama:

https://ollama.com

Pull a model:

```bash
ollama pull llama3.2:3b
```

Start the server:

```bash
ollama serve
```

Then configure:

```env
LLM_PROVIDER=ollama

OLLAMA_MODEL=llama3.2:3b
```

You may replace the model with any locally available Ollama model.

Example:

```env
OLLAMA_MODEL=qwen3:8b
```


# 🔑 Environment Variables

Create a `.env` file.

```env
# LLM Provider
LLM_PROVIDER=groq

# Groq
GROQ_API_KEY=

# Ollama
OLLAMA_MODEL=llama3.2:3b

# Sarvam AI
SARVAM_API_KEY=
SARVAM_STT_MODEL=saaras:v2.5

# Whisper
WHISPER_MODEL=small
```


# 🚀 Running the Project

## Streamlit

```bash
streamlit run app.py
```


## CLI

```bash
python main.py
```


# 💡 Example Workflow

1. Upload a meeting recording or paste a YouTube URL.
2. Audio is downloaded.
3. Audio is chunked.
4. Whisper/Sarvam transcribes speech.
5. AI generates:
   - Title
   - Summary
   - Action Items
   - Key Decisions
   - Questions
6. Transcript is embedded into ChromaDB.
7. Users interact with the meeting through RAG-powered chat.


# 🧠 AI Pipeline

## Meeting Summarization

```text
Transcript
      │
      ▼
 Split into Chunks
      │
      ▼
 Chunk Summaries
      │
      ▼
 Merge & Refine
      │
      ▼
 Final Summary
```


## Information Extraction

The same Map-Reduce strategy is used for:

- Action Items
- Key Decisions
- Open Questions


## Retrieval-Augmented Generation

```text
Transcript
      │
      ▼
Text Splitting
      │
      ▼
Embeddings
      │
      ▼
ChromaDB
      │
      ▼
Similarity Search
      │
      ▼
Relevant Context
      │
      ▼
LLM
      │
      ▼
Answer
```


# 🤝 Contributing

Contributions are always welcome!

## 1. Fork the repository

Click the **Fork** button on GitHub.


## 2. Clone your fork

```bash
git clone https://github.com/<your-username>/VideoMate.git

cd VideoMate
```


## 3. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it.

Install dependencies.

```bash
pip install -r requirements.txt
```


## 4. Configure Environment Variables

Create a `.env` file.

Refer to the **Environment Variables** section.


## 5. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```


## 6. Make Your Changes

Please ensure:

- Code follows the existing project structure.
- Keep functions modular.
- Test your changes before committing.
- Update documentation if needed.


## 7. Commit

```bash
git add .

git commit -m "Add feature description"
```


## 8. Push

```bash
git push origin feature/your-feature-name
```


## 9. Open a Pull Request

Describe:

- What changed
- Why it changed
- Screenshots (if UI changes)
- Testing performed


# 📌 Roadmap

- [x] Meeting Summarization
- [x] Automatic Title Generation
- [x] Action Item Extraction
- [x] Decision Extraction
- [x] Open Question Detection
- [x] RAG-based Meeting Chat
- [x] Groq Integration
- [x] Ollama Integration
- [ ] Speaker Diarization
- [ ] Meeting Timeline
- [ ] Multi-language UI
- [ ] Email Meeting Reports
- [ ] Calendar Integration
- [ ] Multi-Meeting Semantic Search
- [ ] Docker Support
- [ ] Cloud Deployment


# 📜 License

This project is intended for educational, research, and personal use.


# 👨‍💻 Author

**Pavan Teja**

Built with ❤️ using Python, LangChain, Whisper, Groq, Ollama, ChromaDB, HuggingFace Embeddings, Streamlit, and Sarvam AI.
