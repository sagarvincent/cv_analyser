import pdfplumber
import docx
import docx2txt


class cv_parse:
    def parse_pdf_form(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                text += page_text + "\n"
        return text

    def extract_text_from_docx(self, docx_path):
        doc = docx.Document(docx_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text
        return text

    def extract_text_from_doc(self, doc_path):
        return docx2txt.process(doc_path)

    def parse_cv_file(self, file_path: str):
        if file_path.endswith(".pdf"):
            return self.parse_pdf_form(file_path)
        if file_path.endswith(".docx"):
            return self.extract_text_from_docx(file_path)
        if file_path.endswith(".doc"):
            return self.extract_text_from_doc(file_path)
        raise ValueError("Unsupported file format")
