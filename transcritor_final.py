
from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import whisper
import webbrowser
from werkzeug.utils import secure_filename

# 🔧 Força o caminho do FFmpeg
os.environ["PATH"] += os.pathsep + r"C:\\ffmpeg\\bin"

BASE_DIR = r"C:\\Users\\brito\\OneDrive\\Área de Trabalho\\Transcritor de vídeos funcional"
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
TRANSCRIPT_FOLDER = os.path.join(BASE_DIR, "transcripts")
TEMPLATE_FOLDER = os.path.join(BASE_DIR, "templates")

ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'wav', 'm4a', 'aac', 'ogg', 'wma', 'mov', 'mkv'}

app = Flask(__name__, template_folder=r"C:\Users\brito\OneDrive\Área de Trabalho\Transcritor de vídeos funcional\templates")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TRANSCRIPT_FOLDER'] = TRANSCRIPT_FOLDER

# Garante que as pastas existem
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSCRIPT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    transcripts = os.listdir(TRANSCRIPT_FOLDER)
    return render_template('index.html', transcripts=transcripts)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    mode = request.form.get('mode', 'lebre')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Escolhe o modelo conforme o modo
        model_name = "tiny" if mode == "lebre" else "medium"
        model = whisper.load_model(model_name)

        result = model.transcribe(filepath)
        transcript_text = result["text"]

        output_path = os.path.join(app.config['TRANSCRIPT_FOLDER'], filename + '.txt')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transcript_text)

        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(TRANSCRIPT_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)
