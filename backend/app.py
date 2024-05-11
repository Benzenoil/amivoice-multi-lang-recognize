from dotenv import load_dotenv
from utils import get_final_result
from flask_cors import CORS
from flask import Flask, request, jsonify
import os
import requests
import logging

logging.basicConfig(level=logging.DEBUG)
logging.debug('Debug message')

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/upload', methods=['POST'])
def upload_file():
    data = request.form
    engine = data.get('engine', '-a-general')

    file = request.files.get('file', None)
    if file is None:
        return jsonify({'error': 'No file part'}), 400
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file.seek(0, 2)
    file_size = file.tell()
    file.seek(0)

    if file_size <= 8000000:
        response = requests.post(
            'https://acp-api.amivoice.com/v1/nolog/recognize',
            files={
                'a': (file.filename, file, file.content_type)
            },
            data={
                'd': engine,
                'u': os.environ.get('AMIVOICE_API_KEY', '')
            }
        )
        response.raise_for_status()
        return response.json()
    else:
        return jsonify({'error': 'File size exceeds limit'}), 413


@app.route('/bi-lang', methods=['POST'])
def bi_lang():
    data = request.form
    result_data_one = data.get('result_data', None)
    result_data_two = data.get('result_data2', None)
    if not result_data_one or not result_data_two:
        raise ValueError('No result data')

    final_result = get_final_result(result_data_one, result_data_two)
    return jsonify(final_result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5051)
