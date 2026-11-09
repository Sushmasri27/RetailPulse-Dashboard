from pypdf import PdfReader
from docx import Document


def read_pdf(file):

    reader = PdfReader(file)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text:

            pages.append({
                "page": page_number,
                "text": text
            })

    return pages


def read_docx(file):
    doc = Document(file)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def read_txt(file):
    return file.read().decode("utf-8")