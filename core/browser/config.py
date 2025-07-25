from dataclasses import dataclass
from typing import List, Optional, Dict

import getScreenSize
width, height = getScreenSize.get_screen_size()
# 浏览器会话配置
@dataclass
class BrowserProfile:
    storage_state: str = "loginstate.json"
    viewport: Optional[Dict[str, int]] = None
    screen: Optional[Dict[str, int]] = None  # 改为单一字典
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    accept_downloads: bool = True

    def __post_init__(self):
        if self.viewport is None:
            width, height = getScreenSize.get_screen_size()
            self.viewport = {'width': width, 'height': height}

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
