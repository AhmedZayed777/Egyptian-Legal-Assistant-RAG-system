# ⚖️ Egyptian Legal Assistant
### AI-Powered Arabic Legal Assistant using Retrieval-Augmented Generation (RAG)

![Python](https://img.shields.io/badge/Python-3.11-blue)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Database-orange)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow)
![License](https://img.shields.io/badge/License-MIT-success)

An AI-powered legal assistant that answers questions about **Egyptian Labor Law No. 14 of 2025** using **Retrieval-Augmented Generation (RAG)**. The system retrieves the most relevant legal articles from a structured knowledge base and generates accurate, grounded responses in Arabic with article citations.

---

# 📖 Table of Contents

- Project Overview
- Features
- Why RAG?
- System Architecture
- Project Workflow
- Repository Structure
- Dataset
- Technologies Used
- Models
- Installation
- Usage
- Sample Questions
- Challenges & Solutions
- Future Improvements
- Disclaimer
- Author

---

# 📌 Project Overview

Understanding legal documents can be difficult for non-specialists due to the complexity and length of legal texts.

This project aims to simplify access to Egyptian labor law by allowing users to ask questions in natural Arabic and receive responses generated directly from the official law text.

Instead of relying solely on a Large Language Model's internal knowledge, the assistant first retrieves the most relevant legal articles and then generates an answer based only on those retrieved articles.

This significantly improves:

- Accuracy
- Transparency
- Explainability
- Reduced hallucinations
- Reliable legal citations

---

# ✨ Features

- Arabic legal question answering
- Retrieval-Augmented Generation (RAG)
- Semantic search using FAISS
- Arabic sentence embeddings
- Grounded answers with article citations
- Structured legal knowledge base
- Streamlit web interface
- Modular architecture for adding more laws

---

# ❓ Why RAG?

Traditional LLM chatbots generate answers based on their training data and may produce hallucinated or outdated information.

This project uses **Retrieval-Augmented Generation (RAG)** to improve reliability.

Workflow:

1. User asks a legal question.
2. The system converts the question into an embedding.
3. FAISS retrieves the most relevant legal articles.
4. The retrieved context is passed to the LLM.
5. The LLM generates an answer grounded in the retrieved legal text.
6. The response includes article citations.

This approach provides more trustworthy answers while keeping the model focused on official legal documents.

---

# 🏗️ System Architecture

```
                     Egyptian Labor Law JSON
                               │
                               ▼
                     Text Preprocessing
                               │
                               ▼
                 Sentence Embedding Generation
                               │
                               ▼
                      FAISS Vector Database
                               │
                               ▼
User Question ─────────► Semantic Retrieval
                               │
                               ▼
                   Top-k Relevant Articles
                               │
                               ▼
                    Mistral Large Language Model
                               │
                               ▼
              Grounded Arabic Answer + Citation
                               │
                               ▼
                        Streamlit Interface
```

---

# 🔄 Project Workflow

```
Official Government PDF
          │
          ▼
Text Extraction
          │
          ▼
Arabic Text Cleaning
          │
          ▼
Structured JSON Dataset
          │
          ▼
Embedding Generation
          │
          ▼
FAISS Index
          │
          ▼
Retriever
          │
          ▼
Prompt Construction
          │
          ▼
Mistral LLM
          │
          ▼
Answer with Article Citation
          │
          ▼
Streamlit Web Application
```

---

# 📂 Repository Structure

```
egyptian-legal-assistant/
│
├── README.md
├── requirements.txt
├── build_index.py
│
├── data/
│   ├── labor_law_14_2025.json
│   └── issuing_law_14_2025.json
│
├── notebooks/
│   └── project-work-legal-assistant.ipynb
│
├── app/
│   └── app.py
│
├── legal_index/
│
└── assets/
    ├── home.png
    ├── architecture.png
    └── example-question.png
```

---

# 📚 Dataset

The project uses structured JSON files created from the official Egyptian Labor Law.

### Included Documents

- **Issuing Law**
  - 13 procedural articles

- **Labor Law**
  - 299 legal articles

Each article contains metadata including:

- Article number
- Chapter
- Book
- Law name
- Source
- Status
- Effective date
- Full Arabic text

Example:

```json
{
  "article": 47,
  "book": "علاقات العمل الفردية",
  "chapter": "الإجازات",
  "text": "...",
  "status": "active"
}
```

---

# 🛠 Technologies Used

- Python
- LangChain
- Hugging Face Transformers
- Sentence Transformers
- FAISS
- Streamlit
- PyTorch
- Pandas
- NumPy
- Jupyter Notebook

---

# 🤖 Models

## Embedding Model

```
sentence-transformers/paraphrase-multilingual-mpnet-base-v2
```

Supports multilingual semantic search with strong Arabic performance.

---

## Language Model

```
Mistral-Nemo-Instruct-2407
```

Used to generate grounded Arabic legal answers based on retrieved documents.

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/egyptian-legal-assistant.git

cd egyptian-legal-assistant
```

Install dependencies

```bash
pip install -r requirements.txt
```

Build the FAISS index

```bash
python build_index.py
```

Run the Streamlit application

```bash
streamlit run app/app.py
```

---

# 💻 Running on Kaggle

1. Upload both JSON files as a Kaggle Dataset.
2. Open the notebook inside `notebooks/`.
3. Attach the dataset.
4. Enable GPU.
5. Run all notebook cells.
6. Launch the Streamlit interface through ngrok.

---

# 💬 Example Questions

```
ما هي مدة الإجازة السنوية للعامل؟

ما هي حقوق العامل عند إنهاء عقد العمل؟

كم ساعة العمل اليومية؟

هل يجوز فصل العاملة الحامل؟

ما هو تعريف العامل في القانون؟

متى يبدأ تنفيذ قانون العمل الجديد؟
```

---

# 📊 Results

- Indexed **312 legal articles**
- Arabic semantic retrieval using FAISS
- Grounded answers generated with LLM
- Article-level citations
- Fast semantic search over official legal documents

---

# ⚙ Challenges & Solutions

| Challenge | Solution |
|------------|----------|
| Arabic OCR corruption | Custom preprocessing and text correction pipeline |
| Retrieval quality | Normalized multilingual embeddings |
| Prompt repetition | Generated text sliced after input tokens |
| GPU memory limitations | Optimized model loading and memory cleanup |
| Large vector database | FAISS indexing for efficient retrieval |

---

# 🔮 Future Improvements

- Support additional Egyptian laws
- Hybrid Retrieval (BM25 + Dense Retrieval)
- Cross-Encoder reranking
- Conversation memory
- Docker deployment
- REST API
- Cloud deployment
- Confidence scoring
- Multi-document retrieval
- PDF upload and automatic indexing

---

# ⚠ Disclaimer

This project is intended for educational and research purposes only.

It does **not** constitute legal advice. Users should consult qualified legal professionals for official legal guidance.

---

# 👨‍💻 Author

**Ahmed Zayed**

Computer Science Student — Benha University

Interested in:

- Artificial Intelligence
- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)
- Natural Language Processing (NLP)
- Computer Vision
- Machine Learning

---

# ⭐ If you found this project useful

If you found this repository interesting, consider giving it a ⭐ to support the project.
