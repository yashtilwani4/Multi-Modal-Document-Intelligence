# Streamlit Cloud Deployment Guide

## 📋 Pre-Deployment Checklist

### ✅ Required Files (All Present)
- [x] `app.py` - Main application file
- [x] `requirements.txt` - Python dependencies
- [x] `packages.txt` - System packages (tesseract-ocr)
- [x] `.streamlit/config.toml` - Streamlit configuration
- [x] All Python modules (config.py, vector_store.py, etc.)
- [x] Pre-processed data in `data/` folder

## 🚀 Deployment Steps

### Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Multi-Modal RAG QA System - Ready for deployment"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. **Go to**: https://share.streamlit.io/

2. **Sign in** with your GitHub account

3. **Click**: "New app"

4. **Configure**:
   - **Repository**: Select your GitHub repository
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `multi-model_assignment/multi-model_assignment/app.py`
   - **App URL**: Choose a custom URL (optional)

5. **Advanced settings** (click "Advanced settings"):
   - **Python version**: 3.11
   - **Secrets**: Not needed for this app
   
6. **Click**: "Deploy!"

### Step 3: Wait for Deployment

The deployment process will:
1. Install system packages from `packages.txt` (tesseract-ocr)
2. Install Python packages from `requirements.txt`
3. Load your pre-processed data
4. Start the application

**Expected time**: 5-10 minutes

## 📁 File Structure for Deployment

Your repository should have this structure:

```
your-repo/
└── multi-model_assignment/
    └── multi-model_assignment/
        ├── app.py                    ← Main file
        ├── requirements.txt          ← Dependencies
        ├── packages.txt              ← System packages
        ├── .streamlit/
        │   └── config.toml          ← Streamlit config
        ├── config.py
        ├── vector_store.py
        ├── llm_qa.py
        ├── document_processor.py
        └── data/
            ├── vector_store/         ← Pre-processed data
            │   ├── faiss_index/
            │   │   ├── index.faiss
            │   │   └── index.pkl
            │   └── faiss_index_chunks.pkl
            ├── processed/
            │   └── extracted_chunks.json
            └── images/               ← Extracted images
```

## ⚙️ Configuration

### Main File Path
```
multi-model_assignment/multi-model_assignment/app.py
```

### Python Version
```
3.11
```

### Requirements
All dependencies are in `requirements.txt`:
- streamlit
- langchain
- faiss-cpu
- sentence-transformers
- transformers
- torch
- etc.

### System Packages
Defined in `packages.txt`:
- tesseract-ocr (for OCR functionality)

## 🔧 Troubleshooting

### Issue: "No module named 'config'"

**Solution**: Ensure the main file path is correct:
```
multi-model_assignment/multi-model_assignment/app.py
```

### Issue: "Data not found"

**Solution**: Make sure the `data/` folder is committed to git:
```bash
git add data/vector_store/
git add data/processed/
git add data/images/
git commit -m "Add pre-processed data"
git push
```

### Issue: "Out of memory"

**Solution**: Streamlit Cloud has memory limits. The current setup should work, but if issues occur:
1. Use a smaller embedding model
2. Reduce the number of chunks
3. Consider upgrading to Streamlit Cloud Pro

### Issue: "App is slow to load"

**Solution**: This is normal on first load. The app needs to:
1. Download the embedding model (~90MB)
2. Load the vector store
3. Initialize the LLM

Subsequent loads will be faster due to caching.

### Issue: "LLM model fails to load"

**Solution**: The app has a fallback mechanism. It will use SimpleQA if the LLM fails to load. This is expected and the app will still work.

## 🎯 Post-Deployment

### Test Your Deployment

Once deployed, test with these queries:
1. "What is Qatar's economic growth?"
2. "What are the fiscal policy recommendations?"
3. "What is the banking sector situation?"

### Share Your App

Your app will be available at:
```
https://YOUR_APP_NAME.streamlit.app
```

Or:
```
https://share.streamlit.io/YOUR_USERNAME/YOUR_REPO/main/multi-model_assignment/multi-model_assignment/app.py
```

## 📊 Monitoring

### View Logs
- Click on "Manage app" in Streamlit Cloud
- View logs to debug issues
- Check resource usage

### Update Your App
```bash
# Make changes locally
git add .
git commit -m "Update app"
git push

# Streamlit Cloud will auto-deploy
```

## 🔒 Security Notes

### Public vs Private
- **Public**: Anyone can access your app
- **Private**: Only you and invited users (requires Streamlit Cloud Pro)

### Data Privacy
- Your pre-processed data is in the public repo
- No sensitive information should be in the code
- Use Streamlit secrets for API keys (if needed)

## 💡 Optimization Tips

### 1. Reduce Model Size
If deployment is slow, use a smaller model in `config.py`:
```python
EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'  # Current (90MB)
# Or use: 'sentence-transformers/paraphrase-MiniLM-L3-v2'  # Smaller (60MB)
```

### 2. Cache Loading
The app already uses Streamlit's session state for caching. No changes needed.

### 3. Lazy Loading
Models are loaded only when needed, which is already implemented.

## 📞 Support

If you encounter issues:
1. Check Streamlit Cloud logs
2. Review the error messages
3. Verify all files are committed
4. Ensure the main file path is correct

## ✅ Deployment Checklist

Before deploying, verify:
- [ ] All code files committed to GitHub
- [ ] `data/vector_store/` folder committed
- [ ] `requirements.txt` is up to date
- [ ] `packages.txt` includes tesseract-ocr
- [ ] `.streamlit/config.toml` is present
- [ ] Main file path is correct
- [ ] App works locally (`streamlit run app.py`)

## 🎉 Success!

Once deployed, your Multi-Modal RAG QA System will be live and accessible to anyone with the URL!

**Example URL**: https://multimodal-rag-qa.streamlit.app

---

**Need help?** Check the [Streamlit Community Forum](https://discuss.streamlit.io/)
