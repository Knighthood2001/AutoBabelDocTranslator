import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.downloader.manager import DownloadManager
from core.translator import BabelDocTranslator
import json
from pathlib import Path

async def process_paper(url: str, save_dir: str = "./papers"):
    """Modified to return status information"""
    result = {
        'status': 'processing',
        'message': '',
        'pdf_path': '',
        'translation_url': ''
    }
    
    try:
        # 1. Download paper
        downloader = DownloadManager(save_dir)
        strategy = downloader.get_strategy(url)
        pdf_path = strategy.download(url)
        
        if not pdf_path:
            result['status'] = 'error'
            result['message'] = '❌ Failed to download paper'
            return result

        result['pdf_path'] = str(pdf_path)
        result['message'] = '✅ Paper downloaded successfully'
        
        # 2. Translate document
        translator = BabelDocTranslator()
        translation_url = await translator.upload_file(pdf_path)
        
        result['status'] = 'completed'
        result['message'] = '✅ Translation completed'
        result['translation_url'] = translation_url
        
    except Exception as e:
        result['status'] = 'error'
        result['message'] = f'❌ Error: {str(e)}'
    
    return result

def run_translation(url, save_dir):
    """Synchronous wrapper for async process"""
    return asyncio.run(process_paper(url, save_dir))
