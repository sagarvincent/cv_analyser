from flask import Flask, render_template, request
from scoring_function import score_cv

app = Flask(__name__)

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
        job_description_file = request.files['job_description']
        
        # Save the files and get their paths
        cv_path = 'uploads/' + cv_file.filename
        cv_file.save(cv_path)
        job_description_path = 'uploads/' + job_description_file.filename
        job_description_file.save(job_description_path)
        
        # Call the scoring function
        cv_score, score_explanation = score_cv(cv_path, job_description_path)
        
        return render_template('result.html', cv_score=cv_score, explanation=score_explanation)

if __name__ == '__main__':
    app.run(debug=True)