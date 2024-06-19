from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from pydub import AudioSegment

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe')
def transcribe_page():
    return render_template('transcribe.html')

@app.route('/viewer')
def viewer():
    return render_template('viewer.html')

@app.route('/transcribe_audio', methods=['POST'])
def transcribe_audio():
    audio_file = request.files['audio']
    audio_path = "temp.wav"
    audio_file.save(audio_path)

    # Converta o áudio para um formato PCM WAV que o SpeechRecognition possa ler
    audio = AudioSegment.from_file(audio_path)
    audio.export("converted.wav", format="wav")

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile("converted.wav") as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='pt-BR')
            return jsonify({"transcription": text})
    except Exception as e:
        return jsonify({"transcription": f"Erro ao processar o áudio: {e}"})

if __name__ == '__main__':
    app.run(debug=True)
