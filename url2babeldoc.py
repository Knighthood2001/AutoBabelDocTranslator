from PDFPaperDownloader import PDFDownloader
from BabelDocHandler import *
import asyncio

downloader = PDFDownloader(save_dir="G:/Desktop/pythondemo/AutoBabelDocTranslator/papers")
uploader = BabelDocUploader(storage_state="loginstate.json")




async def main():
    # 上传文件进行翻译
    input_file_path = downloader.download("https://arxiv.org/pdf/2111.02045.pdf")
    await uploader.upload_file(input_file_path)


if __name__ == "__main__":
    asyncio.run(main())