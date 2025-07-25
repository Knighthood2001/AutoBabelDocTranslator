from dataclasses import dataclass
from typing import List, Optional

# 浏览器会话配置
@dataclass
class BrowserProfile:
    storage_state: str = "loginstate.json"   # 存储登录状态的JSON文件路径
    viewport: Optional[dict] = None   # 浏览器视口大小，默认None表示使用默认值
    screen: Optional[dict] = None   # 浏览器屏幕大小，默认None表示使用默认值
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"   # 浏览器用户代理
    accept_downloads: bool = True   # 是否允许下载文件，默认为True

# 浏览器配置
@dataclass
class BrowserConfig:
    type: str = "chromium"  # chromium, firefox, webkit  # 浏览器类型
    headless: bool = False   # 是否以无头模式运行，默认为False
    args: Optional[List[str]] = None  # 浏览器启动参数，默认为None
    ignore_default_args: Optional[List[str]] = None   # 忽略的默认启动参数，默认为None
    
    def __post_init__(self):
        self.args = self.args or [
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            '--disable-dev-shm-usage'
        ]
        self.ignore_default_args = self.ignore_default_args or ['--enable-automation']
