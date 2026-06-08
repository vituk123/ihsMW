import pypdf

reader = pypdf.PdfReader("/Users/vitumbikokayuni/Downloads/DDI Documentation English.pdf")
print("Total pages:", len(reader.pages))

for page_num in range(1854, 1862):
    if page_num < len(reader.pages):
        print(f"--- DDI PAGE {page_num + 1} ---")
        text = reader.pages[page_num].extract_text()
        print(text[:2500])
