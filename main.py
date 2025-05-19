import asyncio
import os
from logging import INFO
from pathlib import Path
from typing import Optional

import dotenv
from langchain_groq import ChatGroq
from playwright.async_api import (
    BrowserContext,
    Playwright,
    ProxySettings,
    async_playwright,
)

from logger.logger import get_logger, setup_logger

dotenv.load_dotenv(".env")

setup_logger("main", INFO)
logger = get_logger("main")

if "GROQ_API_KEY" not in os.environ:
    assert "MISSING API KEYS"

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
        assert self.browser, "INTITIALZE THE PLAYWRIGHT INSTANCE"

        async with await self.browser.new_page() as page:
            await page.goto("https://kausthubh.com")
            content = await page.content()
            print(content)
            # logger.info("Content from the page:", content)
        await asyncio.sleep(4)


async def main():
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
    )

    res = llm.invoke(input="hello")
    print(res)
    # logger.info("res:", res)
    async with PlaywrightInstance(headless=False) as p:
        await p.run()


if __name__ == "__main__":
    asyncio.run(main())
