from pathlib import Path

from flask import Flask, send_from_directory

FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"

app = Flask(__name__)


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIST, "index.html")


@app.route("/assets/<path:filename>")
def frontend_assets(filename):
    return send_from_directory(FRONTEND_DIST / "assets", filename)


if __name__ == "__main__":
    app.run(debug=True)
