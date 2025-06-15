from playwright.sync_api import Page

from src.actions.page_actions import PageActions
from src.components.header import Header
from src.enums.hosts import BASE_URL

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self._base_url = BASE_URL
        self._endpoint = ''
        self.actions = PageActions(page)
        self.header = Header(self.actions)

    def _get_url(self, endpoint: str) -> str:
        return self._base_url + endpoint
