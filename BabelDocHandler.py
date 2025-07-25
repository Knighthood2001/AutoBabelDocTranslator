import os
import time
import asyncio
from dataclasses import dataclass
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import getScreenSize

@dataclass
class BrowserConfig:
    browser_type: str = "chromium"
    headless: bool = False
    args: list = None

    def __post_init__(self):
        if self.args is None:
            self.args = [
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            ]

class BabelDocUploader:
    def __init__(self, storage_state="loginstate.json", browser_config=None):
        self.storage_state = storage_state
        self.browser_config = browser_config or BrowserConfig()
        # self.viewport = {'width': 1920, 'height': 1080}
        width, height = getScreenSize.get_screen_size()
        self.viewport = {'width': width-50, 'height': height-50}
        self.login_required_selector = "#immediateLogin"
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def _launch_browser(self):
        if self.playwright is None:
            self.playwright = await async_playwright().start()
            browser_launcher = getattr(self.playwright, self.browser_config.browser_type)
            self.browser = await browser_launcher.launch(
                headless=self.browser_config.headless,
                args=self.browser_config.args,
                ignore_default_args=['--enable-automation']
            )
            self.context = await self.browser.new_context(
                viewport=self.viewport,
                no_viewport=False,
                accept_downloads=True,
                storage_state=self.storage_state if os.path.exists(self.storage_state) else None
            )
            self.page = await self.context.new_page()
        return self.playwright, self.browser, self.context, self.page

    async def save_login_state(self, login_url="https://app.immersivetranslate.com/babel-doc", wait_seconds=60):
        playwright, browser, context, page = await self._launch_browser()
        await page.goto(login_url)
        print(f"请在 {wait_seconds} 秒内完成手动登录...")
        await asyncio.sleep(wait_seconds)
        await context.storage_state(path=self.storage_state)
        print(f"✅ 登录状态已保存至 {self.storage_state}")

    async def _check_login(self, page, context, relogin_seconds=60):
        try:
            await page.wait_for_selector(self.login_required_selector, timeout=3000)
            print("⚠️ 检测到未登录状态，等待手动登录...")
            await asyncio.sleep(relogin_seconds)
            await context.storage_state(path=self.storage_state)
            print(f"✅ 登录状态更新并保存至 {self.storage_state}")
            return False
        except PlaywrightTimeoutError:
            print("✅ 已检测到已登录状态")
            return True

    async def close(self):
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None

    async def upload_file(self, input_file, target_url="https://app.immersivetranslate.com/babel-doc", relogin_seconds=60):
        playwright, browser, context, page = await self._launch_browser()
        await page.goto(target_url)
        print(f"🌐 页面标题: {await page.title()}")

        logged_in = await self._check_login(page, context, relogin_seconds)
        if not logged_in:
            await page.goto(target_url)
            print("🔄 已刷新页面")

        await page.set_input_files('input#file-input', input_file)
        print(f"📄 已上传文件: {input_file}")

        try:
            await asyncio.sleep(2)
            validate_button = await page.wait_for_selector('xpath=//*[@id="turnstile-container"]/div[1]/div[1]/div[1]', timeout=2000)
            await validate_button.click()
            print("✅ 已点击验证按钮")

            translate_button = await page.wait_for_selector('#immediateTranslate', timeout=10000)
            await translate_button.click()
            print("✅ 已点击翻译按钮")
        except PlaywrightTimeoutError:
            print("❌ 未找到验证或翻译按钮，可能页面结构已变化或加载超时")
        except Exception as e:
            print(f"❌ 上传或翻译过程发生错误: {e}")


        # 创建 asyncio 事件
        closed_event = asyncio.Event()

        # 定义关闭事件回调
        def on_close():
            print("✅ 页面已关闭，流程结束")
            closed_event.set()

        page.on("close", lambda _: on_close())

        # 等待页面关闭
        await closed_event.wait()

# ========== 使用示例 ==========

if __name__ == "__main__":
    uploader = BabelDocUploader(storage_state="loginstate.json")

    async def main():
        # 第一次使用前执行保存登录状态
        # await uploader.save_login_state(wait_seconds=30)

        # 上传文件进行翻译
        input_file = "/home/wu/code/papers/Zhuang_Vlogger_Make_Your_Dream_A_Vlog_CVPR_2024_paper.pdf"
        await uploader.upload_file(input_file)

    asyncio.run(main())