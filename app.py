from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS 
import os 

app = Flask(__name__)
CORS(app) # Mengaktifkan CORS untuk semua rute


# Pastikan path ini sesuai dengan tempat file N-gram CSV
N_GRAM_DATA_FOLDER = "D:\\Latihan\\Python\\NLP\\Week 7\\pdf\\"
# Path ke file CSV hasil praproses dokumen
PREPROCESSED_DOCS_PATH = "D:\\Latihan\\Python\\NLP\\Week 7\\preprocessed_documents.csv"

# Load n-gram data
try:
    df_unigram = pd.read_csv(f"{N_GRAM_DATA_FOLDER}unigram.csv")
    df_bigram = pd.read_csv(f"{N_GRAM_DATA_FOLDER}bigram.csv")
    df_trigram = pd.read_csv(f"{N_GRAM_DATA_FOLDER}trigram.csv")

    df_bigram['bigram'] = df_bigram['bigram'].apply(eval)
    df_trigram['trigram'] = df_trigram['trigram'].apply(eval)
    print("Data N-gram berhasil dimuat.")
except FileNotFoundError:
    print(f"Error: Pastikan file N-gram CSV ada di '{N_GRAM_DATA_FOLDER}'. Jalankan generate_ngrams.py terlebih dahulu.")
    exit()
except Exception as e:
    print(f"Error saat memuat data N-gram: {e}")
    exit()

# Load preprocessed documents
try:
    df_preprocessed_docs = pd.read_csv(PREPROCESSED_DOCS_PATH)
    df_preprocessed_docs['preprocessed_tokens'] = df_preprocessed_docs['preprocessed_tokens'].fillna('')
    print(f"Dokumen praproses berhasil dimuat dari: {PREPROCESSED_DOCS_PATH}")
except FileNotFoundError:
    print(f"Error: File dokumen praproses tidak ditemukan di '{PREPROCESSED_DOCS_PATH}'. Pastikan Anda telah menjalankan skrip praproses PDF.")
    exit()
except Exception as e:
    print(f"Error saat memuat dokumen praproses: {e}")
    exit()


@app.route("/api/predict")
def predict():
    query = request.args.get("query", "").lower().strip()
    words = query.split()

    TOP_N_PREDICTIONS = 5
    predictions = []

    if len(words) >= 2:
        last_two_words = tuple(words[-2:])
        filtered_trigram = df_trigram[df_trigram['trigram'].apply(lambda x: (x[0], x[1]) == last_two_words)]
        top_trigram = filtered_trigram.sort_values(by="frekuensi", ascending=False).head(TOP_N_PREDICTIONS)
        predictions.extend([list(x) for x in top_trigram['trigram']])

    if len(predictions) < TOP_N_PREDICTIONS and len(words) >= 1:
        last_word = words[-1]
        filtered_bigram = df_bigram[df_bigram['bigram'].apply(lambda x: x[0] == last_word)]
        
        if len(words) >= 2:
            existing_starts = set(tuple(p[:2]) for p in predictions if isinstance(p, list) and len(p) >= 2)
            filtered_bigram = filtered_bigram[~filtered_bigram['bigram'].apply(lambda x: x in existing_starts)]

        top_bigram = filtered_bigram.sort_values(by="frekuensi", ascending=False).head(TOP_N_PREDICTIONS - len(predictions))
        predictions.extend([list(x) for x in top_bigram['bigram']])

    if len(predictions) < TOP_N_PREDICTIONS:
        existing_words = set()
        for p in predictions:
            if isinstance(p, list):
                existing_words.update(p)
            else:
                existing_words.add(p)

        filtered_unigram = df_unigram[~df_unigram['unigram'].isin(existing_words)]
        top_unigram = filtered_unigram.sort_values(by="frekuensi", ascending=False).head(TOP_N_PREDICTIONS - len(predictions))
        predictions.extend(top_unigram["unigram"].tolist())

    return jsonify(predictions)


@app.route("/api/search")
def search():
    query = request.args.get("query", "").lower().strip()
    if not query:
        return jsonify([])

    query_tokens = query.split()
    results = []

    for index, row in df_preprocessed_docs.iterrows():
        doc_name = row['document_name']
        sentence_num = row['sentence_number']
        sentence_tokens_str = row['preprocessed_tokens'] 
        
        sentence_tokens = sentence_tokens_str.split()
        score = 0

        unique_query_tokens = set(query_tokens)
        for q_token in unique_query_tokens:
            if q_token in sentence_tokens:
                score += 1 
        
        if score > 0:
            results.append({
                "document_name": doc_name,
                "sentence_number": sentence_num,
                "sentence_text": " ".join(sentence_tokens),
                "score": score
            })
    
    # Urutkan hasil berdasarkan skor secara menurun
    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
    
    # Batasi hingga TOP_SEARCH_RESULTS hasil teratas untuk ditampilkan
    TOP_SEARCH_RESULTS = 10
    return jsonify(sorted_results[:TOP_SEARCH_RESULTS])

if __name__ == "__main__":
    app.run(debug=True, port=5050)
