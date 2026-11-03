import fitz
import pytest

from backend.main import normalise_questions
from backend.pdf import PDFLimitError, extract_all_text


def make_pdf(text: str, pages: int = 1) -> bytes:
    document = fitz.open()
    for _ in range(pages):
        page = document.new_page()
        page.insert_text((72, 72), text)
    data = document.tobytes()
    document.close()
    return data


def test_normalise_questions_whitelists_fields_and_replaces_id():
    questions = normalise_questions(
        {
            "items": [
                {
                    "id": "provider-controlled",
                    "type": "theory",
                    "prompt_md": "  What is a graph?  ",
                    "solution_md": "  A set of nodes and edges.  ",
                    "unexpected": "discard me",
                }
            ]
        }
    )

    assert questions[0]["id"] != "provider-controlled"
    assert questions[0]["prompt_md"] == "What is a graph?"
    assert questions[0]["solution_md"] == "A set of nodes and edges."
    assert "unexpected" not in questions[0]


def test_normalise_questions_rejects_malformed_payload():
    with pytest.raises(ValueError):
        normalise_questions({"items": []})


def test_extract_all_text_reads_a_valid_pdf():
    text = extract_all_text(
        make_pdf("Lecture content"),
        max_pages=2,
        max_characters=1_000,
    )
    assert "Lecture content" in text


def test_extract_all_text_enforces_page_limit():
    with pytest.raises(PDFLimitError):
        extract_all_text(
            make_pdf("Lecture content", pages=2),
            max_pages=1,
            max_characters=1_000,
        )
