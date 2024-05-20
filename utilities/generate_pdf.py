from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'John Doe', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

# Create instance of FPDF class
pdf = PDF()

# Add a page
pdf.add_page()

# Title
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, 'John Doe', 0, 1, 'C')
pdf.ln(10)

# Contact Information
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Contact Information:', 0, 1, 'L')
pdf.set_font('Arial', '', 12)
pdf.cell(0, 10, 'Email: john.doe@example.com', 0, 1, 'L')
pdf.cell(0, 10, 'Phone: (123) 456-7890', 0, 1, 'L')
pdf.ln(10)

# Professional Summary
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Professional Summary:', 0, 1, 'L')
pdf.set_font('Arial', '', 12)
summary = (
    "Experienced Software Developer with over 5 years of experience in developing scalable "
    "web applications and working across the full stack. Proficient in Java, Python, and SQL."
)
pdf.multi_cell(0, 10, summary)
pdf.ln(10)

# Work Experience
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Work Experience:', 0, 1, 'L')

pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Software Developer', 0, 1, 'L')
pdf.set_font('Arial', '', 12)
pdf.cell(0, 10, 'XYZ Corp', 0, 1, 'L')
pdf.cell(0, 10, 'June 2017 - Present', 0, 1, 'L')
experience1 = (
    "- Developed and maintained web applications using Java, Spring Boot, and Hibernate.\n"
    "- Collaborated with front-end developers to integrate user-facing elements with server-side logic using JavaScript, HTML, and CSS.\n"
    "- Optimized SQL queries to improve database performance."
)
pdf.multi_cell(0, 10, experience1)
pdf.ln(5)

pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Junior Software Developer', 0, 1, 'L')
pdf.set_font('Arial', '', 12)
pdf.cell(0, 10, 'ABC Inc.', 0, 1, 'L')
pdf.cell(0, 10, 'Jan 2015 - May 2017', 0, 1, 'L')
experience2 = (
    "- Assisted in the development of web applications using Python and Django.\n"
    "- Created and maintained RESTful APIs.\n"
    "- Participated in code reviews and contributed to the development of best practices."
)
pdf.multi_cell(0, 10, experience2)
pdf.ln(10)

# Education
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Education:', 0, 1, 'L')
pdf.set_font('Arial', '', 12)
pdf.cell(0, 10, 'B.Sc. in Computer Science', 0, 1, 'L')
pdf.cell(0, 10, 'University of Somewhere', 0, 1, 'L')
pdf.cell(0, 10, 'Graduated: 2014', 0, 1, 'L')
pdf.ln(10)

# Skills
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Skills:', 0, 1, 'L')
pdf.set_font('Arial', '', 12)
skills = (
    "- Programming Languages: Java, Python, SQL, JavaScript\n"
    "- Web Technologies: HTML, CSS, React.js\n"
    "- Databases: MySQL, PostgreSQL\n"
    "- Tools: Git, Docker, Jenkins"
)
pdf.multi_cell(0, 10, skills)

# Save the PDF
pdf.output(r'test\integration\data\testcase2_cv.pdf')
