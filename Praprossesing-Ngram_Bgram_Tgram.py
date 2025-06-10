import os
import pandas as pd
import fitz  # PyMuPDF
import re

# Folder PDF (Ganti path sesuai kebutuhan)
pdf_folder = "D:\\Latihan\\Python\\NLP\\Search Engine\\File PDF"

# Ekstrak teks dari PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Preprocessing
def preprocess_text(text):
    text = text.lower()                                 # Lowercase
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)          # Hapus semua karakter selain huruf, angka, dan spasi
    text = re.sub(r'\s+', ' ', text).strip()            # Normalisasi spasi
    return text

# Tokenisasi
def tokenize(text):
    return text.split()

# Proses semua PDF
data = []
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        path = os.path.join(pdf_folder, filename)
        raw_text = extract_text_from_pdf(path)
        clean_text = preprocess_text(raw_text)
        tokens = tokenize(clean_text)
        token_string = ' '.join(tokens)
        data.append({
            "namaFile": filename,
            "hasilTokenisasi": token_string
        })


# Simpan ke CSV dengan delimiter ";"
csv_output = os.path.join("D:\\Latihan\\Python\\NLP\\Search Engine\\HasilPreprosesing", "Preprocessed_NGramBGramTRam.csv")
df = pd.DataFrame(data)
df.to_csv(csv_output, index=False, sep=';', encoding='utf-8')

print(f"CSV berhasil disimpan di: {csv_output}")
