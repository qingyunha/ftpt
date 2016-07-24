import os
from flask_autoindex import AutoIndex
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'gz'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

AutoIndex(app, browse_root=UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
                    filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/upload/", methods=["POST"])
@app.route("/upload/<path:path>", methods=["POST"])
def upload(path=""):
    print "upload path is ", path
    # check if the post request has the file part
    if 'file' not in request.files:
        print('no file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        print('No selected file')
        return redirect("/" + path)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'],
            path, filename))
        return redirect("/" + path)


@app.route("/newfolder/", methods=["POST"])
@app.route("/newfolder/<path:path>", methods=["POST"])
def new_folder(path=""):
    folder = request.form["name"]
    os.mkdir(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], path,
        folder))
    return redirect("/" + path)


if __name__ == '__main__':
    app.run(debug=True)
