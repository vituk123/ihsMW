import pypdf

reader = pypdf.PdfReader("/Users/vitumbikokayuni/Downloads/IHS5 2019-2020 Household Survey Basic Information.pdf")
print("Total pages:", len(reader.pages))

for page_num in range(58, 69):
    if page_num < len(reader.pages):
        print(f"--- PAGE {page_num + 1} ---")
        text = reader.pages[page_num].extract_text()
        print(text[:2000]) # Print first 2000 characters of each page
