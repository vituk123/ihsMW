import pypdf
import sys

def search_pdf(pdf_path, keywords):
    print(f"Searching {pdf_path}...")
    reader = pypdf.PdfReader(pdf_path)
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        for kw in keywords:
            if kw.lower() in text.lower():
                print(f"Found '{kw}' on Page {i+1}")
                # Print a small snippet around the keyword
                pos = text.lower().find(kw.lower())
                start = max(0, pos - 150)
                end = min(len(text), pos + 150)
                print(f"Snippet: ...{text[start:end]}...\n")

search_pdf("/Users/vitumbikokayuni/Downloads/IHS5 2019-2020 Household Survey Basic Information.pdf", ["conversion", "factor", "pail", "oxcart"])
