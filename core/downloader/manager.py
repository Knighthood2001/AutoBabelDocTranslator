from typing import Dict, Type
from .strategies import (
    ArxivDownloadStrategy,
    CVPRDownloadStrategy,
    GenericPDFDownloadStrategy
)

class DownloadManager:
    _strategy_map = {
        "arxiv": ArxivDownloadStrategy,
        "cvpr": CVPRDownloadStrategy,
        "default": GenericPDFDownloadStrategy
    }

    def __init__(self, save_dir: str = "."):
        self.save_dir = save_dir

    def get_strategy(self, url: str):
        """根据URL获取合适的下载策略"""
        if "arxiv.org" in url:
            return self._strategy_map["arxiv"](self.save_dir)
        elif "openaccess.thecvf.com" in url:
            return self._strategy_map["cvpr"](self.save_dir)
        return self._strategy_map["default"](self.save_dir)
