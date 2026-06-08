import pypdf

reader = pypdf.PdfReader("/Users/vitumbikokayuni/Downloads/IHS5 2019-2020 Household Survey Basic Information.pdf")
print("Total pages:", len(reader.pages))

for page_num in range(4, 10):
    print(f"--- PAGE {page_num + 1} ---")
    text = reader.pages[page_num].extract_text()
    print(text)
