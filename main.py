from logging import INFO
from pathlib import Path
from typing import Optional

from playwright.async_api import (
    BrowserContext,
    Playwright,
    ProxySettings,
    async_playwright,
)

from src.agents.task_separator import TaskSeperatorAgent
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

        async with await self.browser.new_page() as page:
            tools = WebTools(page)
            await tools.search_url("https://www.google.com")
            await tools.type_text(text="Kausthubh J Rao")
            # You will probably never use it like this
            # await tools.search_url(llm_response.content.strip())


async def main():
    async with PlaywrightInstance(headless=False) as p:
        await p.run()


if __name__ == "__main__":
    llm, model = GroqClient().create_sync_client()
    # llm_response = llm.chat.completions.create(
    #     model=model,
    #     messages=[
    #         {
    #             "role": "system",
    #             "content": "You are a helpful assistant.",
    #         },
    #         {
    #             "role": "user",
    #             "content": "Explain the importance of low latency LLMs",
    #         },
    #     ],
    # )
    # logger.info(llm_response)

    agent = TaskSeperatorAgent(
        llm=llm,
        input="Navigate to kausthubh j rao and analyze the content",
        model=model,
    )
    _ = agent.run()
    # logger.info(agent.system_prompt)
    # logger.info(json.dumps(agent.tool_calls, indent=2))
    # logger.info(f"Output from agent separate: {agent.run()}")
    # logger.info(agent.tool_calls)
# asyncio.run(main())
