"""리포트 생성 모듈."""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, Template, select_autoescape
import weasyprint


def render_html(session) -> str:
    """세션 데이터를 HTML 문자열로 렌더링한다."""
    template_str = """
    <html>
    <head>
        <meta charset='utf-8'>
        <title>Camera Tuning Report</title>
    </head>
    <body>
        <h1>Camera Tuning Report</h1>
        <pre>{{ session | tojson(indent=2) }}</pre>
    </body>
    </html>
    """
    env = Environment(autoescape=select_autoescape(["html", "xml"]))
    template: Template = env.from_string(template_str)
    return template.render(session=session)


def export_pdf(html: str, output_path: str | Path) -> None:
    """HTML을 받아 PDF로 저장한다."""
    pdf = weasyprint.HTML(string=html).write_pdf()
    Path(output_path).write_bytes(pdf)
