import sys
from pathlib import Path

# 获取项目根目录（即 AutoBabelDocTranslator 目录）
project_root = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, project_root)  # 添加到搜索路径首位

from core.downloader.manager import DownloadManager
downloadmanager = DownloadManager("./papers")
url = "https://arxiv.org/abs/2501.00022"
arxiv_strategy = downloadmanager.get_strategy(url)
result = arxiv_strategy.download(url)
print("下载结果:", result)