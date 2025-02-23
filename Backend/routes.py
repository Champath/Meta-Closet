import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import gridfs
import config

api_bp = Blueprint('api', __name__)

# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "meta_closet"
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
fs = gridfs.GridFS(db)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

@api_bp.route('/upload', methods=['POST'])
def upload_image():
    """
    Endpoint to handle image uploads. The image is saved in MongoDB using GridFS.
    Returns the file id as a response.
    """
    # Check if the request contains a file part.
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400

    file = request.files['file']

    # Check if a file was selected.
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(config.UPLOAD_FOLDER, filename)
        
        # Optionally, save the file locally first.
        file.save(filepath)
        
        # Read file data for GridFS.
        with open(filepath, "rb") as f:
            file_data = f.read()
        
        # Store the file in MongoDB via GridFS.
        file_id = fs.put(file_data, filename=filename)
        
        # Optionally, remove the local file after storing it.
        os.remove(filepath)
        
        return jsonify({'message': 'File uploaded successfully', 'file_id': str(file_id)}), 200

    return jsonify({'error': 'File type not allowed'}), 400
