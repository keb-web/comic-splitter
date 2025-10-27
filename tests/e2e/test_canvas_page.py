import pytest
import re
from playwright.async_api import Page, expect


@pytest.mark.asyncio(loop_scope='session')
async def test_has_title(page: Page):
    await page.goto("http://localhost:5173/")
    await expect(page).to_have_title(re.compile("Comic Splitter"))
