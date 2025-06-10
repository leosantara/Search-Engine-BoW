import os
import fitz  # PyMuPDF
import re
import csv
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

# 'punkt' tokenizer diperlukan untuk word_tokenize dan sent_tokenize.
try:
    # cek tokenizer 'punkt' dan 'punkt_tab'
    nltk.data.find('tokenizers/punkt')
    # nltk.data.find('tokenizers/punkt_tab') 
except nltk.downloader.DownloadError:
    print("Mengunduh NLTK 'punkt' tokenizer...")
    try:
        nltk.download('punkt')
    except Exception as e:
        print(f"Gagal mengunduh 'punkt': {e}. Pastikan koneksi internet stabil.")
    print("Pengunduhan data NLTK selesai (periksa pesan di atas untuk keberhasilan).")

def preprocess_sentence_to_tokens(sentence):
    """
    Melakukan normalisasi (lowercase), penghilangan tanda baca, dan tokenisasi kata pada satu kalimat.
    Mengembalikan daftar token.
    """
    sentence = sentence.lower()
    sentence = re.sub(r'[^a-z0-9\s]', '', sentence)
    
    tokens = word_tokenize(sentence)
    
    return tokens

def process_pdfs_to_csv(pdf_folder, csv_output_path):
    """
    Mengonversi PDF ke teks, melakukan tokenisasi kalimat, praproses pada setiap kalimat, 
    dan menyimpan hasilnya ke file CSV.
    Setiap baris teks yang telah dipraproses (dalam bentuk token yang digabungkan) 
    akan menjadi satu baris di CSV.
    """
    if not os.path.exists(pdf_folder):
        print(f"Error: Folder PDF tidak ditemukan di '{pdf_folder}'.")
        return

    with open(csv_output_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        #  header CSV 
        csv_writer.writerow(['document_name', 'sentence_number', 'preprocessed_tokens'])

        # Iterasi melalui semua file dalam folder PDF yang ditentukan
        for file_name in os.listdir(pdf_folder):
            if file_name.endswith(".pdf"):
                pdf_path = os.path.join(pdf_folder, file_name)
                print(f"Memproses file: {file_name}")

                try:
                    # Buka dokumen PDF menggunakan PyMuPDF (fitz)
                    doc = fitz.open(pdf_path)
                    full_text = ""
                    for page in doc:           # Ekstrak teks dari setiap halaman PDF
                        full_text += page.get_text("text") + " " # Gabungkan teks halaman dengan spasi
                    doc.close() # Tutup dokumen setelah selesai

                    # Tokenisasi Kalimat: Pisahkan seluruh teks dokumen menjadi kalimat-kalimat individual
                    sentences = sent_tokenize(full_text)
                    
                    sentence_count = 0 # Penghitung kalimat untuk setiap dokumen
                    for sentence in sentences:
                        # Hanya proses kalimat yang tidak kosong atau hanya berisi spasi
                        if sentence.strip():
                            sentence_count += 1
                            preprocessed_tokens = preprocess_sentence_to_tokens(sentence)

                            if preprocessed_tokens:
                                csv_writer.writerow([file_name, sentence_count, ' '.join(preprocessed_tokens)])
                                
                except Exception as e:
                    print(f"Gagal memproses {file_name}: {e}")
                    
    print(f"\nSemua dokumen PDF telah diproses dan disimpan ke: {csv_output_path}")


pdf_folder = "D:\\Latihan\\Python\\NLP\\Search Engine\\File PDF"
csv_output_path = "D:\\Latihan\\Python\\NLP\\Search Engine\\HasilPreprosesing\\Preprocessed_SearchBoW.csv"

if __name__ == "__main__":
    process_pdfs_to_csv(pdf_folder, csv_output_path)
