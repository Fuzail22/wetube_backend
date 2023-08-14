from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allow Cross-Origin Resource Sharing
# CORS(app, resources={r"/upload/*": {"origins": "http://localhost:8080"}})

UPLOAD_FOLDER = 'uploads\\videos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload/video', methods=['POST'])
def upload_video():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            return jsonify({'message': 'File uploaded successfully'}), 200
        else:
            return jsonify({'error': 'File upload failed'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/subtitles.vtt')
def get_subtitles():
    subtitles_path = 'uploads\\subtitles\\subtitles.vtt'
    return send_file(subtitles_path, mimetype='text/vtt')


@app.route('/update-subtitles', methods=['POST'])
def update_subtitles():
    try:
        # Get modified subtitles content from request
        modified_subtitles_content = request.json.get('subtitlesContent')

        # Write the modified subtitles content to the subtitles.vtt file
        with open('uploads\\subtitles\\subtitles.vtt', 'w') as f:
            f.write(modified_subtitles_content)

        return jsonify(message="Subtitles updated successfully")
    except Exception as e:
        return jsonify(error=str(e)), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
