# test/win/test_translate.py
import sys
from pathlib import Path

# 获取项目根目录（即 AutoBabelDocTranslator 目录）
project_root = str(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0, project_root)  # 添加到搜索路径首位

from core.translator import BabelDocTranslator
import asyncio

async def process_paper(pdf_path):
    # 2. 翻译文档
    translator = BabelDocTranslator()
    await translator.upload_file(pdf_path)

if __name__ == "__main__":
    # 示例：处理arXiv论文
    asyncio.run(process_paper(pdf_path=".\\papers\\REKnow_ Enhanced Knowledge for Joint Entity and Relation Extraction.pdf"
    ))