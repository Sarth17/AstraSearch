# 🚀 AstraSearch

**AstraSearch** is a modular, scalable search engine framework built from scratch in Python.  
It implements core information-retrieval concepts used in production systems such as Lucene and Elasticsearch, with a strong focus on clean architecture, correctness, and extensibility.

This project is designed for **learning, experimentation, and real-world system design**, not as a toy demo.

---

## ✨ Features

- 🔄 Streaming XML parser (handles large dumps safely)
- 🧹 Text cleaning & normalization pipeline
- 🔤 Tokenizer with stopword removal
- 🧠 Inverted index with term frequencies
- 💾 Disk persistence (index + metadata)
- 🔍 Query parsing & search engine
- 📊 TF-IDF ranking
- 🧪 Pytest-based test suite
- ⚙️ Config-driven architecture
- 🪵 Centralized logging system
- 🖥️ CLI search interface

---

## 🏗️ Architecture Overview


Documents
↓
Parser
↓
Cleaner
↓
Tokenizer
↓
Inverted Index
↓
Disk Storage
↓
Index Reader
↓
Query Parser
↓
Ranking (TF-IDF)
↓
Search Engine
↓
Results


Each component is **independent, testable, and replaceable**, making the system easy to extend with new ranking models, storage backends, or APIs.

---

## 📁 Project Structure

├── src/
│ ├── parser/
│ ├── preprocessing/
│ ├── indexer/
│ ├── storage/
│ ├── query/
│ ├── ranking/
│ └── utils/
├── scripts/
│ ├── build_index.py
│ └── run_search.py
├── tests/
├── data/ # ignored (raw dumps, index files)
├── logs/ # ignored (runtime logs)
├── requirements.txt
└── README.md


---

## 🚀 Getting Started

### 1. Create a virtual environment

```bash

python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Indexing Real Data

Download a Wikipedia dump (recommended: Simple English Wikipedia):

https://dumps.wikimedia.org/simplewiki/

Extract the file and place it here:
```bash
data/raw/simplewiki.xml
```

### 4. Build the index 
```bash
python -m scripts.build_index
```
this generates:

data/index/
├── inverted_index.json
├── documents.json
└── metadata.json

### 5. Searching

run the CLI search: 
```bash
python -m scripts.run_search
```

example: 
search> india
search> computer science
search> world war

### 6. Run the tests
```bash
python -m pytest
```

## Configuration 

all paths and constants are centralized in:
```bash
 src/utils/config.py
```

logs are written to: 
```bash
logs/app.log
```

## 📜 License
MIT License
