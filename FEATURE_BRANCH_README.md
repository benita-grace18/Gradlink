# GradLink Safe Additions Feature Branch

## Overview

This feature branch (`feat/gradlink-safe-additions`) adds **four isolated, non-invasive blueprints** to the AMP-Devs platform with feature flags for safe, reversible deployment.

### What's Included

#### 1. **Resume Upload & ATS Analysis** (`/resume/`)

- Upload resumes (PDF, DOCX, DOC, TXT)
- Simple ATS-like scoring (60% keyword matching + 40% section detection)
- Feedback on missing sections and keywords
- **Route**: `GET/POST /resume/`
- **Feature Flag**: `FEATURE_RESUME_UPLOAD`

#### 2. **Mentor Compatibility Scoring (MCS)** (`/mcs/recommend`)

- Content similarity scoring (cosine similarity via numpy/sklearn)
- Logistical feasibility (timezone + availability matching)
- Collaborative filtering (historical match quality)
- Weighted recommendation: 40% content + 40% logistics + 20% CF
- **Route**: `GET /mcs/recommend`
- **Feature Flag**: `FEATURE_MCS`

#### 3. **AskAlum - Career Advice Search** (`/ask/`)

- Simple full-text search across alumni advice
- Extensible to DB queries (currently in-memory demo data)
- **Route**: `GET/POST /ask/`
- **Feature Flag**: `FEATURE_ASK_ALUM`

#### 4. **New Theme (Optional CSS)**

- Modern design with card-based layout
- Segoe UI typography, subtle shadows
- **Template**: `templates/new_base.html`
- **Feature Flag**: `FEATURE_NEW_THEME`

---

## File Structure

```
config/
  feature_flags.py                 # Feature flag configuration

extensions/
  resume/
    __init__.py                    # Blueprint definition
    views.py                       # Upload + ATS scoring logic
    templates/resume/
      upload.html                  # Upload form
      result.html                  # Analysis results

  matching/
    __init__.py                    # Blueprint definition
    mcs.py                         # Scoring algorithms
    views.py                       # Recommendation route
    templates/mcs/
      recommend.html               # Demo results page

  ask_alum/
    __init__.py                    # Blueprint definition
    views.py                       # Search logic
    templates/ask/
      form.html                    # Search form + results

static/css/
  new-theme.css                    # Demo theme stylesheet

templates/
  new_base.html                    # Alternate base template
```

---

## How to Use

### 1. Enable Features Locally

Set environment variables (PowerShell):

```powershell
$env:FEATURE_RESUME_UPLOAD='true'
$env:FEATURE_MCS='true'
$env:FEATURE_ASK_ALUM='true'
$env:FEATURE_NEW_THEME='false'   # Set 'true' to use new theme
$env:FLASK_APP='app.py'
$env:FLASK_ENV='development'
```

### 2. Run the App

```powershell
.\venv\Scripts\python.exe app.py
```

### 3. Visit Demo Routes

- **Resume**: http://localhost:5000/resume/
- **MCS**: http://localhost:5000/mcs/recommend
- **AskAlum**: http://localhost:5000/ask/

---

## Technical Details

### Feature Flags

Defined in `config/feature_flags.py`:

```python
FEATURE_FLAGS = {
    "NEW_THEME": os.getenv("FEATURE_NEW_THEME", "false").lower() == "true",
    "RESUME_UPLOAD": os.getenv("FEATURE_RESUME_UPLOAD", "false").lower() == "true",
    "MCS_RECOMMENDER": os.getenv("FEATURE_MCS", "false").lower() == "true",
    "ASK_ALUM": os.getenv("FEATURE_ASK_ALUM", "false").lower() == "true",
}
```

Each route checks its flag and returns 404 if disabled.

### Blueprint Registration

In `app.py`:

```python
from config.feature_flags import FEATURE_FLAGS
app.config['FEATURE_FLAGS'] = FEATURE_FLAGS

app.register_blueprint(resume_bp)
app.register_blueprint(mcs_bp)
app.register_blueprint(ask_bp)
```

### Dependencies

- numpy
- scikit-learn

Install with:

```powershell
.\venv\Scripts\python.exe -m pip install numpy scikit-learn
```

---

## Deployment Strategy

### Staging/QA

1. Merge this branch to `develop` or `staging`
2. Set feature flags to `true` in `.env` file
3. Test each route thoroughly
4. Verify no conflicts with existing features

### Production

1. Merge to `main` when ready
2. **All features default to OFF** (flags set to `false`)
3. Enable features selectively via environment variables
4. Monitor error logs for issues

### Rollback

If an issue arises:

```powershell
# Option 1: Disable via environment variable
$env:FEATURE_RESUME_UPLOAD='false'
$env:FEATURE_MCS='false'
$env:FEATURE_ASK_ALUM='false'

# Option 2: Revert commit
git revert <commit-hash>

# Option 3: Switch branch
git checkout main
```

---

## Future Enhancements

### Resume Upload

- [ ] PDF/DOCX text extraction (pdfminer, python-docx)
- [ ] DB storage of resume metadata
- [ ] Job matching against postings
- [ ] User profile integration

### MCS

- [ ] Load student/mentor vectors from DB
- [ ] Real historical match data
- [ ] A/B testing on weighting (alpha, beta, gamma)
- [ ] API for integration with matching dashboard

### AskAlum

- [ ] Query DB table of verified alumni advice
- [ ] RAG (Retrieval-Augmented Generation) fallback
- [ ] Upvoting/rating of answers
- [ ] Escalation to mentors for unanswered questions

### Theme

- [ ] Conditional inclusion in `base.html` via feature flag
- [ ] Dark mode variant
- [ ] Accessibility audit (WCAG 2.1 AA)

---

## Testing Checklist

- [ ] Feature flags load correctly
- [ ] Each blueprint registers without errors
- [ ] Routes return 404 when feature disabled
- [ ] Upload endpoint accepts valid files
- [ ] ATS scoring logic works correctly
- [ ] MCS calculations are reasonable
- [ ] AskAlum search functions properly
- [ ] Static files (CSS) load correctly
- [ ] No console errors in browser
- [ ] App restarts cleanly after changes

---

## Commits on This Branch

```
63a84f4 feat: add accessibility labels and proper HTML5 structure
0711579 refactor: align all files with specification exactly
a4f4cea fix: resolve all HTML validation errors in templates
55e6a2e docs: add environment variables example
f9600b4 feat: add isolated resume, mcs, ask_alum blueprints + feature flags
```

---

## Contact & Support

- **Feature Owner**: GradLink Team
- **Branch**: `feat/gradlink-safe-additions`
- **Status**: Ready for PR and review
- **Risk Level**: Low (isolated blueprints, feature-flagged, no DB changes)

---

## Notes

- Validator warnings on Jinja2 templates are normal (HTML validators are strict with template syntax)
- All templates are functionally correct and will render properly at runtime
- The app boots cleanly with all features enabled or disabled
- No breaking changes to existing routes or models
