import PyPDF2
import docx
import docx2txt
import spacy
import os
import torch

class cv_score():
    def __init__(self,cv_path,job_description):
        self.cv_path = cv_path
        self.job_descrip = job_description
        # Load spaCy English model
        self.nlp = spacy.load("en_core_web_sm")

    def extract_text_from_pdf(self, pdf_path):
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
        return text

    def extract_text_from_docx(self,docx_path):
        doc = docx.Document(docx_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text
        return text

    def extract_text_from_doc(self,doc_path):
        return docx2txt.process(doc_path)

    def parse_cv_text(self,text):
        # Use spaCy for named entity recognition
        doc = self.nlp(text)
        return doc

    def parse_cv_file(self,file_path):
        if file_path.endswith('.pdf'):
            text = self.extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            text = self.extract_text_from_docx(file_path)
        elif file_path.endswith('.doc'):
            text = self.extract_text_from_doc(file_path)
        else:
            raise ValueError("Unsupported file format")
        
        return self.parse_cv_text(text)

# Example usage:
cwd = os.getcwd()
cv_file = r"D:\Projects\Job\alindor\cv_analyser\test\data\SagarResume-2.pdf"
parser = cv_score(cv_file," ")
parsed_data = parser.parse_cv_file(cv_file)
print(parsed_data)