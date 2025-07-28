
import os
import json
import re
from pathlib import Path
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

INPUT_DIR = Path("/app/input")
OUTPUT_DIR = Path("/app/output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def is_heading_candidate(text):
    if len(text.split()) < 3:
        return False
    if len(text) == 0 or sum(c.isalpha() for c in text) / len(text) < 0.4:
        return False
    if re.match(r'^\d{1,2}\.\s.*\"', text):
        return False
    if any(kw in text.lower() for kw in [
        "copyright", "table of contents", "index", "keywords", "abstract"
    ]):
        return False
    return True

def extract_headings(pdf_path):
    grouped = {}
    for page_num, layout in enumerate(extract_pages(pdf_path), start=1):
        for element in layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    if hasattr(text_line, 'get_text'):
                        text = text_line.get_text().strip()
                        if not text:
                            continue
                        sizes = [char.size for char in text_line if isinstance(char, LTChar)]
                        avg_size = round(sum(sizes) / len(sizes), 2) if sizes else 0
                        key = (avg_size, page_num)
                        grouped.setdefault(key, []).append(text)

    # Merge lines of same size + page
    combined = []
    for (size, page), lines in grouped.items():
        full_text = " ".join(lines).strip()
        combined.append((full_text, size, page))

    # Sort font sizes and assign levels
    all_sizes = sorted({s for _, s, _ in combined if s > 0}, reverse=True)
    size_to_level = {}
    if len(all_sizes) >= 3:
        size_to_level = {all_sizes[0]: "H1", all_sizes[1]: "H2", all_sizes[2]: "H3"}
    elif len(all_sizes) == 2:
        size_to_level = {all_sizes[0]: "H1", all_sizes[1]: "H2"}
    elif all_sizes:
        size_to_level = {all_sizes[0]: "H1"}

    result = []
    seen = set()
    for text, size, page in combined:
        if (text, page) in seen:
            continue
        seen.add((text, page))
        if is_heading_candidate(text):
            level = size_to_level.get(size, "H3")
            result.append({
                "text": text,
                "level": level,
                "page": page
            })

    return result

def extract_title(structured):
    # Try first H1 as title
    for item in structured:
        if item["level"] == "H1":
            return item["text"]
    # Fallback: first H2
    for item in structured:
        if item["level"] == "H2":
            return item["text"]
    # Fallback: any heading
    return structured[0]["text"] if structured else ""

def process_all_pdfs():
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = INPUT_DIR / filename
            structure = extract_headings(pdf_path)
            title = extract_title(structure)

            # Keep title out of outline
            outline = [s for s in structure if s["text"] != title]

            output_json = {
                "title": title,
                "outline": outline
            }

            out_path = OUTPUT_DIR / filename.replace(".pdf", ".json")
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(output_json, f, indent=2, ensure_ascii=False)
            print(f"✅ Processed: {filename}")

if __name__ == "__main__":
    process_all_pdfs()

