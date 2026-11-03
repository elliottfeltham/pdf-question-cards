import fitz  # PyMuPDF


class PDFValidationError(ValueError):
    """Raised when an upload is not a readable PDF."""


class PDFLimitError(ValueError):
    """Raised when a readable PDF exceeds an application limit."""


def extract_all_text(
    pdf_bytes: bytes,
    *,
    max_pages: int,
    max_characters: int,
) -> str:
    try:
        document = fitz.open(stream=pdf_bytes, filetype="pdf")
    except (fitz.FileDataError, ValueError) as exc:
        raise PDFValidationError("The uploaded file is not a readable PDF.") from exc

    try:
        if document.page_count > max_pages:
            raise PDFLimitError(f"PDF exceeds the {max_pages}-page limit.")

        parts: list[str] = []
        character_count = 0
        for page in document:
            page_text = page.get_text()
            character_count += len(page_text)
            if character_count > max_characters:
                raise PDFLimitError(
                    f"PDF text exceeds the {max_characters:,}-character limit."
                )
            parts.append(page_text)
        return "".join(parts)
    finally:
        document.close()
