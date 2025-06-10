import pandas as pd

# Load n-gram CSV
df_unigram = pd.read_csv("D:\\Latihan\\Python\\NLP\\Search Engine\\HasilPreprosesing\\1unigram.csv")
df_bigram = pd.read_csv("D:\\Latihan\\Python\\NLP\\Search Engine\\HasilPreprosesing\\2bigram.csv")
df_trigram = pd.read_csv("D:\\Latihan\\Python\\NLP\\Search Engine\\HasilPreprosesing\\3trigram.csv")

# Ubah kolom bigram & trigram jadi tuple
df_bigram['bigram'] = df_bigram['bigram'].apply(eval)
df_trigram['trigram'] = df_trigram['trigram'].apply(eval)

def predict_next_word(input_text, top_n=5):
    words = input_text.strip().lower().split()
    
    if len(words) == 0:
        # Gunakan unigram
        print("Prediksi berdasarkan unigram:")
        print(df_unigram.sort_values(by="frekuensi", ascending=False).head(top_n))
    
    elif len(words) == 1:
        # Gunakan bigram
        last_word = words[-1]
        candidates = df_bigram[df_bigram['bigram'].apply(lambda x: x[0] == last_word)]
        if candidates.empty:
            print("Tidak ditemukan prediksi berdasarkan bigram.")
        else:
            print(f"Prediksi setelah '{last_word}':")
            print(candidates.sort_values(by="frekuensi", ascending=False).head(top_n)[['bigram', 'frekuensi']])
    
    else:

        last_two = tuple(words[-2:])
        candidates = df_trigram[df_trigram['trigram'].apply(lambda x: (x[0], x[1]) == last_two)]
        if candidates.empty:
            print("Tidak ditemukan prediksi berdasarkan trigram.")
        else:
            print(f"Prediksi setelah '{last_two[0]} {last_two[1]}':")
            print(candidates.sort_values(by="frekuensi", ascending=False).head(top_n)[['trigram', 'frekuensi']])


while True:
    query = input("\nMasukkan 0–2 kata (atau ketik 'exit' untuk keluar): ")
    if query.lower() == 'exit':
        break
    predict_next_word(query)
