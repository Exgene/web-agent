import asyncio
import os
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

dotenv.load_dotenv(".env")

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
        print("Cleaning up resources...")
        try:
            if self.browser:
                await self.browser.close()
                print("closed browser")
                self.browser = None

            if self.playwright:
                await self.playwright.stop()
                print("stopped playwright")
                self.playwright = None

        except Exception as e:
            print(f"Error during cleanup: {e}")

        return False

    async def create_playwright_instance(self):
        self.playwright = await async_playwright().start()
        proxy = proxies[0]

        chromium = self.playwright.chromium
        print(self.user_data_dir)
        self.browser = await chromium.launch_persistent_context(
            user_data_dir="./user_data_dir",
            headless=self.headless,
        )

    async def run(self):
        assert self.browser, "INTITIALZE THE PLAYWRIGHT INSTANCE"
        page = await self.browser.new_page()
        await page.goto("https://kausthubh.com")
        content = await page.content()
        print(content)
        await asyncio.sleep(4)


async def main():
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
    )

    res = llm.invoke(input="hello")
    print(res)
    async with PlaywrightInstance(headless=False) as p:
        await p.run()


if __name__ == "__main__":
    asyncio.run(main())
