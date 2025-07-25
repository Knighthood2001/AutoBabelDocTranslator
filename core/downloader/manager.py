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

    # @classmethod
    # def register_strategy(cls, name: str, strategy_class):
    #     """
    #     注册新的下载策略。

    #     Args:
    #         cls (class): 需要注册下载策略的类。
    #         name (str): 下载策略的名称。
    #         strategy_class (class): 下载策略类。

    #     Returns:
    #         None
    #     """
    #     cls._strategy_map[name] = strategy_class
if __name__ == "__main__":
    downloadmanager = DownloadManager("/home/wu/code/papers")
    arxiv_strategy = downloadmanager.get_strategy("https://arxiv.org/abs/2206.05123")
    result = arxiv_strategy.download("https://arxiv.org/abs/2206.05123")
    print("下载结果:", result)