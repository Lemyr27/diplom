import io

from docx import Document


def get_text_from_docx(file: io.BytesIO) -> str:
    document = Document(file)
    return ". ".join([paragraph.text for paragraph in document.paragraphs])

