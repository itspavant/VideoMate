Live: [https://videomate.streamlit.app/](https://videomate.streamlit.app/)

# 🎥 VideoMate – AI Meeting Assistant

VideoMate is an AI-powered meeting assistant that converts meeting recordings or YouTube videos into structured, actionable insights. It automatically transcribes meetings, generates concise summaries, extracts action items, decisions, and unanswered questions, and enables users to ask natural language questions over the meeting using Retrieval-Augmented Generation (RAG).

## ✨ Features

- 🎙️ **Speech-to-Text**
  - Local transcription using **OpenAI Whisper**
  - Hindi/Hinglish transcription + English translation using **Sarvam AI**

- 📄 **AI Meeting Summary**
  - Generates concise bullet-point summaries
  - Uses a **Map-Reduce summarization pipeline** for long transcripts

- 🏷️ **Automatic Meeting Title**
  - Generates a professional title for every meeting

- ✅ **Action Item Extraction**
  - Task description
  - Responsible owner
  - Deadline (if mentioned)

- 📌 **Key Decision Extraction**
  - Automatically identifies important decisions made during the meeting

- ❓ **Question Extraction**
  - Finds unresolved questions and follow-up topics

- 🔍 **RAG-based Q&A**
  - Ask questions about the meeting transcript
  - Retrieves only relevant transcript chunks before querying the LLM

- 📥 **Input Support**
  - Local audio/video files
  - YouTube URLs

- 📤 **Export**
  - Structured meeting notes
  - Transcript
  - Summary
  - Action Items
  - Decisions
  - Questions

## 🛠️ Tech Stack

### AI & LLM
- Mistral AI
- LangChain (LCEL)

### Speech Processing
- OpenAI Whisper
- Sarvam AI Speech-to-Text API

### Retrieval-Augmented Generation
- ChromaDB
- HuggingFace Embeddings
- Sentence Transformers

### Backend
- Python

### Media Processing
- yt-dlp
- FFmpeg
- pydub

### UI
- Streamlit

## 🏗️ Project Architecture

```
                Video / YouTube URL
                        │
                        ▼
             Download & Audio Extraction
                        │
                        ▼
                 Audio Chunking
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
   Whisper (English)          Sarvam AI (Hindi/Hinglish)
        │                               │
        └───────────────┬───────────────┘
                        ▼
                  Full Transcript
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
     Summary        Information      Vector Store
                    Extraction           │
                        │                ▼
                        │            ChromaDB
                        │                │
                        ▼                │
          Title • Action Items •         │
          Decisions • Questions          │
                                         ▼
                                  RAG Question Answering
```

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/videomate.git

cd videomate
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file.

```env
MISTRAL_API_KEY=your_api_key

SARVAM_API_KEY=your_api_key

SARVAM_STT_MODEL=saaras:v2.5

WHISPER_MODEL=small
```

## 🚀 Running the Project

Run the application

```bash
streamlit run app.py
```

or

```bash
python test.py
```

## 💡 Example Workflow

1. Upload a meeting recording or paste a YouTube link.
2. Audio is downloaded and split into chunks.
3. Whisper or Sarvam transcribes the audio.
4. AI generates:
   - Meeting Title
   - Summary
   - Action Items
   - Key Decisions
   - Open Questions
5. Transcript is embedded into ChromaDB.
6. Users can ask natural language questions about the meeting.

## 🧠 AI Pipeline

### Transcription

- Whisper (Offline)
- Sarvam AI (Translation + STT)

### Summarization

Uses a **Map-Reduce** strategy to summarize long transcripts beyond the LLM context window.

```
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

---

### Information Extraction

The same Map-Reduce pipeline is used to extract:

- Action Items
- Decisions
- Open Questions

---

### Retrieval-Augmented Generation (RAG)

```
Transcript
      │
      ▼
 Text Chunks
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
 Mistral LLM
      │
      ▼
 Answer
```

## 📈 Future Improvements

- Speaker diarization
- Meeting timeline generation
- Multi-language support
- Calendar integration
- Email meeting summaries
- Action item reminders
- Multi-meeting semantic search
- Cloud deployment

## 📜 License

This project is intended for educational and personal use.

## 👨‍💻 Author

**Pavan Teja**

Built using **Python, LangChain, Whisper, Mistral AI, ChromaDB, HuggingFace Embeddings, Streamlit, and Sarvam AI**.
