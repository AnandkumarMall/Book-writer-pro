
# 📚 Automated Book Publication Workflow

This project is an AI-powered pipeline designed to fetch book chapters from the web, rewrite them using LLMs (e.g., Gemini), review them with AI and humans, version the outputs, and allow retrieval based on RL-style search.

---

## 🚀 Features

### 1. Web Scraping & Screenshots (`scrapper.py`)
- Scrapes content from a given Wikisource URL.
- Saves full-page screenshots of the chapter for reference.
- Uses `Playwright` for scraping and rendering.

### 2. AI Writing (`gemini_writer.py`)
- Uses a Gemini API (or any LLM) to rewrite chapters with improved clarity or emotional tone.

### 3. AI Reviewing (`ai_reviewer.py`)
- Automatically evaluates AI-written content.
- Scores clarity, emotion, and correctness.
- Review metadata is stored for ranking later.

### 4. Human-in-the-Loop
- Allows writers/editors to view AI suggestions.
- Supports multiple iteration rounds for refining text.

### 5. ChromaDB Integration (`chromedb_store.py`)
- Stores multiple versions of chapters with metadata:
  - Book name
  - Chapter number
  - AI review
  - Human feedback (optional)
- Enables versioning of rewritten chapters.

### 6. RL-style Retrieval System (`retrival.py`)
- Intelligent retrieval of best chapter versions based on:
  - Clarity
  - Emotion
- Uses reinforcement-style scoring from metadata.
- Allows exporting best version as a PDF.

### 7. Streamlit App (`app.py`)
- Complete frontend interface for:
  - Loading books & chapters
  - Running AI Writer & Reviewer
  - Saving and retrieving versions
  - Exporting final content as PDF

---

## 🛠️ How to Use

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

### 2. Install Playwright and Chromium

```bash
playwright install
```

### 3. Run the Streamlit App

```bash
streamlit run app.py
```

### 4. Folder Structure

```
.
├── app.py                 # Streamlit frontend
├── scrapper.py           # Playwright-based scraper
├── gemini_writer.py      # AI Writer using LLM
├── ai_reviewer.py        # AI Reviewer scoring clarity/emotion
├── chromedb_store.py     # Save versions with ChromaDB
├── retrival.py           # Retrieval + RL-style ranking
├── screenshots/          # Saved chapter screenshots
├── chromadb_data/        # Persistent vector DB
├── requirements.txt      # Required libraries
└── README.md             # Project documentation
```

---

## 🧠 Technologies Used

- **Python**
- **Playwright**
- **ChromaDB**
- **LLMs (e.g., Gemini)**
- **Streamlit**
- **FPDF**
- **Reinforcement Learning-style scoring**

---

## 📦 Requirements

A list of libraries used is available in the file below:

### `requirements.txt`
```
streamlit
chromadb
fpdf
playwright
generativeai
```

---


