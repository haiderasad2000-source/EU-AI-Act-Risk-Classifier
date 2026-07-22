from typing import List, Dict

QUESTION_BANK: List[Dict] = [
    {
        "id": "q1",
        "text": "What is the primary purpose of the AI system?",
        "category": "Use Case",
        "help_text": "Select the closest match to your system's main function.",
        "options": [
            {"value": "safety_critical", "label": "Safety-critical infrastructure (transport, energy, healthcare)", "weight": 0.9, "is_risk_trigger": True},
            {"value": "employment", "label": "Employment / HR decisions (recruitment, promotion)", "weight": 0.8, "is_risk_trigger": True},
            {"value": "education", "label": "Education (admissions, grading, assessment)", "weight": 0.7, "is_risk_trigger": True},
            {"value": "law_enforcement", "label": "Law enforcement / justice system", "weight": 0.85, "is_risk_trigger": True},
            {"value": "credit", "label": "Credit scoring / financial decisions", "weight": 0.7, "is_risk_trigger": True},
            {"value": "general_purpose", "label": "General purpose (customer service, productivity, content generation)", "weight": 0.3, "is_risk_trigger": False},
            {"value": "entertainment", "label": "Entertainment / creative content", "weight": 0.1, "is_risk_trigger": False}
        ]
    },
    {
        "id": "q2",
        "text": "Does the AI system make decisions that affect individuals' legal rights or access to essential services?",
        "category": "Use Case",
        "options": [
            {"value": "yes", "label": "Yes", "weight": 0.9, "is_risk_trigger": True},
            {"value": "no", "label": "No", "weight": 0.1, "is_risk_trigger": False}
        ]
    },
    {
        "id": "q3",
        "text": "What type of data does the AI system use?",
        "category": "Data",
        "help_text": "Select all that apply (multiple selection).",
        "options": [
            {"value": "biometric", "label": "Biometric data (faces, fingerprints, voice)", "weight": 0.9, "is_risk_trigger": True},
            {"value": "personal", "label": "Personal identifying information (names, addresses)", "weight": 0.6, "is_risk_trigger": False},
            {"value": "sensitive", "label": "Sensitive data (health, racial, political, religious)", "weight": 0.8, "is_risk_trigger": True},
            {"value": "public", "label": "Publicly available data", "weight": 0.2, "is_risk_trigger": False},
            {"value": "synthetic", "label": "Synthetic / anonymized data", "weight": 0.1, "is_risk_trigger": False}
        ]
    },
    {
        "id": "q4",
        "text": "Does the training data contain historical biases or underrepresentation of certain groups?",
        "category": "Data",
        "options": [
            {"value": "yes_known", "label": "Yes, and we have documented it", "weight": 0.6, "is_risk_trigger": True},
            {"value": "yes_unknown", "label": "Yes, but we haven't fully assessed", "weight": 0.8, "is_risk_trigger": True},
            {"value": "no", "label": "No, our data is representative", "weight": 0.1, "is_risk_trigger": False}
        ]
    },
    {
        "id": "q5",
        "text": "What level of human oversight exists for the AI system?",
        "category": "Human Oversight",
        "options": [
            {"value": "none", "label": "No human oversight (fully autonomous)", "weight": 0.9, "is_risk_trigger": True},
            {"value": "review", "label": "Human review of outputs (but decisions are automated)", "weight": 0.5, "is_risk_trigger": False},
            {"value": "approval", "label": "Human approval required for all major decisions", "weight": 0.2, "is_risk_trigger": False},
            {"value": "human_in_loop", "label": "Human-in-the-loop (AI assists, human decides)", "weight": 0.1, "is_risk_trigger": False}
        ]
    },
    {
        "id": "q6",
        "text": "Can a human override the AI system's decisions?",
        "category": "Human Oversight",
        "options": [
            {"value": "yes", "label": "Yes, with clear process", "weight": 0.1, "is_risk_trigger": False},
            {"value": "limited", "label": "Limited / difficult to override", "weight": 0.6, "is_risk_trigger": True},
            {"value": "no", "label": "No override capability", "weight": 0.9, "is_risk_trigger": True}
        ]
    },
    {
        "id": "q7",
        "text": "Is the AI system explainable to end-users?",
        "category": "Transparency",
        "options": [
            {"value": "yes", "label": "Yes, fully explainable", "weight": 0.1, "is_risk_trigger": False},
            {"value": "partial", "label": "Partially explainable (some decisions not clear)", "weight": 0.5, "is_risk_trigger": False},
            {"value": "no", "label": "Black-box / not explainable", "weight": 0.8, "is_risk_trigger": True}
        ]
    },
    {
        "id": "q8",
        "text": "Are users informed when they are interacting with an AI system?",
        "category": "Transparency",
        "options": [
            {"value": "yes", "label": "Yes, always disclosed", "weight": 0.1, "is_risk_trigger": False},
            {"value": "sometimes", "label": "Sometimes (depending on context)", "weight": 0.5, "is_risk_trigger": False},
            {"value": "no", "label": "No, users are not informed", "weight": 0.7, "is_risk_trigger": True}
        ]
    },
    {
        "id": "q9",
        "text": "Could the AI system cause physical or psychological harm?",
        "category": "Risk",
        "options": [
            {"value": "high", "label": "Yes, high potential for serious harm", "weight": 1.0, "is_risk_trigger": True},
            {"value": "moderate", "label": "Some potential for moderate harm", "weight": 0.6, "is_risk_trigger": True},
            {"value": "low", "label": "Low risk of harm", "weight": 0.2, "is_risk_trigger": False},
            {"value": "none", "label": "No risk of harm", "weight": 0.0, "is_risk_trigger": False}
        ]
    },
    {
        "id": "q10",
        "text": "Does the AI system operate in a regulated sector?",
        "category": "Risk",
        "options": [
            {"value": "finance", "label": "Financial services / banking", "weight": 0.6, "is_risk_trigger": True},
            {"value": "healthcare", "label": "Healthcare / medical devices", "weight": 0.8, "is_risk_trigger": True},
            {"value": "transport", "label": "Transport / autonomous vehicles", "weight": 0.7, "is_risk_trigger": True},
            {"value": "critical", "label": "Critical infrastructure (energy, water, telecoms)", "weight": 0.8, "is_risk_trigger": True},
            {"value": "none", "label": "No specific sector regulation", "weight": 0.1, "is_risk_trigger": False}
        ]
    }
]

def get_questions() -> List[Dict]:
    return QUESTION_BANK

def get_question_by_id(q_id: str) -> Dict:
    for q in QUESTION_BANK:
        if q["id"] == q_id:
            return q
    return None
