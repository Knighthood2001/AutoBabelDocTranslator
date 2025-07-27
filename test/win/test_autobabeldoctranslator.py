# test/win/test_downloadPDF.py
import sys
from pathlib import Path

# 获取项目根目录（即 AutoBabelDocTranslator 目录）
project_root = str(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0, project_root)  # 添加到搜索路径首位

import asyncio
from core.downloader.manager import DownloadManager
from core.translator import BabelDocTranslator

async def process_paper(url: str, save_dir: str = "./papers"):
    # 1. 下载论文
    downloader = DownloadManager(save_dir)
    strategy = downloader.get_strategy(url)
    pdf_path = strategy.download(url)
    
    if not pdf_path:
        print("❌ 论文下载失败")
        return

    # 2. 翻译文档
    translator = BabelDocTranslator()
    await translator.upload_file(pdf_path)

if __name__ == "__main__":
    # 示例：处理arXiv论文
    asyncio.run(process_paper(
        "https://arxiv.org/pdf/2501.00009"
    ))
