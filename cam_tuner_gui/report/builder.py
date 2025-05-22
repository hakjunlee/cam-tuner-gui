"""리포트 생성 모듈."""

from __future__ import annotations


def render_html(session) -> str:
    """세션 데이터를 HTML 문자열로 렌더링한다."""
    # TODO: Jinja2 템플릿 렌더링 구현
    pass


def export_pdf(html: str, output_path: str) -> None:
    """HTML을 받아 PDF로 저장한다."""
    # TODO: PDF 변환 구현
    pass
