from flask import Flask, render_template, request, jsonify
from main import run_translation
import threading
import os
import time
from datetime import datetime


app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'AutoBabelDocTranslator', 'papers')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 存储任务状态
current_task = {
    'status': 'initializing',
    'message': '正在初始化...',
    'timestamp': datetime.now().isoformat()
}



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # 更新任务状态
    current_task.update({
        'status': 'processing',
        'message': '开始处理翻译任务',
        'timestamp': datetime.now().isoformat()
    })

    # Run translation in a separate thread
    thread = threading.Thread(
        target=lambda: run_translation(url, UPLOAD_FOLDER),
        daemon=True
    )
    thread.start()
    
    return jsonify({'status': 'started', 'message': 'Translation process started'})

def simulate_status_updates():
    """模拟状态更新"""
    time.sleep(2)  # 2秒后更新为下载中
    current_task.update({
        'status': 'downloading',
        'message': '正在下载PDF文档...',
        'timestamp': datetime.now().isoformat()
    })
    
    time.sleep(3)  # 再过3秒后更新为翻译中
    current_task.update({
        'status': 'translating',
        'message': '正在翻译文档内容...',
        'timestamp': datetime.now().isoformat()
    })
    
    time.sleep(5)  # 再过5秒后完成(总共10秒)
    current_task.update({
        'status': 'completed',
        'message': '✅ 翻译完成',
        'translation_url': 'https://example.com/translated.pdf',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/status')
def get_status():
    # 直接返回当前任务状态
    return jsonify(current_task)
    
        
if __name__ == '__main__':
    app.run(port=5000, debug=True)
