import json
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

from .normalize_output import normalize_output
from reposage.health.scorer import calculate_health_score


def _force_dict(obj):
    """
    Force CrewAI outputs into dict safely.
    Handles:
    - dict
    - Pydantic
    - JSON string
    - garbage
    """
    if obj is None:
        return {}

    if isinstance(obj, dict):
        return obj

    if hasattr(obj, "model_dump"):
        return obj.model_dump()

    if isinstance(obj, str):
        try:
            return json.loads(obj)
        except Exception:
            return {}

    return {}

def generate_report_pdf(
    scan_output,
    architecture_output,
    security_output,
    performance_output,
    roadmap_output,
    output_path: str = "outputs/report.pdf",
):
    # --------------------------------------------------
    # FORCE everything into dicts (CRITICAL FIX)
    # --------------------------------------------------
    scan = _force_dict(normalize_output(scan_output))
    architecture = _force_dict(normalize_output(architecture_output))
    security = _force_dict(normalize_output(security_output))
    performance = _force_dict(normalize_output(performance_output))
    roadmap = _force_dict(normalize_output(roadmap_output))

    health = calculate_health_score(
            scan, architecture, security, performance
        )

    # --------------------------------------------------
    # Output path
    # --------------------------------------------------
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------
    # PDF setup
    # --------------------------------------------------
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="TitleCenter",
            fontSize=18,
            alignment=TA_CENTER,
            spaceAfter=20,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Section",
            fontSize=14,
            spaceBefore=16,
            spaceAfter=8,
            bold=True,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            fontSize=10,
            spaceAfter=6,
            alignment=TA_LEFT,
        )
    )

    elements = []

    # ==================================================
    # TITLE
    # ==================================================
    elements.append(Paragraph("Repository Analysis Report", styles["TitleCenter"]))
    elements.append(Spacer(1, 12))

    # ==================================================
    # OVERVIEW
    # ==================================================
    elements.append(Paragraph("Repository Overview", styles["Section"]))

    elements.append(
        Paragraph(f"<b>Repository Path:</b> {scan.get('repo_path', 'unknown')}", styles["Body"])
    )
    elements.append(
        Paragraph(f"<b>Total Files Scanned:</b> {scan.get('total_files_scanned', 0)}", styles["Body"])
    )
    elements.append(
        Paragraph(
            f"<b>Detected Languages:</b> {', '.join(scan.get('detected_languages', []))}",
            styles["Body"],
        )
    )

    # score added
    elements.append(Paragraph(
            f"<b>Health Score:</b> {health['score']} / 100 (Grade {health['grade']})",
            styles["Heading2"]
        ))

    for k, v in health["breakdown"].items():
        elements.append(Paragraph(f"- {k.title()}: {v}", styles["Body"]))



    # ==================================================
    # ARCHITECTURE
    # ==================================================
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Architecture Summary", styles["Section"]))

    elements.append(
        Paragraph(
            f"<b>Architecture Type:</b> {architecture.get('architecture_type', 'N/A')}",
            styles["Body"],
        )
    )

    if architecture.get("key_modules"):
        elements.append(
            Paragraph(
                f"<b>Key Modules:</b> {', '.join(architecture.get('key_modules', []))}",
                styles["Body"],
            )
        )

    if architecture.get("runtime_flow_summary"):
        elements.append(
            Paragraph(
                f"<b>Runtime Flow:</b><br/>{architecture.get('runtime_flow_summary')}",
                styles["Body"],
            )
        )

    # ==================================================
    # SECURITY
    # ==================================================
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Security Findings", styles["Section"]))

    security_issues = security.get("issues", [])
    if not security_issues:
        elements.append(Paragraph("No security issues detected.", styles["Body"]))
    else:
        elements.append(
            ListFlowable(
                [
                    ListItem(
                        Paragraph(
                            f"<b>{i.get('severity')}:</b> {i.get('issue')}",
                            styles["Body"],
                        )
                    )
                    for i in security_issues
                ],
                bulletType="bullet",
            )
        )

    # ==================================================
    # PERFORMANCE
    # ==================================================
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Performance Findings", styles["Section"]))

    perf_issues = performance.get("issues", [])
    if not perf_issues:
        elements.append(Paragraph("No performance issues detected.", styles["Body"]))
    else:
        elements.append(
            ListFlowable(
                [
                    ListItem(
                        Paragraph(
                            f"<b>{i.get('severity')}:</b> {i.get('issue')}",
                            styles["Body"],
                        )
                    )
                    for i in perf_issues
                ],
                bulletType="bullet",
            )
        )

    # ==================================================
    # ROADMAP
    # ==================================================
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Engineering Roadmap", styles["Section"]))

    def render_phase(title, items):
        elements.append(Paragraph(title, styles["Body"]))
        if not items:
            elements.append(Paragraph("No items identified.", styles["Body"]))
            return
        elements.append(
            ListFlowable(
                [
                    ListItem(
                        Paragraph(
                            f"<b>{i.get('priority')}:</b> {i.get('task')}",
                            styles["Body"],
                        )
                    )
                    for i in items
                ],
                bulletType="bullet",
            )
        )

    render_phase("Immediate Fixes", roadmap.get("immediate_fixes", []))
    render_phase("Short Term", roadmap.get("short_term", []))
    render_phase("Medium Term", roadmap.get("medium_term", []))

    # ==================================================
    # BUILD PDF (THIS IS THE KEY LINE)
    # ==================================================
    doc.build(elements)

    print(f"✅ report.pdf written to {output_path.resolve()}")
    return output_path
