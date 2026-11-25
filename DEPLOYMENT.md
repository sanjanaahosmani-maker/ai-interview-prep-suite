# Deployment Guide - AI Interview Prep Suite

## 🚀 Local Development

### 1. Prerequisites
- Python 3.8+
- pip package manager
- API key from Groq or Google Gemini

### 2. Installation

```bash
# Clone/download project
cd ai-interview-prep-suite

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Unix/Mac:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
pip install streamlit

# Configure API keys
cp .env.example .env
# Edit .env and add your API keys
```

### 3. Run Application

```bash
# Terminal 1: Streamlit Frontend
streamlit run frontend/app.py

# Terminal 2 (Optional): FastAPI Backend
cd backend
python -m uvicorn main:app --reload
```

Access at: `http://localhost:8501`

---

## ☁️ Cloud Deployment

### Option 1: Streamlit Cloud (Easiest)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Connect your GitHub repository
5. Select `frontend/app.py` as the main file
6. Add secrets:
   - Go to Advanced settings
   - Add `GROQ_API_KEY` or `GEMINI_API_KEY`

**Pros:** 
- Free tier available
- Easy to deploy
- Automatic updates from GitHub

**Cons:** 
- Shared infrastructure
- Rate limits

### Option 2: Render.com (Backend)

```bash
# Create requirements.txt for backend
pip freeze > requirements.txt

# Create Procfile
echo "web: python -m uvicorn backend.main:app" > Procfile
```

1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python -m uvicorn backend.main:app --host 0.0.0.0`
5. Add environment variables:
   - `GROQ_API_KEY` or `GEMINI_API_KEY`

### Option 3: Docker & Heroku

#### Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt backend/requirements.txt
COPY frontend/requirements.txt frontend/requirements.txt
RUN pip install -r backend/requirements.txt && \
    pip install -r frontend/requirements.txt && \
    pip install streamlit

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501"]
```

#### Deploy to Heroku
```bash
# Install Heroku CLI
# Login
heroku login

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set GROQ_API_KEY=your_key
# or
heroku config:set GEMINI_API_KEY=your_key

# Deploy
git push heroku main

# Open app
heroku open
```

### Option 4: DigitalOcean App Platform

1. Go to [DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform)
2. Create new app from GitHub
3. Configure build and run commands
4. Add environment variables
5. Deploy

---

## 🔧 Production Considerations

### 1. Environment Variables
```bash
# Use environment variables for sensitive data
export GROQ_API_KEY=your_key
export GEMINI_API_KEY=your_key
export APP_ENV=production
```

### 2. Rate Limiting
Add rate limiting to backend:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/resume/generate")
@limiter.limit("10/minute")
async def generate_resume(request: Request, profile: UserProfile):
    ...
```

### 3. Monitoring & Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("Resume generation started")
```

### 4. Database Setup (for storing user data)
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Production database
DATABASE_URL = "postgresql://user:password@db_host:5432/aips_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

### 5. Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_study_path(role: str, level: str):
    # Cached results
    pass
```

### 6. API Authentication
```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/api/resume/generate")
async def generate_resume(credentials: HTTPAuthCredentials = Depends(security)):
    # Verify token
    ...
```

---

## 📊 Performance Optimization

### 1. Response Caching
```python
from fastapi_cache2 import FastAPICache2
from fastapi_cache2.backends.redis import RedisBackend

# Enable Redis caching
@cached(expire=3600)
@app.get("/api/study/{role}/{level}")
async def get_study_path(role: str, level: str):
    ...
```

### 2. Async Processing
```python
from celery import Celery

app_celery = Celery('aips', broker='redis://localhost:6379')

@app_celery.task
def generate_resume_async(profile_id):
    # Long-running task
    pass
```

### 3. Database Indexing
```python
# Create indexes for frequently queried fields
CREATE INDEX idx_role ON interview_questions(role);
CREATE INDEX idx_user_id ON user_sessions(user_id);
```

---

## 🔐 Security Best Practices

1. **Never commit API keys** - Use `.env` files and `.gitignore`
2. **HTTPS only** - Use SSL certificates in production
3. **Input validation** - Validate all user inputs
4. **Rate limiting** - Prevent abuse
5. **CORS properly configured** - Only allow trusted origins
6. **SQL injection prevention** - Use parameterized queries
7. **Keep dependencies updated** - Run `pip list --outdated`

---

## 📈 Scaling Strategy

### Phase 1: MVP (Current)
- Streamlit frontend
- Python backend
- Groq/Gemini API

### Phase 2: Improved Performance
- Add caching layer (Redis)
- Database for storing user data (PostgreSQL)
- API authentication

### Phase 3: Enterprise
- Microservices architecture
- Load balancing
- Multi-region deployment
- Advanced monitoring

---

## 🆘 Troubleshooting

### Issue: Streamlit connection timeout
**Solution:** Increase timeout in `.streamlit/config.toml`
```toml
[client]
toolbarMode = "minimal"
showErrorDetails = true

[server]
runOnSave = true
maxUploadSize = 200
```

### Issue: LLM API rate limit exceeded
**Solution:** Implement retry logic with exponential backoff
```python
import time
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential())
def call_llm_with_retry(prompt):
    return llm_service.call_llm(prompt)
```

### Issue: Memory issues with large datasets
**Solution:** Use data generators and chunking
```python
def process_large_file(file_path, chunk_size=1000):
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # Process chunk
        yield process_chunk(chunk)
```

---

## 📞 Support & Resources

- **Groq Documentation:** https://groq.com/api
- **Google Gemini:** https://ai.google.dev
- **Streamlit Docs:** https://docs.streamlit.io
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Render Deployment:** https://render.com/docs

---

## ✅ Deployment Checklist

- [ ] API keys configured
- [ ] Environment variables set
- [ ] Dependencies installed
- [ ] Database initialized
- [ ] Tests passing
- [ ] Logging configured
- [ ] Error handling implemented
- [ ] Security headers added
- [ ] Rate limiting enabled
- [ ] Monitoring setup
- [ ] Documentation updated
- [ ] Performance tested
