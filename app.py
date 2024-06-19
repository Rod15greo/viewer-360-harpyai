from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
import speech_recognition as sr
from pydub import AudioSegment
import os
import torch
from txt2panoimg import Text2360PanoramaImagePipeline

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'generated_images'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe')
def transcribe_page():
    return render_template('transcribe.html')

@app.route('/viewer')
def viewer():
    return render_template('viewer.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        prompt = request.form['transcription']
        return render_template('generate.html', prompt=prompt)
    return redirect(url_for('transcribe_page'))

@app.route('/generate_image', methods=['POST'])
def generate_image():
    prompt = request.form['prompt']
    
    # Geração da imagem 360° a partir do prompt
    input = {'prompt': prompt, 'upscale': False}
    model_id = 'models'
    txt2panoimg = Text2360PanoramaImagePipeline(model_id, torch_dtype=torch.float16)
    output = txt2panoimg(input)
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result.png')
    output.save(output_path)

    return jsonify({"image_path": output_path})

@app.route('/download_image/<filename>')
def download_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
