from pathlib import Path
import fitz
from docx import Document


def load_pdf(file_path):
    pages = []
    pdf = fitz.open(file_path)

    for page_num, page in enumerate(pdf, start=1):
        text = page.get_text()
        if text.strip():
            pages.append({
                "text": text,
                "source": Path(file_path).name,
                "page": page_num
            })

    pdf.close()
    return pages


def load_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    return [{"text": text, "source": Path(file_path).name, "page": 1}]


def load_documents(folder_path):
    documents = []
    for file in Path(folder_path).glob("*"):
        if file.suffix == ".pdf":
            documents.extend(load_pdf(str(file)))
        elif file.suffix == ".docx":
            documents.extend(load_docx(str(file)))

    return documents