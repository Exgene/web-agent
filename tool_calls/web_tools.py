from logging import INFO
from typing import Optional

from langchain_groq import ChatGroq
from playwright.async_api import Page

from logger.logger import get_logger, setup_logger

setup_logger("web_tools", INFO)
logger = get_logger("web_tools")


class WebTools:
    def __init__(self, page: Page):
        self.page = page

    async def search_url(self, url: str) -> None:
        """Navigate to a specific URL"""
        await self.page.goto(url)

    async def get_page_content(self) -> str:
        """Get the current page content"""
        return await self.page.content()

    async def click_button(self, selector: str) -> None:
        """Click a button using selector"""
        await self.page.click(selector)

    async def type_text(self, selector: str | None = None, text: str = "") -> None:
        """Type text into the first selectable input field or specified selector"""
        if selector:
            await self.page.fill(selector, text)
        else:
            input_selector = 'input:not([disabled]):not([type="hidden"]):visible'
            await self.page.wait_for_selector(input_selector)
            await self.page.fill(input_selector, text)

    async def wait_for_selector(self, selector: str, timeout: int = 5000) -> None:
        """Wait for an element to appear"""
        await self.page.wait_for_selector(selector, timeout=timeout)

    # Not sure if i need this or not, Lets see
    async def check_for_captcha(self, llm: ChatGroq) -> bool:
        """Check if there's a captcha on the page"""
        content = await self.get_page_content()
        is_captcha = llm.invoke(
            input=f"Is there a captcha on the page? {content}, Only return True or False"
        )
        if type(is_captcha.content) is str:
            print(is_captcha.content.strip())
            return is_captcha.content.strip() == "True"

        logger.error("Couldnt parse the string ::", is_captcha.content)
        return False

    async def get_element_text(self, selector: str) -> Optional[str]:
        """Get text content of an element"""
        element = await self.page.query_selector(selector)
        if element:
            return await element.text_content()
        return None

