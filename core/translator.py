import os
import asyncio
import time
from typing import Optional
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError
from .browser.manager import BrowserManager
from .browser.config import BrowserProfile

from utils import logger

class BabelDocTranslator:
    def __init__(
        self,
        storage_state: str = "loginstate.json",
        browser_config: Optional[dict] = None,
        browser_profile: Optional[dict] = None
    ):
        profile = BrowserProfile(**(browser_profile or {}))
        profile.storage_state = storage_state
        
        self.manager = BrowserManager(
            config=browser_config or {},
            profile=profile
        )
        self.login_selector = "#immediateLogin"  # 立即登录 按钮
        self.uploadFile = '#uploadFile'   # 上传文件并翻译 按钮
        self.captcha_selector = 'xpath=//*[@id="turnstile-container"]/div[1]/div[1]/div[1]'  # 点击按钮开始验证 按钮
        self.translate_selector = "#immediateTranslate"   # 立即翻译 按钮
        self.file_input_selector = "input#file-input"   # 文件注入


    async def upload_file(
        self,
        input_file: str,
        target_url: str = "https://app.immersivetranslate.com/babel-doc",
    ):
        """上传并翻译文件"""
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"输入文件不存在: {input_file}")

        _, _, _, page = await self.manager.launch()
        
        try:
            # 登录检查流程
            await self._ensure_logged_in(page, target_url)
            
            # 文件上传流程
            await self._upload_and_translate(page, input_file)
            
            # 等待完成
            await self._wait_for_completion(page)
            
        finally:
            await self.manager.close()


    async def _ensure_logged_in(self, page: Page, url: str, max_wait_seconds: int = 60):
        """确保已登录状态"""
        await page.goto(url)
        
        try:
            # 先检查是否显示登录按钮
            await page.wait_for_selector(self.login_selector, timeout=10000)  # 太短可能会导致跳过登录
            logger.info("⚠️ 需要登录，请手动登录...")
            
            start_time = time.time()
            while True:
                # 检查上传文件按钮是否存在（表示已登录）
                try:
                    await page.wait_for_selector(self.uploadFile, timeout=10000)
                    logger.info("✅ 登录成功，已检测到上传按钮")
                    await self.manager.save_login_state()  # 保存登录状态
                    return
                except PlaywrightTimeoutError:
                    pass
                
                # 检查是否超时
                if time.time() - start_time > max_wait_seconds:
                    logger.error(f"等待登录超时（{max_wait_seconds}秒）")
                    raise TimeoutError(f"等待登录超时（{max_wait_seconds}秒）")
                
                # 短暂等待后继续检查
                await asyncio.sleep(1)
                
        except PlaywrightTimeoutError:
            # 如果一开始就没找到登录按钮，说明已经登录
            logger.info("✅ 已处于登录状态")


    async def _upload_and_translate(self, page: Page, file_path: str):
        """执行文件上传和翻译"""
        await page.set_input_files(self.file_input_selector, file_path)
        logger.info(f"📄 已上传文件: {file_path}")

        try:
            await asyncio.sleep(2)  # 等待验证码加载
            await page.click(self.captcha_selector)
            logger.info("✅ 已通过验证")
            
            await page.click(self.translate_selector)
            logger.info("✅ 已开始翻译")
        except Exception as e:
            logger.error(f"❌ 翻译过程中出错: {e}")
            raise

    async def _wait_for_completion(self, page: Page):
        """等待翻译完成"""
        event = asyncio.Event()
        page.on("close", lambda _: event.set())
        await event.wait()
        logger.info("✅ 翻译流程完成")
