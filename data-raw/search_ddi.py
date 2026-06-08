import pypdf

def search_pdf(pdf_path, keywords):
    print(f"Searching {pdf_path}...")
    reader = pypdf.PdfReader(pdf_path)
    print(f"Total pages: {len(reader.pages)}")
    found_pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        matches = [kw for kw in keywords if kw.lower() in text.lower()]
        if len(matches) > 1:
            print(f"Page {i+1} has multiple matches: {matches}")
            found_pages.append(i+1)
    return found_pages

search_pdf("/Users/vitumbikokayuni/Downloads/DDI Documentation English.pdf", ["conversion", "factor", "kilogram", "kg", "crop", "pail"])
