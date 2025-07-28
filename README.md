
# 🧠 DocuMind-1A — Round 1A: Understand Your Document

> 🎯 Adobe India Hackathon 2025 — Round 1A Challenge  
> 🚀 Goal: Extract clean, structured outlines (Title, H1–H3) from PDFs in an **offline**, **Dockerized**, **CPU-compatible** solution.


## 📌 Problem Statement

You're handed a PDF — but instead of reading it manually, your task is to **extract its structure like a machine**.

Your solution must:
- ✅ Accept **PDFs up to 50 pages**
- ✅ Extract the **Title**, **Headings (H1, H2, H3)**, and **Page numbers**
- ✅ Output **JSON** matching Adobe's provided schema


## ✅ Features

- 🧠 Accurate heading extraction using **font-size + semantic filtering**
- 🌍 Supports **multilingual PDFs** (e.g., Japanese, Hindi)
- 🔐 Fully **offline** — no internet/API calls
- ⚡ Fast — completes within **≤10s** for 50 pages
- 🐳 **Dockerized**, runs on **CPU-only amd64** architecture
- 📦 Outputs structured `<filename>.json` files to `/app/output`


## 🧾 Output Format

Each PDF generates a JSON like this:

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}

⚙️ How It Works

PDF is parsed using pdfminer.six
Font size and layout info is extracted per page
Top 3 font sizes are mapped to H1, H2, H3
Smart rules filter valid headings (e.g. text length, noise, keywords)
JSON output is created with title + structured outline

🐳 Docker Setup

🔨 Build the Docker Image

Recommended for compatibility with Adobe’s amd64 environment

# For Linux/macOS or cross-platform build
docker build --platform linux/amd64 -t documind-1a .

# If you're testing on Windows PowerShell
docker build -t documind-1a .

🚀 Run the Container

🐧 For Linux/macOS:

docker run --rm \
  -v "$(pwd)/sample_dataset/pdfs:/app/input:ro" \
  -v "$(pwd)/sample_dataset/outputs:/app/output" \
  --network none \
  documind-1a

🪟 For Windows PowerShell:

docker run --rm `
  -v "${PWD}\sample_dataset\pdfs:/app/input:ro" `
  -v "${PWD}\sample_dataset\outputs:/app/output" `
  --network none `
  documind-1a

✅ All PDF files inside /app/input will be processed automatically, generating one .json per .pdf.

✅ Adobe Constraints Checklist - 
Constraint	            ✅Status             Details
Max Runtime	            ✅ Met	           ≤ 10 seconds for 50-page PDFs
Model Size	            ✅ N/A	           No ML model used
Internet Access	        ✅ Offline only	   Fully Dockerized, no API/web usage
Architecture	        ✅ amd64-only       Compatible & tested
Output Format	        ✅ Matches schema   JSON validated
Multilingual Handling	✅ Implemented	   Japanese headings supported

📚 Libraries Used

pdfminer.six — For font-size, layout, and semantic text extraction
Python 3.10
No external APIs or machine learning models used

🔒 Notes
❌ No hardcoded file names, heuristics, or heading assumptions
✅ Works across simple & complex PDFs
✅ No internet, API keys, or web dependencies
✅ Tested successfully on Linux and Windows (PowerShell)


🏁 Final Output Location

All extracted .json files will be saved to:

/sample_dataset/outputs/
Each file will match its input PDF name, e.g., jap_doc.pdf → jap_doc.json


