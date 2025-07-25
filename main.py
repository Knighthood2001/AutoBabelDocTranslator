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
        "https://arxiv.org/abs/2107.12090",
        save_dir="/home/wu/code/papers"
    ))
