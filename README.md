# 🇪🇺 EU AI Act Risk Classifier

> Classify AI systems under the **EU AI Act** (Unacceptable, High, Limited, Minimal risk tiers).  
> Generates a **compliance checklist** and an **audit‑ready PDF report** – perfect for demonstrating your ability to translate complex regulations into technical frameworks.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red.svg)
![WeasyPrint](https://img.shields.io/badge/WeasyPrint-61.2-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🎯 Why This Project

- **Regulatory compliance** – translate the EU AI Act into executable rules.  
- **Dynamic risk assessment** – 10+ questionnaire questions covering use case, data, human oversight, transparency, and risk.  
- **Audit‑ready output** – generates a structured PDF report with compliance gaps and actionable recommendations.  
- **Rules‑based engine** – uses weighted scoring and risk triggers to map answers to risk tiers.  
- **Production‑ready** – FastAPI backend, Streamlit frontend, and PDF generation out‑of‑the‑box.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **📝 Dynamic Questionnaire** | 10 questions grouped into categories (Use Case, Data, Human Oversight, Transparency, Risk) |
| **⚖️ Risk Classification** | Maps answers to EU AI Act risk tiers: Unacceptable, High, Limited, Minimal |
| **📊 Weighted Scoring** | Each answer contributes a weight; risk triggers boost the score |
| **📋 Compliance Gaps** | Identifies specific Articles (5, 9, 10, 13, 14) with severity and remediation steps |
| **💡 Recommendations** | Actionable next steps tailored to the classification |
| **📄 PDF Report** | Professional, branded report with system overview, classification, gaps, and recommendations |
| **📜 History** | Stores all assessments for audit and review |
| **🔗 RESTful API** | Endpoints for questions, classification, history, and report download |

---

## 🧠 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (Streamlit)                  │
│  ┌─────────────┐  ┌─────────────┐  ┌────────────────────┐  │
│  │ Question-   │  │ Results &   │  │ History & Report   │  │
│  │ naire       │  │ Dashboard   │  │ Download           │  │
│  └─────────────┘  └─────────────┘  └────────────────────┘  │
└────────────────────────────┬─────────────────────────────────┘
                             │ HTTP
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                  API Routers                        │    │
│  │   /api/classify (questions, classify, history)     │    │
│  └────────────────────┬────────────────────────────────┘    │
│                       │                                      │
│  ┌────────────────────▼────────────────────────────────┐   │
│  │              Services Layer                         │   │
│  │  ┌─────────────┐ ┌──────────────┐ ┌─────────────┐  │   │
│  │  │Rules Engine │ │ Report       │ │ Database    │  │   │
│  │  │(classifier) │ │ Generator    │ │ (SQLite)    │  │   │
│  │  └─────────────┘ └──────────────┘ └─────────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
│                       │                                    │
│  ┌────────────────────▼────────────────────────────────┐  │
│  │              Database (SQLite / Postgres)           │  │
│  │   - AIRiskAssessment (answers, classification, gaps)│  │
│  └─────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

---

## 🛠 Tech Stack

- **Backend**: FastAPI, SQLAlchemy, Pydantic  
- **Rules Engine**: `business-rules` library with custom thresholds  
- **PDF Generation**: WeasyPrint + Jinja2 HTML templates  
- **Frontend**: Streamlit, Requests, JSON viewer  
- **Database**: SQLite (default), can be switched to PostgreSQL  
- **Containerisation**: Docker & Docker Compose  

---

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.10+
- (Optional) Docker & Docker Compose

### 1. Clone the repository
```bash
git clone https://github.com/haiderasad2000-source/EU-AI-Act-Risk-Classifier.git
cd eu_ai_risk_classifier
```

### 2. Set up environment variables
Copy the example environment file:
```bash
cp backend/.env.example backend/.env
```
(Optionally adjust `DATABASE_URL` or `DRAFT_VERSION`.)

### 3. Run with the quick‑start script (Unix)
```bash
chmod +x run.sh
./run.sh
```
This will:
- Install Python dependencies
- Launch the FastAPI backend (port 8000)
- Launch the Streamlit frontend (port 8501)

### 4. Access the dashboard
Open your browser at [http://localhost:8501](http://localhost:8501)

---

## 🐳 Run with Docker

```bash
docker-compose up --build
```
This spins up both backend and frontend services.

---

## ⚙️ Configuration

Environment variables in `backend/.env`:

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | SQLAlchemy database URL (default: SQLite) |
| `DRAFT_VERSION` | Version tag for the report (default: EU-AI-Act-v1.1) |
| `USE_MOCK_CLASSIFIER` | (Reserved) for future mock mode |

---

## 📡 API Endpoints

### `GET /api/classify/questions`
Get the full questionnaire with all questions, options, and weights.

**Response**: List of `Question` objects.

---

### `POST /api/classify`
Submit answers and get a classification.

**Request body**:
```json
{
  "system_name": "HARP-AI",
  "system_description": "Transaction monitoring system",
  "answers": {
    "q1": "safety_critical",
    "q2": "yes",
    "q3": "biometric",
    "q4": "yes_unknown",
    "q5": "none",
    "q6": "no",
    "q7": "no",
    "q8": "no",
    "q9": "high",
    "q10": "healthcare"
  }
}
```

**Response**: Full `ClassificationResponse` with risk tier, score, compliance gaps, recommendations, and report URL.

---

### `GET /api/classify/history`
List previous assessments.

**Query parameters**:
- `limit` (int, default 20)

---

### `GET /api/classify/{assessment_id}/report`
Download the PDF report for a specific assessment.

---

## 📊 Frontend Dashboard

The Streamlit UI provides:

- **Questionnaire** – all questions grouped by category with radio/select inputs.
- **Classification Results** – risk tier badge, score bar, compliance gaps, and recommendations.
- **History Sidebar** – quick access to past assessments and report downloads.
- **Downloadable PDF** – one‑click export of the full audit report.

---

## 🧪 Example Test

Try answering as follows to trigger a **High** or **Unacceptable** risk classification:

| Question ID | Answer |
| :--- | :--- |
| q1 (Purpose) | `safety_critical` |
| q2 (Legal rights) | `yes` |
| q3 (Data type) | `biometric` |
| q4 (Bias) | `yes_unknown` |
| q5 (Oversight) | `none` |
| q6 (Override) | `no` |
| q7 (Explainability) | `no` |
| q8 (Disclosure) | `no` |
| q9 (Harm) | `high` |
| q10 (Sector) | `healthcare` |

**Expected classification:** 🔴 **UNACCEPTABLE** or 🟠 **HIGH**, with compliance gaps for Articles 5, 9, 10, 13, and 14.

---

## 🔌 Extending the System

- **Add new questions** – modify the question bank in `rules/questions.py`.  
- **Adjust risk thresholds** – update the `risk_thresholds` dictionary in `rules/engine.py`.  
- **Add more compliance gaps** – extend the `_generate_gaps` method.  
- **Customise the PDF report** – edit `templates/report_template.html` and the CSS.  
- **Integrate with bias scanners** – feed fairness metrics into the questionnaire.  

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or pull request for new features, bug fixes, or improvements.

---

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## 📬 Contact & Support

Built by [Asad Haider](https://github.com/haiderasad2000-source) – feel free to reach out for questions or collaborations.

---

**Classify with confidence!** ⚖️
