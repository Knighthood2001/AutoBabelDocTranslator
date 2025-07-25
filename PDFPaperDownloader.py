import os
import re
import requests
from urllib.parse import urlparse
from pathvalidate import sanitize_filename

# 抽象基类，定义下载策略的接口
class DownloadStrategy:
    def __init__(self, save_dir="."):
        self.save_dir = save_dir
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        os.makedirs(self.save_dir, exist_ok=True)

    def download(self, url, filename=None, save_dir=None):
        raise NotImplementedError("Subclasses should implement this method.")

# Arxiv 下载策略
class ArxivDownloadStrategy(DownloadStrategy):
    def _get_title_from_abs(self, abs_url):
        try:
            response = requests.get(abs_url, headers=self.headers, timeout=10)
            response.raise_for_status()

            # 方法1: 使用正则表达式提取标题
            title_match = re.search(
                r'<h1 class="title mathjax">(.*?)</h1>',
                response.text,
                re.DOTALL
            )

            if title_match:
                title = title_match.group(1)
                title = re.sub(r'<[^>]+>', '', title)
                title = re.sub(r'^\s*Title:\s*', '', title).strip()
                return title

            # 方法2: 备用方案 - 从页面标题提取
            title_match = re.search(
                r'<title>arXiv:\s*(.*?)\s*\[.*?\]</title>',
                response.text
            )
            if title_match:
                return title_match.group(1).strip()

            # 方法3: 最后尝试 - 使用论文ID
            paper_id = os.path.basename(urlparse(abs_url).path)
            return f"arxiv_{paper_id}"

        except requests.exceptions.RequestException as e:
            print(f"获取标题失败: {str(e)}")
            paper_id = os.path.basename(urlparse(abs_url).path)
            return f"arxiv_{paper_id}"

    def _extract_paper_id(self, url):
        if "arxiv.org/pdf/" in url or (url.endswith(".pdf") and "arxiv" in url):
            paper_id = os.path.basename(urlparse(url).path)
            if paper_id.endswith(".pdf"):
                paper_id = paper_id[:-4]
            return paper_id
        elif "/abs/" in url:
            return os.path.basename(urlparse(url).path)
        else:
            return url  # 直接传入ID的情况

    def download(self, url, filename=None, save_dir=None):
        current_save_dir = save_dir if save_dir is not None else self.save_dir
        os.makedirs(current_save_dir, exist_ok=True)

        paper_id = self._extract_paper_id(url)
        if "arxiv.org/pdf/" in url or (url.endswith(".pdf") and "arxiv" in url):
            pdf_url = url
            abs_url = f"https://arxiv.org/abs/{paper_id}"
        else:
            if "/abs/" in url:
                abs_url = url
            else:
                abs_url = f"https://arxiv.org/abs/{paper_id}"
            pdf_url = f"https://arxiv.org/pdf/{paper_id}"

        try:
            title = self._get_title_from_abs(abs_url)
            print(f"获取到论文标题: {title}")
        except Exception as e:
            print(f"获取标题失败: {str(e)}")
            title = None

        if not filename:
            if title:
                try:
                    clean_title = sanitize_filename(title, replacement_text="_")
                    filename = clean_title[:100]
                except ImportError:
                    filename = re.sub(r'[^\w\s-]', '', title).strip()[:50]
            else:
                filename = f"arxiv_{paper_id}"

        save_path = os.path.join(current_save_dir, f"{filename}.pdf")

        print(f"📥 开始下载: {pdf_url}")
        print(f"💾 保存路径: {save_path}")
        try:
            response = requests.get(pdf_url, stream=True, headers=self.headers, timeout=30)
            response.raise_for_status()

            file_size = int(response.headers.get('Content-Length', 0))
            if file_size > 0:
                size_mb = file_size / (1024 * 1024)
                print(f"📦 文件大小: {size_mb:.2f} MB")

            downloaded = 0
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if downloaded % (1024 * 1024) == 0 and file_size > 0:
                            percent = (downloaded / file_size) * 100
                            print(f"\r📊 下载进度: {percent:.1f}% ({downloaded/(1024*1024):.1f} MB)", end="")

            print(f"\n✅ 下载完成: {save_path}")
            return save_path

        except requests.exceptions.RequestException as e:
            print(f"❌ 下载失败: {e}")
            return None

