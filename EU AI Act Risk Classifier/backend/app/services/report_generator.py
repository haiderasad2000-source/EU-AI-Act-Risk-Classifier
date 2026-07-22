import os
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any
from datetime import datetime

try:
    from weasyprint import HTML
    HAS_WEASYPRINT = True
except ImportError:
    HAS_WEASYPRINT = False

class ReportGenerator:
    def __init__(self):
        template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates")
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def generate(self, assessment: Dict[str, Any]) -> str:
        template = self.env.get_template("report_template.html")

        data = {
            **assessment,
            "generated_date": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
            "risk_color": self._get_risk_color(assessment.get("classification", "")),
            "gaps_count": len(assessment.get("compliance_gaps", [])),
            "recommendations": assessment.get("recommendations", [])
        }

        html_content = template.render(**data)

        output_dir = "reports"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{assessment['id']}.pdf"
        filepath = os.path.join(output_dir, filename)

        if HAS_WEASYPRINT:
            HTML(string=html_content).write_pdf(filepath)
        else:
            html_path = filepath.replace(".pdf", ".html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            filepath = html_path

        return filepath

    def _get_risk_color(self, classification: str) -> str:
        mapping = {
            "Unacceptable": "#d32f2f",
            "High": "#f57c00",
            "Limited": "#f9a825",
            "Minimal": "#388e3c"
        }
        return mapping.get(classification, "#757575")

report_generator = ReportGenerator()
