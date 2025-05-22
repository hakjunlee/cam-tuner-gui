"""리포트 생성 모듈."""

from __future__ import annotations

from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML


def render_html(session: Any) -> str:
    """세션 데이터를 HTML 문자열로 렌더링한다."""
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape()
    )
    template = env.get_template("report.html")
    return template.render(session=session)


def export_pdf(html: str, output_path: str) -> None:
    """HTML을 받아 PDF로 저장한다."""
    HTML(string=html).write_pdf(output_path)
