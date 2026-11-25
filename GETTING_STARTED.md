# 🚀 Getting Started with AIPS - 5 Minutes to Success

## ⚡ Super Quick Start

### Step 1: Get an API Key (2 minutes)
Choose one (Groq is faster):

**Option A: Groq (Recommended - 30 seconds)**
- Go to [groq.com](https://console.groq.com/keys)
- Sign up for free account
- Copy your API key

**Option B: Google Gemini**
- Go to [aistudio.google.com](https://aistudio.google.com)
- Click "Get API Key"
- Create new API key

### Step 2: Install & Run (3 minutes)

```bash
# Navigate to project
cd ai-interview-prep-suite

# On Windows - run this
setup.bat

# On Mac/Linux - run this
bash setup.sh

# After setup completes, run:
streamlit run frontend/app.py
```

### Step 3: Configure API (1 minute)
1. Open Streamlit app (appears in browser automatically)
2. Click the ▶ icon in top right → Settings
3. In sidebar, select your LLM provider
4. Paste your API key

**Done! 🎉 Start using the app.**

---

## 🎯 Feature Quick Tour

### Resume Builder (2 minutes)
1. Go to **Resume Builder** from sidebar
2. Fill in your profile (name, email, target role, etc.)
3. Click **Generate Resume**
4. Get AI-powered suggestions

### Interview Q&A (3 minutes)
1. Go to **Interview Q&A**
2. Select your role, experience level
3. Click **Generate Questions**
4. Practice answers and get feedback

### Study Concepts (2 minutes)
1. Go to **Study Concepts**
2. Select your role and experience level
3. Click **Load Study Path**
4. Browse organized topics by difficulty

### Mock Interview (5 minutes)
1. Go to **Mock Interview**
2. Set interview parameters
3. Click **Start Interview**
4. Answer each question
5. Get scoring and feedback

---

## 🛠️ Manual Setup (If setup.bat/sh doesn't work)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
pip install streamlit

# Create .env file
copy .env.example .env

# Edit .env with your API key
# (Open with any text editor)

# Run the app
streamlit run frontend/app.py
```

---

## 📋 Troubleshooting

### "Module not found" error
```bash
# Make sure you're in the project directory
cd ai-interview-prep-suite

# Reinstall dependencies
pip install -r backend/requirements.txt
pip install streamlit
```

### "API Key not working"
1. Double-check you copied the full key
2. Make sure you're using the right provider (Groq vs Gemini)
3. Check the API provider website - key might have expiration/usage limits

### Streamlit not opening in browser
```bash
# Manually open:
# http://localhost:8501
```

### Slow responses
- Use Groq API (faster than Gemini)
- Check your internet connection
- Make sure you have a valid API key with remaining quota

---

## 📊 Project Structure (For Reference)

```
ai-interview-prep-suite/
├── frontend/
│   └── app.py              ← Main app to run
├── backend/
│   ├── llm_service.py      ← LLM API calls
│   ├── resume_builder.py   ← Resume logic
│   ├── question_generator.py ← Interview logic
│   ├── study_concepts.py   ← Study material
│   ├── main.py             ← FastAPI backend (optional)
│   └── requirements.txt    ← Dependencies
├── data/
│   └── sample_data.py      ← Fallback data
├── README.md               ← Full documentation
├── DEPLOYMENT.md           ← Cloud deployment
└── .env.example            ← API keys template
```

---

## 🎯 Key Features

✅ **Resume Builder** - Generate ATS-friendly resumes  
✅ **Interview Q&A** - Practice with AI-generated questions  
✅ **Study Concepts** - Organized learning paths  
✅ **Mock Interview** - Realistic interview simulation  
✅ **AI Feedback** - Get detailed feedback on responses  
✅ **Performance Scoring** - Track your readiness  

---

## 💡 Pro Tips

1. **Start with Resume Builder** - It gives context to all other features
2. **Use Groq API** - Much faster than Gemini for this use case
3. **Practice multiple times** - Better understanding comes from repetition
4. **Review feedback carefully** - That's where the learning happens
5. **Try different roles** - See what resonates with you

---

## 🎓 Learning Resources

- **Groq API Docs:** https://groq.com/api
- **Streamlit Docs:** https://docs.streamlit.io
- **Streamlit Gallery:** https://streamlit.io/gallery
- **Interview Prep:** https://www.techinterviewhandbook.org

---

## ❓ FAQ

**Q: Do I need to pay for anything?**  
A: No! All APIs have free tiers. Groq and Gemini are free to use with generous rate limits.

**Q: Can I use this offline?**  
A: No, you need an internet connection for the LLM APIs. Local LLMs coming soon.

**Q: How long does resume generation take?**  
A: Usually 5-10 seconds with Groq, 10-15 seconds with Gemini.

**Q: Can I export my resume?**  
A: Yes! Copy-paste from the app or use PDF export (coming soon).

**Q: How many questions will be generated?**  
A: You can select 3-10 questions per session.

**Q: Is my data saved?**  
A: Currently only in your session. Data persistence coming soon.

---

## 📞 Need Help?

1. Check [README.md](README.md) for detailed docs
2. Review [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help
3. Check error messages - they usually tell you what's wrong
4. Ensure API keys are valid and have quota remaining

---

## 🚀 Next Steps

After initial setup:

1. **Customize for your role** - Edit backend/study_concepts.py to add more roles
2. **Add more questions** - Expand data/sample_data.py
3. **Deploy to cloud** - Follow DEPLOYMENT.md for Streamlit Cloud, Render, etc.
4. **Add database** - Store user data with SQLAlchemy + PostgreSQL
5. **Advanced features** - Add voice input, analytics dashboard, etc.

---

**Ready? Let's go! 🎯**

```bash
# One last command:
streamlit run frontend/app.py

# Then open: http://localhost:8501
```
