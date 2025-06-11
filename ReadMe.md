<h1 align="center">NLP<samp><i> Search Engine</i></samp></h1>

# 📑About Our NLP Project

This project is a Natural Language Processing (NLP)-based search engine designed to help users find the most relevant documents based on their search queries. It processes user input in natural language, analyzes its meaning, and retrieves documents that closely match the intent of the search.

# 🚀 How to Run the NLP-Based Document Search Engine

Follow the steps below to set up and run the document search engine:

## 1. Preprocessing

First, run the following script to prepare the n-gram datasets:

```bash
python Preprocessing-Ngram_Bgram_Tgram.py
```

## 2. Bag-of-Words Preprocessing

After the n-gram preprocessing is completed, run:

```bash
python Preprocessing-SearchBoW.py
```

## 3. Generate N-gram Matching Results

Once preprocessing is done, execute the script for generating N-gram matching results:

```bash
python Ngram-Bgram-Tgram.py
```

## 4. Run the Application

### Option A: With React UI

If you wish to use the web interface:

1. Navigate to the `UI-React` directory.
2. In the terminal, run:

```bash
npm run dev
```

3. Open your browser and try out the search engine from the React UI.

### Option B: Without UI

To use the search engine directly from the terminal without UI, run:

```bash
python prediksiKataTanpaUI.py
```

---

> **Note:**  
> Some scripts may contain hardcoded local file paths. Please make sure to update those paths according to your own computer's directory structure to ensure the application runs properly.

# 👊The Team

|              Member               |   NIM    |
| :-------------------------------: | :------: |
|     Farrel Ardiyanto Saputro      | 71210702 |
| Leonardo Bondan Nusantara Hendrik | 71210730 |
| Yosriko Rahmat Karoni Sabelekake' | 71210780 |
|        Yessa Ryantie Laoh         | 71220916 |

<p align="right">Sign by~ <br/>Group 4 Team </p>
