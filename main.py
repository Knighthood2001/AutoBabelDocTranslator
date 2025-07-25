import asyncio
import argparse
from PDFPaperDownloader import PDFDownloader
from BabelDocHandler import BabelDocUploader

async def main(url):
    downloader = PDFDownloader(save_dir="/home/wu/code/papers")
    uploader = BabelDocUploader(storage_state="loginstate.json")
    
    # Download and upload the PDF
    input_file_path = downloader.download(url)
    await uploader.upload_file(input_file_path)
    print(f"✅ Successfully downloaded and uploaded: {url}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Download a PDF from arXiv and upload to BabelDoc for translation')
    parser.add_argument('url', type=str, help='URL of the PDF to download and translate')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run the async main function
    asyncio.run(main(args.url))