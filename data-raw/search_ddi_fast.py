import pypdf

pdf_path = "/Users/vitumbikokayuni/Downloads/DDI Documentation English.pdf"
reader = pypdf.PdfReader(pdf_path)

with open("/Users/vitumbikokayuni/Documents/IHS-mw/data-raw/search_results.txt", "w") as f:
    f.write(f"Total pages: {len(reader.pages)}\n")
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if "conversion" in text.lower():
            f.write(f"\n--- Page {i+1} ---\n")
            lines = text.split('\n')
            for line in lines:
                if "conversion" in line.lower() or "factor" in line.lower() or "pail" in line.lower():
                    f.write(line + "\n")
print("Search complete.")
