from pathlib import Path
from werkzeug.utils import secure_filename
from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
)

from backend.parsing_fun import cv_parse      # CV parser class/constructor
from backend.similarity_score import similarity_score  # scoring class
import os
from backend.scoring_fun import score 
from typing import cast


app = Flask(__name__,template_folder='templates') # webapp declaration
app.secret_key = ''
UPLOAD_FOLDER = 'uploads' # Ensuring type safety
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024 # Max file size 16MB

os.makedirs(UPLOAD_FOLDER,exist_ok=True) # makes sure the directory exists
ALLOWED_EXTENSIONS = ['pdf','doc','docx','txt']

def allowed_file(filename: str):
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


@app.route('/')
@app.route("/")
def index():
    """
    Render the main upload page.
    If no previous result is set, no score is shown.
    """
    return render_template("main.html")


@app.route("/analyse", methods=["POST"])
def analyse():
    """
    Process CV and job description files uploaded by the user.

    This route:
    - Validates both files are present and have allowed extensions.
    - Saves them to the upload directory.
    - Scores the CV against the job description.
    - Renders the result page.
    """
    if "cv" not in request.files or "job_description" not in request.files:
        flash("Missing CV or job description file.")
        return redirect(url_for("index"))

    cv_file = request.files["cv"]
    job_file = request.files["job_description"]

    # Check filenames and validity
    if not cv_file.filename or not job_file.filename:
        flash("CV or job description file name is missing.")
        return redirect(url_for("index"))

    if not allowed_file(cv_file.filename) or not allowed_file(job_file.filename):
        flash("Please upload valid PDF, DOC, DOCX, or TXT files.")
        return redirect(url_for("index"))

    # Secure filenames and save
    cv_filename = secure_filename(cv_file.filename)
    job_filename = secure_filename(job_file.filename)

    upload_dir: Path = Path(cast(str, app.config["UPLOAD_FOLDER"]))

    cv_path = upload_dir / cv_filename
    job_path = upload_dir / job_filename

    cv_file.save(str(cv_path))
    job_file.save(str(job_path))

    # Score CV against job description
    try:
        cvscorer = score()
        cv_score, explanation = cvscorer.score_cv(str(cv_path), str(job_path)) # type safety
    except Exception as e:
        flash(f"Error processing files: {e}")
        return redirect(url_for("index"))

    return render_template(
        "result.html",
        cv_score=cv_score,
        explanation=explanation
    )

@app.route("/comp_score", methods=["POST"])
def comp_score():
    """
    Score an uploaded CV against a manually entered job description text.

    This route:
    - Checks that CV file and job description text are present.
    - Validates the CV file extension.
    - Saves the CV, parses it, then scores it.
    - Renders the main page again with the result.
    """
    cv_file = request.files.get("cv")
    job_text = request.form.get("job-description", "").strip()

    if not cv_file or not cv_file.filename:
        flash("CV file is required.")
        return redirect(url_for("index"))

    if not allowed_file(cv_file.filename):
        flash("Please upload a valid PDF, DOC, DOCX, or TXT file.")
        return redirect(url_for("index"))

    if not job_text:
        flash("Job description text is required.")
        return redirect(url_for("index"))

    # Save CV file
    cv_filename = secure_filename(cv_file.filename)
    upload_dir = Path(cast(str,app.config["UPLOAD_FOLDER"])) # type safety
    cv_path = upload_dir / cv_filename

    cv_file.save(str(cv_path))

    # Parse CV and score
    try:
        parser = cv_parse()
        parsed_data = parser.parse_cv_file(str(cv_path))

        scorer = similarity_score(parsed_data, job_text)
        cv_score, explanation = scorer.sim_score()
    except Exception as e:
        flash(f"Error analyzing CV: {e}")
        return redirect(url_for("index"))

    return render_template(
        "main.html",
        cv_score=cv_score,
        explanation=explanation
    )



if __name__ == '__main__':
    app.run(debug=True)