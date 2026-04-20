from playwright.sync_api import sync_playwright, Page, expect
import time
from utils.data_generator import DataGenerator

def test_register_box(page: Page):
    page.goto('https://dev-cinescope.coconutqa.ru/register')

    username_locator = '[name="fullName"]'
    email_locator = '[name=email]'
    password_locator = '[name=password]'
    repeat_password_locator = '[name=passwordRepeat]'

    user_email = f"bulbagorbik{DataGenerator.generate_random_int_()}@test.com"
    user_password = '12345Bulbik.'

    page.fill(username_locator, 'Бульбагорб Сразужмяков Алькатрасович')
    page.fill(email_locator, user_email)
    page.fill(password_locator, user_password)
    page.fill(repeat_password_locator, user_password)

    page.click('[type=submit]')

    page.wait_for_url('https://dev-cinescope.coconutqa.ru/login')
    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)
    time.sleep(10)