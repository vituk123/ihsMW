import pypdf

def search_pdf_details(pdf_path):
    reader = pypdf.PdfReader(pdf_path)
    print(f"Total pages: {len(reader.pages)}")
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if "conversion" in text.lower() or "pail" in text.lower() or "factor" in text.lower():
            lines = text.split('\n')
            for line in lines:
                if any(k in line.lower() for k in ["conversion", "pail", "factor", "oxcart", "heap", "kg", "kilogram"]):
                    print(f"Page {i+1}: {line}")

search_pdf_details("/Users/vitumbikokayuni/Downloads/IHS5 2019-2020 Household Survey Basic Information.pdf")
