import os
from flask_autoindex import AutoIndex
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
AutoIndex(app, browse_root=UPLOAD_FOLDER)


@app.route("/upload/", methods=["POST"])
@app.route("/upload/<path:path>", methods=["POST"])
def upload(path=""):
    # check if the post request has the file part
    if 'file' not in request.files:
        return redirect("/" + path)
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        if not filename:
            return redirect("/" + path)
        file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'],
            path, filename))
    return redirect("/" + path)


@app.route("/newfolder/", methods=["POST"])
@app.route("/newfolder/<path:path>", methods=["POST"])
def new_folder(path=""):
    # there still a risk: path (since user can change this)
    folder = secure_filename(request.form["name"])
    abs_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], path, folder)
    if not os.path.exists(abs_path):
        os.mkdir(abs_path)
    return redirect("/" + path)


if __name__ == '__main__':
    app.run(debug=False)
