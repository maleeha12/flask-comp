from flask import Flask, render_template, request, jsonify
from PIL import Image
import imagehash

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
#comment
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    image = Image.open(file)
    image_hash = str(imagehash.phash(image))

    return jsonify({'hash': image_hash})

@app.route('/compare', methods=['POST'])
def compare():
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({'error': 'Both files are required'})

    file1 = request.files['file1']
    file2 = request.files['file2']

    image1 = Image.open(file1)
    image2 = Image.open(file2)

    hash1 = imagehash.phash(image1)
    hash2 = imagehash.phash(image2)

    similarity = hash1 - hash2

    if similarity == 0:
        result = 'Images are same'
    else:
        result = 'Different images'

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
