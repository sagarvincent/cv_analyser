import PyPDF2
import pdfplumber
import docx
import docx2txt
import os
import similarity_score

class cv_parse():
    def __init__(self,cv_path,job_description):
        self.cv_path = cv_path
        self.job_descrip = job_description
        
    def extract_text_from_pdf(self, pdf_path):
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
        return text
    
    def parse_pdf_form(self,pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                # Extract text from the current page
                page_text = page.extract_text()
                # Append the extracted text to the result
                text += page_text + "\n"
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
        
        return text

    def parse_cv_file(self,file_path):
        if file_path.endswith('.pdf'):
            text = self.parse_pdf_form(file_path)
        elif file_path.endswith('.docx'):
            text = self.extract_text_from_docx(file_path)
        elif file_path.endswith('.doc'):
            text = self.extract_text_from_doc(file_path)
        else:
            raise ValueError("Unsupported file format")
        
        return self.parse_cv_text(text)

# Example usage:
cwd = os.getcwd()
cv_file = r"D:\Projects\Job\alindor\cv_analyser\test\data\Arya_Sivaraj.docx"
parser = cv_parse(cv_file," ")
parsed_data = parser.parse_cv_file(cv_file)
s = similarity_score.similarity_score(parsed_data, "Dear Candidate, Greetings From  Designation- Assistant manager/Deputy manager Role- Equity Dealer CTC- up to-6 LPA + incentive + Other benefit Branch Dealing Roles Responsibilities • Execution of trade orders on behalf of clients. • Building Relationships with clients. • Generating brokerage and volume. • Cross selling third party products. • New Client Acquisition • NISM 8 certification is mandatory • Graduate / Post graduate with minimum 1 yr exp in Equitie. Kindly reply with an updated CV on apex.vedikahr@gmail.com if you are interested in the mentioned Job Role. you can call also on 7991515067. This job is provided by Shine.com")
r = s.sim_score()
