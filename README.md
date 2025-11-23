# Multi-Modal RAG QA System

A production-ready Retrieval-Augmented Generation system for multi-modal document intelligence, capable of processing text, tables, and images from complex PDF documents.

## 🎯 Features

- **Multi-Modal Document Processing**: Extract text, tables, and images from PDFs
- **Semantic Search**: Vector-based retrieval using sentence transformers
- **Citation-Backed Answers**: Every response includes source attribution
- **Interactive Chat Interface**: Streamlit-based UI for natural conversations
- **Modular Architecture**: Easy to extend and customize

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- (Optional) Tesseract OCR for image text extraction

### Installation

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Place Your PDF**
   - Put your PDF file in `data/raw/qatar_test_doc.pdf`
   - Or update the path in `config.py`

3. **Run the Pipeline**
```bash
python run_pipeline.py
```

This will:
- Extract text, tables, and images from the PDF
- Create embeddings for all content
- Build a FAISS vector index

4. **Launch the Application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
multi-model_assignment/
├── app.py                    # Streamlit chat interface
├── config.py                 # Configuration and paths
├── document_processor.py     # PDF parsing and extraction
├── process_document.py       # Document processing script
├── create_embeddings.py      # Embedding generation script
├── vector_store.py           # FAISS vector store wrapper
├── llm_qa.py                 # LLM-based answer generation
├── run_pipeline.py           # End-to-end pipeline runner
├── requirements.txt          # Python dependencies
├── data/
│   ├── raw/                  # Input PDFs
│   ├── processed/            # Extracted chunks (JSON)
│   ├── images/               # Extracted images
│   └── vector_store/         # FAISS index files
├── TECHNICAL_REPORT.md       # Detailed technical documentation
└── README.md                 # This file
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Embedding model
EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'

# LLM model for answer generation
LLM_MODEL = 'google/flan-t5-base'

# File paths
PDF_PATH = 'data/raw/qatar_test_doc.pdf'
```

## 💡 Usage Examples

### Command Line Pipeline

```bash
# Step 1: Process document
python process_document.py

# Step 2: Create embeddings
python create_embeddings.py

# Step 3: Run the app
streamlit run app.py
```

### Programmatic Usage

```python
from vector_store import VectorStore
from llm_qa import LLMQA

# Load vector store
vector_store = VectorStore()
vector_store.load('data/vector_store/faiss_index')

# Search
results = vector_store.search("What is Qatar's GDP growth?", k=5)

# Generate answer
qa = LLMQA()
answer = qa.generate_answer_with_citations(
    "What is Qatar's GDP growth?", 
    results
)

print(answer['answer'])
for citation in answer['citations']:
    print(f"Source: {citation['source']}")
```

## 🧪 Testing

Test individual components:

```bash
# Test document processor
python document_processor.py

# Test vector store
python vector_store.py

# Test QA system
python llm_qa.py
```

## 📊 Performance

- **Document Processing**: ~30 seconds for 78-page PDF
- **Embedding Generation**: ~2 minutes for 697 chunks
- **Query Response Time**: <500ms average
- **Index Size**: ~2.5MB for 697 vectors

## 🔍 Technical Details

### Models Used
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
- **LLM**: google/flan-t5-base (248M parameters)
- **Vector DB**: FAISS (CPU optimized)

### Document Processing
- **Text Extraction**: PyMuPDF (fitz)
- **Table Detection**: Block-based extraction
- **OCR**: Tesseract (optional)

### Retrieval Strategy
- Semantic search using cosine similarity
- Top-k retrieval with relevance scoring
- Multi-modal result ranking

## 🐛 Troubleshooting

### OCR Not Working
Install Tesseract:
- **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
- **Mac**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

### Out of Memory
Reduce batch size in `create_embeddings.py` or use a smaller embedding model.

### Slow Performance
- Use GPU if available (update `device` in config)
- Reduce number of retrieved chunks (k parameter)
- Use a smaller LLM model

## 📧 Contact

## Name : Yash Tilwani
## Email : yashtilwani4@gmail.com
## Contact : +91 9039424683

---

**Built with**: LangChain, FAISS, Streamlit, HuggingFace Transformers
