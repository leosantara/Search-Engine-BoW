import pandas as pd
from collections import Counter
from nltk import ngrams
from nltk.corpus import stopwords
import nltk

try:
    stop_words = set(stopwords.words('indonesian'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('indonesian'))

# Baca file CSV (Ganti path sesuai kebutuhan)
csv_input = "D:\\Latihan\\Python\\NLP\\Search Engine\\HasilPreprosesing\\Preprocessed_NGramBGramTRam.csv"
df = pd.read_csv(csv_input, sep=';', encoding='utf-8')

# Inisialisasi awal
unigram_counter = Counter()
bigram_counter = Counter()
trigram_counter = Counter()

# Proses setiap baris
for tokens in df['hasilTokenisasi']:
    words = tokens.split()

    # Unigram: d
    unigram_counter.update(words)

    # Bigram & Trigram: 
    bigram_counter.update([bg for bg in ngrams(words, 2) if all(w not in stop_words for w in bg)])
    trigram_counter.update([tg for tg in ngrams(words, 3) if all(w not in stop_words for w in tg)])

# Simpan hasil ke CSV
pd.DataFrame(unigram_counter.items(), columns=["unigram", "frekuensi"])\
  .sort_values(by="frekuensi", ascending=False)\
  .to_csv("D:\\Latihan\\Python\\NLP\\Search Engine\\HasilPreprosesing\\1unigram.csv", index=False, encoding="utf-8")

pd.DataFrame(bigram_counter.items(), columns=["bigram", "frekuensi"])\
  .sort_values(by="frekuensi", ascending=False)\
  .to_csv("D:\\Latihan\\Python\\NLP\\Search Engine\\HasilPreprosesing\\2bigram.csv", index=False, encoding="utf-8")

pd.DataFrame(trigram_counter.items(), columns=["trigram", "frekuensi"])\
  .sort_values(by="frekuensi", ascending=False)\
  .to_csv("D:\\Latihan\\Python\\NLP\\Search Engine\\HasilPreprosesing\\3trigram.csv", index=False, encoding="utf-8")

print("Semua file n-gram berhasil disimpan!")
