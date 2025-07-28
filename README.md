# 🧠 DocuMind-1A — Round 1A: Understand Your Document

> 🎯 Adobe India Hackathon 2025 — Round 1A Challenge  
> 🚀 Goal: Extract clean, structured outlines (Title, H1–H3) from PDFs in an **offline**, **Dockerized**, **CPU-compatible** solution.


## 📌 Problem Statement

You're handed a PDF — but instead of reading it manually, your task is to **extract its structure like a machine**.

Your solution must:
- ✅ Accept **PDFs up to 50 pages**
- ✅ Extract the **Title**, **Headings (H1, H2, H3)**, and **Page numbers**
- ✅ Output **JSON** matching Adobe's schema


## ✅ Features

- 🧠 Accurate heading extraction using **font-size + semantic filtering**
- 🌍 Supports **multilingual PDFs** (e.g., Japanese, Hindi, etc.)
- 🔐 Fully **offline** — no internet/API calls
- ⚡ Fast — completes within **≤10s** for 50 pages
- 🐳 **Dockerized**, runs on **CPU-only amd64** architecture
- 📦 Outputs per-file JSON to `/app/output`, matching schema


## 🧾 Output Format

Each PDF generates a `<filename>.json` like this:

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

## ⚙️ How It Works
 - PDF is parsed using pdfminer.six
 
 - Font size and layout info is extracted per page
 
 - Top 3 font sizes are mapped to H1, H2, H3
 
 - Smart rules filter valid headings (e.g. text length, noise, keywords)
 
 - JSON output is created with title + structured outline

## 🐳 Docker Setup

### 🔨 Build the Docker Image

**Linux/macOS (offline-safe)**

```bash
docker build --platform linux/amd64 -t documind-1a .
```

**Windows PowerShell (verified)**

```powershell
docker build -t documind-1a .
```

---

### 🚀 Run the Container

**Linux/macOS**

```bash
docker run --rm \
  -v "$(pwd)/sample_dataset/pdfs:/app/input:ro" \
  -v "$(pwd)/sample_dataset/outputs:/app/output" \
  --network none \
  documind-1a
```

**Windows PowerShell**

```powershell
docker run --rm ^
  -v "${PWD}\sample_dataset\pdfs:/app/input:ro" ^
  -v "${PWD}\sample_dataset\outputs:/app/output" ^
  --network none ^
  documind-1a
```

---

### 🏗️ Project Structure

```bash
DocuMind_1a/
├── sample_dataset/
│   ├── pdfs/              # 📥 Input PDFs
│   ├── outputs/           # 📤 Output JSONs
│   └── schema/
│       └── output_schema.json
├── process_pdfs.py        # 🧠 Main logic for heading extraction
├── Dockerfile             # 🐳 Container setup
└── README.md              # 📘 You are here
```

---

### 📌 Constraints Met

| Constraint              | Status | Details                            |
|-------------------------|--------|------------------------------------|
| Max Runtime             | ✅     | ≤ 10s for 50-page PDF              |
| Model Size              | ✅     | No ML model used                   |
| Internet Access         | ✅     | Offline only                       |
| CPU-only, amd64 arch    | ✅     | Verified                           |
| Output Format           | ✅     | Matches Adobe schema               |
| Multilingual Support    | ✅     | Japanese, Hindi, etc. supported    |

---

### 📚 Libraries Used

- `pdfminer.six` — Font & layout extraction
- Python 3.10
- No external APIs or ML models

---

### 🔒 Notes

- No hardcoded logic or file-specific tuning
- Works on arbitrary PDFs
- Semantic filtering avoids noise, footers, copyrights
