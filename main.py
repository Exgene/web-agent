import asyncio
from logging import INFO
from pathlib import Path
from typing import Optional

from playwright.async_api import (
    BrowserContext,
    Playwright,
    ProxySettings,
    async_playwright,
)

from src.clients.groq import GroqClient
from src.logger.logger import get_logger, setup_logger
from src.tool_calls.web_tools import WebTools

setup_logger("main", INFO)
logger = get_logger("main")

proxies: list[ProxySettings] = [
    {"server": "", "username": "", "password": ""},
    {"server": "", "username": "", "password": ""},
]


class PlaywrightInstance:
    def __init__(self, headless: bool = True) -> None:
        self.playwright: Optional[Playwright]
        self.browser: Optional[BrowserContext]
        self.user_data_dir: Path = Path("./user_data_dir")
        self.headless = headless

    async def __aenter__(self):
        await self.create_playwright_instance()
        return self

    async def __aexit__(self, exc_t, exc_v, exc_tb):
        logger.info("Cleaning up resources...")
        try:
            if self.browser:
                await self.browser.close()
                logger.debug("closed browser")
                self.browser = None

            if self.playwright:
                await self.playwright.stop()
                logger.debug("stopped playwright")
                self.playwright = None

        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

        return False

    async def create_playwright_instance(self):
        self.playwright = await async_playwright().start()
        proxy = proxies[0]

        chromium = self.playwright.chromium
        logger.debug("User Data Directory:", self.user_data_dir)
        self.browser = await chromium.launch_persistent_context(
            user_data_dir="./user_data_dir",
            headless=self.headless,
        )
        logger.info("Successfully initialized browser")

    async def run(self):
        assert self.browser, "INITIALIZE THE PLAYWRIGHT INSTANCE"
        llm = GroqClient().create_client()

        async with await self.browser.new_page() as page:
            tools = WebTools(page)
            if await tools.check_for_captcha(llm):
                logger.info("CAPTCHA detected. Waiting for user instruction.")
                return

            await tools.search_url("https://www.google.com")
            await tools.type_text(text="Kausthubh J Rao")
            content = await tools.get_page_content()
            llm_response = llm.invoke(
                input=f"Out of these select the one which seems most likely to be a portfolio website: {content[:1000]}, Return its link"
            )
            await tools.search_url(llm_response.content.strip())


async def main():
    async with PlaywrightInstance(headless=False) as p:
        await p.run()


if __name__ == "__main__":
    asyncio.run(main())
