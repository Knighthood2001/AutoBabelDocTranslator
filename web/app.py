from flask import Flask, render_template, request, jsonify
from main import run_translation
import threading
import os
import time
from datetime import datetime
import sys
from pathlib import Path

app = Flask(__name__)


# UPLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'AutoBabelDocTranslator', 'papers')
# print(UPLOAD_FOLDER)    # C:\Users\knighthood\AutoBabelDocTranslator\papers

project_root = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, project_root)  # 添加到搜索路径首位
UPLOAD_FOLDER = os.path.join(project_root, 'papers')
# print(UPLOAD_FOLDER)     # E:\code\AutoBabelDocTranslator\AutoBabelDocTranslator\papers

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # Run translation in a separate thread
    thread = threading.Thread(
        target=lambda: run_translation(url, UPLOAD_FOLDER),
        daemon=True
    )
    thread.start()
    
    return jsonify({'status': 'started', 'message': 'Translation process started'})

        
if __name__ == '__main__':
    app.run(port=5000, debug=True)