# CVPR 下载策略
class CVPRDownloadStrategy(DownloadStrategy):
    def _guess_title_from_url(self, pdf_url):
        filename = os.path.basename(urlparse(pdf_url).path).replace(".pdf", "")
        return f"{filename}"

    def download(self, pdf_url, filename=None, save_dir=None):
        current_save_dir = save_dir if save_dir else self.save_dir
        os.makedirs(current_save_dir, exist_ok=True)

        if not filename:
            title = self._guess_title_from_url(pdf_url)
            filename = sanitize_filename(title)[:100] or "cvpr_paper"

        save_path = os.path.join(current_save_dir, f"{filename}.pdf")

        print(f"📥 开始下载: {pdf_url}")
        print(f"💾 保存路径: {save_path}")

        try:
            with requests.get(pdf_url, stream=True, headers=self.headers, timeout=30) as response:
                response.raise_for_status()
                total = int(response.headers.get('Content-Length', 0))
                if total > 0:
                    print(f"📦 文件大小: {total / (1024 * 1024):.2f} MB")

                downloaded = 0
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total > 0:
                                percent = downloaded / total * 100
                                print(f"\r📊 下载进度: {percent:.1f}% ({downloaded/(1024*1024):.1f} MB)", end="")
                print(f"\n✅ 下载完成: {save_path}")
                return save_path

        except requests.exceptions.RequestException as e:
            print(f"❌ 下载失败: {e}")
            return None

# 普通 PDF 下载策略
class GenericPDFDownloadStrategy(DownloadStrategy):
    def download(self, pdf_url, filename=None, save_dir=None):
        current_save_dir = save_dir if save_dir else self.save_dir
        os.makedirs(current_save_dir, exist_ok=True)

        if filename is None:
            basename = os.path.basename(urlparse(pdf_url).path)
            if basename.lower().endswith(".pdf"):
                filename = basename[:-4]
            else:
                filename = "downloaded_pdf"
        filename = sanitize_filename(filename)

        save_path = os.path.join(current_save_dir, f"{filename}.pdf")

        print(f"📥 开始下载: {pdf_url}")
        print(f"💾 保存到: {save_path}")

        try:
            with requests.get(pdf_url, stream=True, headers=self.headers, timeout=30) as response:
                response.raise_for_status()
                total = int(response.headers.get('Content-Length', 0))
                if total > 0:
                    print(f"📦 文件大小: {total / (1024 * 1024):.2f} MB")

                downloaded = 0
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total > 0:
                                percent = downloaded / total * 100
                                print(f"\r📊 下载进度: {percent:.1f}% ({downloaded/(1024*1024):.1f} MB)", end="")
            print(f"\n✅ 下载完成: {save_path}")
            return save_path

        except requests.exceptions.RequestException as e:
            print(f"❌ 下载失败: {e}")
            return None

# 上下文类，根据 URL 选择合适的下载策略
class PDFDownloader:
    def __init__(self, save_dir="."):
        self.save_dir = save_dir

    def download(self, url, filename=None, save_dir=None):
        if "arxiv.org" in url:
            strategy = ArxivDownloadStrategy(save_dir=self.save_dir)
        elif "openaccess.thecvf.com" in url:
            strategy = CVPRDownloadStrategy(save_dir=self.save_dir)
        else:
            strategy = GenericPDFDownloadStrategy(save_dir=self.save_dir)

        return strategy.download(url, filename, save_dir)

# 使用示例
if __name__ == "__main__":
    downloader = PDFDownloader(save_dir="/home/wu/code/papers")

    # 下载 Arxiv 论文
    # downloader.download("https://arxiv.org/pdf/2111.02045.pdf")

    # 下载 CVPR 论文
    downloader.download("https://openaccess.thecvf.com/content/CVPR2024/papers/Zhuang_Vlogger_Make_Your_Dream_A_Vlog_CVPR_2024_paper.pdf")

    # 下载普通 PDF
    # downloader.download("https://example.com/sample.pdf", filename="sample")
