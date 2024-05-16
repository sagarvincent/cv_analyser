from flask import Flask, render_template, request
from backend.parsing_fun import cv_parse
from backend.similarity_score import similarity_score
import os

app = Flask(__name__,template_folder='templates')

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/analyse', methods=['POST'])
def analyse():
    if request.method == 'POST':
        cv_file = request.files['cv']
        job_description_file = request.files['job_description']
        
        # Save the files and get their paths
        cv_path = 'uploads/' + cv_file.filename
        cv_file.save(cv_path)
        job_description_path = 'uploads/' + job_description_file.filename
        job_description_file.save(job_description_path)
        
        # Call the scoring function
        cv_score, score_explanation = score_cv(cv_path, job_description_path)
        
        return render_template('result.html', cv_score=cv_score, explanation=score_explanation)

@app.route('/comp_score', methods=['POST'])
def comp_score():
    if request.method == 'POST':
        cv_file = request.files['cv']
        job_description = request.form['job-description']
        
        # Save the files and get their paths
        cv_path = 'uploads/' + cv_file.filename
        cv_file.save(cv_path)
        parser = cv_parse()
        print(type(job_description))
        #cv_file = parser.convert_to_pdf(cv_file)
        # Call the scoring function
        cwd = os.getcwd()
        parsed_data = parser.parse_cv_file(cv_path)
        s = similarity_score(parsed_data, job_description)
        cv_score, score_explanation = s.sim_score()
        
        return render_template('./main.html', cv_score=cv_score, explanation=score_explanation)

if __name__ == '__main__':
    app.run(debug=True)