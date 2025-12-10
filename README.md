# AMP-Devs – Alumni Connect Platform

**AMP-Devs** is a Flask-based web platform that connects students with alumni for mentorship, networking, and career growth. Built to bridge the academic-to-career gap, the platform is designed with institutions and technical education in mind.

🌐 **Live Demo:** [https://alumniconnect-d7mo.onrender.com/](https://alumniconnect-d7mo.onrender.com/)

---

## 🚀 Features

- 🔐 **Secure Login & Signup** for students and alumni
- 🧑‍💼 **Alumni Directory** with searchable filters
- 🧭 **Mentorship Matching** based on skills & interests
- 🗓️ **Event Scheduler** for webinars and reunions
- 💬 **Discussion Forums** for knowledge sharing
- 📋 **Profile Dashboard** with personal insights

---

## 🛠 Tech Stack

- **Frontend:** HTML, CSS, Bootstrap
- **Backend:** Python, Flask
- **Database:** SQLite (`gradlink.db`)
- **Hosting:** Render.com

---

## 📦 Installation

```bash
git clone https://github.com/Techy-Play/AMP-Devs.git
cd AMP-Devs
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

App runs locally at: `http://localhost:5000`

---

## 📁 Project Structure

```
AMP-Devs/
├── app.py                # Main Flask application
├── models.py             # Database models
├── gradlink.db      # SQLite database
├── templates/            # HTML templates (Jinja2)
├── static/               # CSS, JS, images
├── requirements.txt      # Required Python packages
├── README.md             # This file
```

## 🌱 MVP & Roadmap

- ✅ User Login/Signup
- ✅ Alumni Listing & Filters
- ✅ Mentor Match System
- ⏳ Add chat or messaging (Next Update)
- ⏳ Admin Controls (Phase 2)

---

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit changes
4. Push and open a Pull Request

---

## ⚠️ AI Integration (Developer preview)

This project includes experimental AI features (RAG-based AskAlum, ATS resume scoring, and a DB-backed Mentor Compatibility Scorer). They are gated behind feature flags in `config/feature_flags.py`.

- To enable features for local testing, update `app.config['FEATURE_FLAGS']` or set the flags in `config/feature_flags.py`.
- Required (optional for dev): `OPENAI_API_KEY` environment variable for full RAG generation.
- Recommended dev-only packages (don't commit secrets):

```powershell
# activate venv
.\\venv\\Scripts\\Activate.ps1
pip install openai faiss-cpu numpy scikit-learn pdfminer.six python-docx spacy pytest
python -m spacy download en_core_web_sm
```

Notes:
- The repository includes a dev-friendly in-memory RAG index and `scripts/import_advice.py` to seed it from sample advice.
- The AI modules log and fail gracefully if optional dependencies are missing.
- Do not store `OPENAI_API_KEY` in the repo. Use environment variables or a secrets manager.


## 📃 License

Licensed under MIT. Free to use and extend.

---

## 👨‍💻 Developer

- **Lokesh Paneru**
  GitHub: [Techy-Play](https://github.com/Techy-Play)
  Project: [Alumni Connect (AMP-Devs)](https://alumniconnect-d7mo.onrender.com/)

---
