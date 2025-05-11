import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_file(file_obj, subfolder="uploads"):
    if file_obj and allowed_file(file_obj.filename):
        filename = secure_filename(file_obj.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        full_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
        os.makedirs(full_folder, exist_ok=True)

        file_path = os.path.join(full_folder, unique_filename)
        file_obj.save(file_path)
        return f'uploads/{subfolder}/{unique_filename}'.replace("\\", "/")
    return None



def delete_file_if_exists(file_path):
    try:
        if isinstance(file_path, str):
            full_path = os.path.join(current_app.root_path, 'static', file_path.replace('\\', '/'))
            if os.path.exists(full_path):
                os.remove(full_path)
                print(f"🗑️ Deleted file at: {full_path}")
        else:
            print("⚠️ Skipped deleting: file_path is not a string")
    except Exception as e:
        print("Error deleting file:", e)




