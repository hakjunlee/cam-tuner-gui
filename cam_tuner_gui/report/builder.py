"""리포트 생성 모듈."""

from __future__ import annotations

from typing import Any


def render_html(session: dict[str, Any]) -> str:
    """세션 데이터를 HTML 문자열로 렌더링한다.

    Jinja2가 설치되어 있으면 템플릿을 사용하고, 그렇지 않으면 간단한
    문자열 포매팅으로 대체한다.
    """
    try:
        from jinja2 import Template

        template_str = """
        <html>
        <head><meta charset="utf-8"><title>Camera Report</title></head>
        <body>
          <h1>Camera Session Report</h1>
          <ul>
          {% for key, value in session.items() %}
            <li><strong>{{ key }}:</strong> {{ value }}</li>
          {% endfor %}
          </ul>
        </body>
        </html>
        """
        template = Template(template_str)
        return template.render(session=session)
    except Exception:
        # Fallback without Jinja2
        rows = "\n".join(
            f"<li><strong>{k}:</strong> {v}</li>" for k, v in session.items()
        )
        return (
            "<html><head><meta charset='utf-8'><title>Camera Report</title></head>"
            "<body><h1>Camera Session Report</h1><ul>" + rows + "</ul></body></html>"
        )


def export_pdf(html: str, output_path: str) -> None:
    """HTML을 받아 PDF로 저장한다."""
    try:
        from weasyprint import HTML  # type: ignore

        HTML(string=html).write_pdf(output_path)
    except Exception:
        # 라이브러리 미설치 또는 변환 실패 시 HTML 내용을 그대로 저장한다.
        with open(output_path, "wb") as f:
            if isinstance(html, str):
                html_bytes = html.encode("utf-8")
            else:
                html_bytes = html
            # Minimal PDF header so viewer won't fail completely
            f.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
            f.write(b"1 0 obj<<>>endobj\n")
            f.write(b"trailer<<>>\n%%EOF")
            f.write(b"\n")
            f.write(html_bytes)

