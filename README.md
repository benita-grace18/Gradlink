# Gradlink – AI-Powered Alumni–Student Mentorship and Career Guidance Platform

**Gradlink** is an intelligent Flask-based web platform that connects students with alumni for mentorship, networking, and career guidance. Powered by cutting-edge AI technology, Gradlink bridges the academic-to-career gap with smart matching, resume optimization, and personalized career advice.

**Created by:** Benita Grace

🌐 **Live Demo:** [https://gradlink.onrender.com/](https://gradlink.onrender.com/)

---

## 🚀 Features

- 🔐 **Secure Login & Signup** for students and alumni
- 🧑‍💼 **AI-Powered Alumni Directory** with intelligent search filters
- 🤖 **AI Mentor Matching (MCS)** - Database-backed skill-based mentor compatibility scoring
- 📄 **Resume Scorer (ATS)** - AI-powered resume analysis and skill detection
- 💡 **Ask Alumni (RAG)** - Retrieval-augmented generation for personalized career advice
- 🗓️ **Event Scheduler** for webinars and reunions
- 💬 **Discussion Forums** for knowledge sharing
- 📋 **Profile Dashboard** with personal insights and AI recommendations

---

## 🛠 Tech Stack

- **Frontend:** HTML5, CSS3, Bootstrap 5, Font Awesome
- **Backend:** Python 3.13, Flask 2.3.3
- **AI/ML:** OpenAI API, FAISS (semantic search), scikit-learn (TF-IDF), spaCy
- **Document Processing:** pdfminer.six, python-docx
- **Database:** SQLite (`gradlink.db`), SQLAlchemy ORM
- **Hosting:** Render.com
- **Testing:** Pytest

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/benita-grace18/Gradlink.git
cd Gradlink

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model (for AI features)
python -m spacy download en_core_web_sm

# Run the application
python app.py
```

App runs locally at: `http://localhost:5000`

---

## 📁 Project Structure

```
Gradlink/
├── app.py                          # Main Flask application
├── models.py                       # SQLAlchemy database models
├── gradlink.db                     # SQLite database
├── config/
│   └── feature_flags.py            # Feature toggles for AI features
├── extensions/
│   ├── ai/
│   │   ├── rag_faiss.py           # RAG module (Ask Alumni)
│   │   └── ats.py                 # ATS module (Resume Scorer)
│   ├── matching/
│   │   └── db_mcs.py              # Mentor Compatibility Scorer
│   ├── ask_alum/                  # Ask Alumni blueprint
│   ├── resume/                    # Resume upload & scoring blueprint
│   └── ...other blueprints
├── templates/                      # Jinja2 HTML templates
├── static/                         # CSS, JavaScript, images
├── scripts/
│   └── import_advice.py            # RAG index seeder
├── tests/                          # Pytest test suite
├── requirements.txt                # Python dependencies
└── AI_INTEGRATION_GUIDE.md         # Comprehensive AI setup guide
```

## 🤖 AI Features Explained

### 1. Ask Alumni (RAG - Retrieval Augmented Generation)

- Provides personalized career advice from an alumni knowledge base
- Uses OpenAI embeddings for semantic search
- FAISS index for efficient vector similarity search
- Graceful fallback when OpenAI API is unavailable
- **Endpoint:** `POST /ask/rag`

### 2. Resume Scorer (ATS - Applicant Tracking System)

- Analyzes resumes (PDF, DOCX, TXT formats)
- Detects technical and soft skills
- Uses TF-IDF vectorization for skill matching
- Returns compatibility score with job requirements
- **Endpoint:** `POST /resume/`

### 3. Mentor Compatibility Scorer (MCS)

- Matches students with alumni mentors based on skills
- Database-backed mentor profiles with availability
- Considers timezone and availability constraints
- TF-IDF skill vector similarity for matching
- **Endpoint:** `GET /mcs/recommend`

## 🌱 MVP & Roadmap

- ✅ User Login/Signup with role-based access
- ✅ Alumni Directory with AI-powered search
- ✅ AI Mentor Matching System (MCS)
- ✅ Resume Scoring & Skill Detection (ATS)
- ✅ Career Advice from Alumni (RAG)
- ✅ Event Scheduler for webinars and reunions
- ⏳ Real-time messaging/chat between mentors and mentees (Phase 2)
- ⏳ Advanced analytics dashboard (Phase 2)
- ⏳ Mobile app (Phase 3)
- ⏳ Enterprise admin controls (Phase 3)

---

## 🤝 Contributing

We welcome contributions! To contribute:

1. Fork the project (https://github.com/benita-grace18/Gradlink)
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🔐 AI Features Configuration

All AI features are gated behind feature flags in `config/feature_flags.py`:

```python
app.config['FEATURE_FLAGS'] = {
    'NEW_THEME': True,              # Modern UI theme
    'RESUME_UPLOAD': True,          # ATS resume scoring
    'MCS_RECOMMENDER': True,        # Mentor compatibility scorer
    'ASK_ALUM': True               # RAG-based career advice
}
```

### Setup AI Features

1. **Install optional AI packages:**

```bash
pip install openai faiss-cpu spacy
python -m spacy download en_core_web_sm
```

2. **Add OpenAI API key (for RAG):**

```bash
# Create .env file
echo "OPENAI_API_KEY=your_key_here" > .env
```

3. **Run the app:**

```bash
python app.py
# Visit http://localhost:5000
# Click on AI feature buttons: Ask Alumni, Resume Scorer, Find Mentors
```

### AI Module Features

- **Graceful Fallbacks:** All AI modules work offline with fallback responses
- **No Required Secrets:** Runs without OpenAI key (uses static responses)
- **Tested & Verified:** All endpoints tested and working
- **Production Ready:** Proper error handling and logging

---

## 📊 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_ats.py

# Run with coverage
pytest --cov=extensions tests/

# Integration tests
python test_ai_integration.py
python test_home_page_ai.py
```

---

## 👩‍💼 Author

**Benita Grace**

- GitHub: [@benita-grace18](https://github.com/benita-grace18)
- Project: [Gradlink - AI-Powered Mentorship Platform](https://github.com/benita-grace18/Gradlink)

---

## 📄 License

Licensed under the MIT License. See LICENSE file for details.

Free to use, modify, and extend for personal and commercial projects.

---

## 📞 Support & Feedback

For issues, feature requests, or feedback:

- Open an issue on [GitHub Issues](https://github.com/benita-grace18/Gradlink/issues)
- Check [AI Integration Guide](AI_INTEGRATION_GUIDE.md) for technical documentation

---

## 🙏 Acknowledgments

- Built with Flask and modern AI/ML technologies
- UI/UX inspired by leading edtech platforms
- Community feedback and contributions
- All open-source libraries and tools used

---

## 👨‍💻 Developer

- **Lokesh Paneru**
  GitHub: [Techy-Play](https://github.com/Techy-Play)
  Project: [Alumni Connect (AMP-Devs)](https://alumniconnect-d7mo.onrender.com/)

---
