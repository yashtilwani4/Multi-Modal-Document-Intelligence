# Deployment Guide - Multi-Modal RAG QA System

## Quick Start (Local Development)

### Prerequisites
```bash
# Python 3.8 or higher
python --version

# pip package manager
pip --version
```

### Installation Steps

1. **Clone/Download the project**
```bash
cd multi-model_assignment
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Place your PDF document**
```bash
# Put your PDF in: data/raw/qatar_test_doc.pdf
# Or update the path in config.py
```

4. **Run the processing pipeline**
```bash
python run_pipeline.py
```

5. **Launch the application**
```bash
streamlit run app.py
```

6. **Access the application**
```
Open browser: http://localhost:8501
```

## Production Deployment

### Option 1: Docker Deployment (Recommended)

**Create Dockerfile:**
```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build and run:**
```bash
docker build -t multimodal-rag .
docker run -p 8501:8501 -v $(pwd)/data:/app/data multimodal-rag
```

### Option 2: Cloud Deployment (Streamlit Cloud)

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Multi-modal RAG system"
git push origin main
```

2. **Deploy on Streamlit Cloud**
- Go to https://share.streamlit.io
- Connect your GitHub repository
- Select the main branch and `app.py`
- Deploy!

**Note:** Pre-process documents locally and commit the vector store to avoid processing on cloud.

### Option 3: AWS Deployment

**Using EC2:**
```bash
# Launch EC2 instance (t3.medium or larger)
# SSH into instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install dependencies
sudo yum update -y
sudo yum install python3 python3-pip tesseract -y

# Clone and setup
git clone your-repo
cd multi-model_assignment
pip3 install -r requirements.txt

# Run with nohup
nohup streamlit run app.py --server.port=8501 &
```

**Using ECS (Container):**
- Build Docker image
- Push to ECR
- Create ECS task definition
- Deploy as ECS service

### Option 4: Azure Deployment

**Using Azure App Service:**
```bash
# Install Azure CLI
az login

# Create resource group
az group create --name rag-system --location eastus

# Create App Service plan
az appservice plan create --name rag-plan --resource-group rag-system --sku B1 --is-linux

# Create web app
az webapp create --resource-group rag-system --plan rag-plan --name multimodal-rag --runtime "PYTHON:3.11"

# Deploy
az webapp up --name multimodal-rag --resource-group rag-system
```

## Environment Configuration

### Environment Variables

Create `.env` file:
```bash
# Model Configuration
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL=google/flan-t5-base

# Paths
PDF_PATH=data/raw/qatar_test_doc.pdf
VECTOR_STORE_PATH=data/vector_store/faiss_index

# Performance
MAX_CHUNKS=1000
SEARCH_K=5

# API Keys (if using cloud models)
OPENAI_API_KEY=your-key-here
HUGGINGFACE_TOKEN=your-token-here
```

### Production Settings

Update `config.py` for production:
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Use environment variables
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
LLM_MODEL = os.getenv('LLM_MODEL', 'google/flan-t5-base')

# Enable caching
ENABLE_CACHE = True
CACHE_TTL = 3600  # 1 hour
```

## Performance Optimization

### 1. Model Optimization

**Use quantized models:**
```python
# In vector_store.py
from optimum.onnxruntime import ORTModelForFeatureExtraction

model = ORTModelForFeatureExtraction.from_pretrained(
    model_name,
    export=True,
    provider="CPUExecutionProvider"
)
```

### 2. Caching

**Add Redis caching:**
```python
import redis
import hashlib

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cached_search(query, k=5):
    cache_key = hashlib.md5(f"{query}:{k}".encode()).hexdigest()
    cached = redis_client.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    results = vector_store.search(query, k)
    redis_client.setex(cache_key, 3600, json.dumps(results))
    return results
```

### 3. Load Balancing

**Use Nginx:**
```nginx
upstream streamlit {
    server localhost:8501;
    server localhost:8502;
    server localhost:8503;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://streamlit;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Monitoring & Logging

### Application Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Metrics Collection

```python
from prometheus_client import Counter, Histogram

query_counter = Counter('queries_total', 'Total queries processed')
query_latency = Histogram('query_latency_seconds', 'Query latency')

@query_latency.time()
def process_query(query):
    query_counter.inc()
    # Process query
    return results
```

## Security Considerations

### 1. API Authentication

```python
import streamlit as st

def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if check_password():
    # Show app
    pass
```

### 2. Rate Limiting

```python
from functools import wraps
import time

def rate_limit(max_calls=10, time_window=60):
    calls = []
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [c for c in calls if c > now - time_window]
            
            if len(calls) >= max_calls:
                raise Exception("Rate limit exceeded")
            
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## Backup & Recovery

### Backup Strategy

```bash
# Backup vector store
tar -czf backup-$(date +%Y%m%d).tar.gz data/vector_store/

# Backup to S3
aws s3 cp backup-$(date +%Y%m%d).tar.gz s3://your-bucket/backups/
```

### Recovery

```bash
# Restore from backup
tar -xzf backup-20241123.tar.gz

# Or rebuild from source
python run_pipeline.py
```

## Troubleshooting

### Common Issues

**Issue: Out of memory**
```bash
# Solution: Increase swap space or use smaller model
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
```

**Issue: Slow queries**
```bash
# Solution: Reduce k value or optimize index
# In vector_store.py, use IVF index for large datasets
```

**Issue: Port already in use**
```bash
# Solution: Change port
streamlit run app.py --server.port=8502
```

## Maintenance

### Regular Tasks

1. **Update dependencies** (monthly)
```bash
pip list --outdated
pip install -U package-name
```

2. **Clean cache** (weekly)
```bash
rm -rf ~/.cache/huggingface/
```

3. **Monitor disk space**
```bash
df -h
du -sh data/
```

4. **Review logs**
```bash
tail -f app.log
```

## Scaling Considerations

### Horizontal Scaling
- Deploy multiple instances behind load balancer
- Use shared vector store (Redis or Elasticsearch)
- Implement distributed caching

### Vertical Scaling
- Increase instance size (more RAM/CPU)
- Use GPU instances for faster inference
- Optimize batch processing

---

**For support or questions, refer to the technical documentation or contact the development team.**
