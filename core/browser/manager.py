from playwright.async_api import async_playwright
from .config import BrowserConfig, BrowserProfile
from typing import Tuple
import os
class BrowserManager:
    def __init__(self, config: BrowserConfig = None, profile: BrowserProfile = None):
        self.config = config or BrowserConfig()
        self.profile = profile or BrowserProfile()
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None

    # async def launch(self) -> Tuple:
    #     """异步启动浏览器并返回(playwright, browser, context, page)"""
    #     if not self._playwright:
    #         self._playwright = await async_playwright().start()
    #         browser_launcher = getattr(self._playwright, self.config.type)
            
    #         self._browser = await browser_launcher.launch(
    #             headless=self.config.headless,
    #             args=self.config.args,
    #             ignore_default_args=self.config.ignore_default_args
    #         )
    #         if not os.path.exists(self.profile.storage_state):
    #             with open(self.profile.storage_state, "w") as f:
    #                 f.write("{}")  # 写入空JSON对象

    #         self._context = await self._browser.new_context(
    #             viewport=self.profile.viewport,
    #             screen=self.profile.screen,
    #             storage_state=self.profile.storage_state,
    #             user_agent=self.profile.user_agent,
    #             accept_downloads=self.profile.accept_downloads
    #         )
            
    #         self._page = await self._context.new_page()
        
    #     return self._playwright, self._browser, self._context, self._page

    async def launch(self) -> Tuple:
        """异步启动浏览器并返回(playwright, browser, context, page)"""
        if not self._playwright:
            self._playwright = await async_playwright().start()
            browser_launcher = getattr(self._playwright, self.config.type)
            
            # 准备启动参数
            launch_options = {
                "headless": self.config.headless,
                "args": self.config.args,
                "ignore_default_args": self.config.ignore_default_args
            }
            
            # 如果配置了 channel 参数，添加到启动选项
            if self.config.channel:
                launch_options["channel"] = self.config.channel
            
            # 启动浏览器
            self._browser = await browser_launcher.launch(**launch_options)
            
            # 检查存储状态文件是否存在，不存在则创建
            if not os.path.exists(self.profile.storage_state):
                with open(self.profile.storage_state, "w") as f:
                    f.write("{}")  # 写入空JSON对象

            # 创建浏览器上下文
            self._context = await self._browser.new_context(
                viewport=self.profile.viewport,
                screen=self.profile.screen,
                storage_state=self.profile.storage_state,
                user_agent=self.profile.user_agent,
                accept_downloads=self.profile.accept_downloads
            )
            
            # 创建新页面
            self._page = await self._context.new_page()
        
        return self._playwright, self._browser, self._context, self._page


    async def close(self):
        """关闭浏览器资源"""
        if self._browser:
            await self._browser.close()  # 关闭浏览器
            self._browser = None
        if self._playwright:
            await self._playwright.stop()  # 停止playwright
            self._playwright = None   # 清空playwright

    async def save_login_state(self, path: str = None):
        """保存当前登录状态"""
        if not self._context:
            await self.launch()
        await self._context.storage_state(path=path or self.profile.storage_state)
