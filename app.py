import os
import uuid

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for
)

from werkzeug.utils import secure_filename

from config import (
    SECRET_KEY,
    UPLOAD_FOLDER
)

from modules.auth import authenticate_user
from models.file_model import UploadedFile
from config import (
    PROCESSED_FOLDER
)

from modules.processor import (
    CancerRegistryPIIProcessor
)

app = Flask(__name__)
app.secret_key = SECRET_KEY


# LOGIN
@app.route('/', methods=['GET', 'POST'])
def login():

    # Prevent logged-in users from seeing login page
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    error = None

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = authenticate_user(
            username,
            password
        )

        if user:

            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            return redirect(
                url_for("dashboard")
            )

        error = "Invalid username or password"

    return render_template(
        "login.html",
        error=error
    )


# DASHBOARD
@app.route('/dashboard')
def dashboard():

    if "user_id" not in session:
        return redirect('/')

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


# UPLOAD DATASET
@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if "user_id" not in session:
        return redirect('/')

    error = None

    if request.method == "POST":

        file = request.files.get("dataset")

        if not file:
            error = "Please select a file."
            return render_template(
                "upload.html",
                error=error
            )

        if file.filename == "":
            error = "No file selected."
            return render_template(
                "upload.html",
                error=error
            )

        # Create unique filename
        stored_name = (
            str(uuid.uuid4()) +
            "_" +
            secure_filename(file.filename)
        )

        filepath = os.path.join(
            UPLOAD_FOLDER,
            stored_name
        )

        file.save(filepath)

        UploadedFile.create_file(
            file.filename,
            stored_name,
            session["user_id"]
        )

        return redirect(
            url_for('files')
        )

    return render_template(
        'upload.html',
        error=error
    )


# PROCESS FILE
@app.route(
    '/process/<int:file_id>'
)
def process_file(
    file_id
):

    if "user_id" not in session:
        return redirect('/')

    file = UploadedFile.get_file(
        file_id
    )

    if not file:

        return redirect(
            url_for('files')
        )

    processor = (
        CancerRegistryPIIProcessor()
    )

    input_file = os.path.join(
        UPLOAD_FOLDER,
        file["stored_filename"]
    )

    output_file = os.path.join(
        PROCESSED_FOLDER,
        f"hashed_{file['stored_filename']}"
    )

    stats = processor.process_file(
        input_file,
        output_file
    )

    UploadedFile.update_status(
        file_id,
        "Processed",
        stats["records_processed"]
    )

    return redirect(
        url_for("files")
    )


# VIEW FILES
@app.route('/files')
def files():

    if "user_id" not in session:
        return redirect('/')

    files = UploadedFile.get_all_files()

    return render_template(
        'files.html',
        files=files
    )



# LOGOUT
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')


# RUN APP
if __name__ == '__main__':
    app.run(debug=True)
    


# python create_admin.py (run on terminer/bash)
# Username: admin
# Password: admin123
# Role: administrator