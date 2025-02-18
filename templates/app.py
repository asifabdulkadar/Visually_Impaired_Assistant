from flask import Flask, render_template, request, send_file
from gtts import gTTS
import os
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS speech_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        text TEXT,
                        language TEXT,
                        file_name TEXT
                    )''')
    conn.commit()
    conn.close()

init_db()

# Ensure the 'static' directory exists
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_text_to_speech():
    text = request.form['text']
    language = request.form['language']
    
    tts = gTTS(text=text, lang=language, slow=False)
    
    # Ensure the filename is unique for each conversion
    audio_file = f"static/output_{len(text)}.mp3"
    tts.save(audio_file)
    
    # Save to database
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO speech_history (text, language, file_name) VALUES (?, ?, ?)", (text, language, audio_file))
    conn.commit()
    conn.close()

    # Return the file to the user
    return send_file(os.path.join(app.root_path, audio_file), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
