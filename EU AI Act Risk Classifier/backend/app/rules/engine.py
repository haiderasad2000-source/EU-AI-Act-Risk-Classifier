from typing import Dict, Any, List, Tuple
from ..models import RiskTier
from .questions import get_question_by_id

class RiskClassifier:

    def __init__(self):
        self.risk_thresholds = {
            "unacceptable": 0.75,
            "high": 0.50,
            "limited": 0.25,
            "minimal": 0.0
        }

    def classify(self, answers: Dict[str, Any]) -> Tuple[RiskTier, float, List[Dict], List[str]]:
        total_weight = 0.0
        max_possible_weight = 0.0
        triggered_articles = []

        for q_id, answer_value in answers.items():
            question = get_question_by_id(q_id)
            if not question:
                continue
            for option in question.get("options", []):
                if option["value"] == answer_value:
                    weight = option.get("weight", 0)
                    total_weight += weight
                    max_possible_weight += 1.0
                    if option.get("is_risk_trigger", False):
                        triggered_articles.append({
                            "question": q_id,
                            "reason": f"Selected '{option['label']}'"
                        })
                    break

        if max_possible_weight > 0:
            raw_score = total_weight / max_possible_weight
        else:
            raw_score = 0.0

        classification, score = self._determine_tier(raw_score, triggered_articles)
        compliance_gaps = self._generate_gaps(classification, answers, triggered_articles)
        recommendations = self._generate_recommendations(classification, compliance_gaps)

        return classification, score, compliance_gaps, recommendations

    def _determine_tier(self, raw_score: float, triggers: List) -> Tuple[RiskTier, float]:
        boost = min(len(triggers) * 0.05, 0.2)
        adjusted_score = min(raw_score + boost, 1.0)
        score_100 = adjusted_score * 100

        if adjusted_score >= self.risk_thresholds["unacceptable"]:
            return RiskTier.UNACCEPTABLE, score_100
        elif adjusted_score >= self.risk_thresholds["high"]:
            return RiskTier.HIGH, score_100
        elif adjusted_score >= self.risk_thresholds["limited"]:
            return RiskTier.LIMITED, score_100
        else:
            return RiskTier.MINIMAL, score_100

    def _generate_gaps(self, classification: RiskTier, answers: Dict, triggers: List) -> List[Dict]:
        gaps = []

        if classification == RiskTier.UNACCEPTABLE:
            gaps.append({
                "article": "Article 5",
                "requirement": "Prohibited AI practices must not be deployed",
                "status": "non_compliant",
                "severity": "critical",
                "recommendation": "Immediately cease deployment or redesign system to avoid prohibited use cases."
            })

        if classification in [RiskTier.UNACCEPTABLE, RiskTier.HIGH]:
            q5_answer = answers.get("q5", "none")
            if q5_answer in ["none", "review"]:
                gaps.append({
                    "article": "Article 9",
                    "requirement": "High-risk AI systems must have a robust risk management system",
                    "status": "partially_compliant",
                    "severity": "high",
                    "recommendation": "Implement a risk management system with defined processes for risk identification and mitigation."
                })

        if classification in [RiskTier.UNACCEPTABLE, RiskTier.HIGH]:
            q4_answer = answers.get("q4", "no")
            if q4_answer in ["yes_unknown"]:
                gaps.append({
                    "article": "Article 10",
                    "requirement": "Training data must be free from biases and representative",
                    "status": "non_compliant",
                    "severity": "high",
                    "recommendation": "Conduct a thorough bias audit of training data and document mitigation measures."
                })

        if classification in [RiskTier.UNACCEPTABLE, RiskTier.HIGH, RiskTier.LIMITED]:
            q6_answer = answers.get("q6", "no")
            if q6_answer in ["limited", "no"]:
                gaps.append({
                    "article": "Article 14",
                    "requirement": "Human oversight must be possible, with clear override procedures",
                    "status": "non_compliant",
                    "severity": "medium",
                    "recommendation": "Design and implement a clear human override mechanism with documented process."
                })

        if classification in [RiskTier.UNACCEPTABLE, RiskTier.HIGH, RiskTier.LIMITED]:
            q7_answer = answers.get("q7", "no")
            if q7_answer in ["no", "partial"]:
                gaps.append({
                    "article": "Article 13",
                    "requirement": "AI systems must be transparent and explainable to users",
                    "status": "partially_compliant",
                    "severity": "medium",
                    "recommendation": "Implement explainability tools (e.g., LIME, SHAP) and provide clear documentation."
                })

        return gaps

    def _generate_recommendations(self, classification: RiskTier, gaps: List[Dict]) -> List[str]:
        recommendations = []

        if classification == RiskTier.UNACCEPTABLE:
            recommendations = [
                "CRITICAL: System appears to involve prohibited practices under Article 5. Immediate redesign or discontinuation required.",
                "Consult with legal counsel to determine if your system falls under any exemption.",
                "Prepare a detailed justification if claiming exemption.",
                "Document all mitigation measures for regulatory review."
            ]
        elif classification == RiskTier.HIGH:
            recommendations = [
                "Implement a comprehensive risk management system (Article 9).",
                "Establish a data governance framework with bias auditing (Article 10).",
                "Ensure human oversight and override capabilities (Article 14).",
                "Develop technical documentation and transparency disclosures (Article 13).",
                "Register the system in the EU database for high-risk AI systems (Article 60).",
                "Implement a post-market monitoring system (Article 72)."
            ]
        elif classification == RiskTier.LIMITED:
            recommendations = [
                "Implement transparency measures (Article 52) — users must know they are interacting with AI.",
                "Provide clear information about the AI system's capabilities and limitations.",
                "Consider implementing a lightweight risk management process.",
                "Maintain documentation for regulatory inspection."
            ]
        else:
            recommendations = [
                "System appears to have minimal risk.",
                "Document compliance with Article 52 (transparency requirements).",
                "Maintain internal records for 3 years.",
                "Consider voluntary compliance with high-risk requirements for future readiness."
            ]

        for gap in gaps:
            if gap["recommendation"] not in recommendations:
                recommendations.append(f"- {gap['recommendation']}")

        return recommendations

classifier = RiskClassifier()
