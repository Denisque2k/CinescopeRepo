from playwright.sync_api import sync_playwright, Page, expect
import time
import allure
import pytest
from conftest import browser
from models.page_object_models import CinescopeRegisterPage
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

@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Register")
@pytest.mark.ui
class TestRegisterPage:
   @allure.title("Проведение успешной регистрации")
   def test_register_by_ui(self):
      with sync_playwright() as playwright:
           #Подготовка данных для регистрации
           random_email = DataGenerator.generate_random_email()
           random_name = DataGenerator.generate_random_name()
           random_password = DataGenerator.generate_random_password()

           browser = playwright.chromium.launch(headless=False)  # Запуск браузера headless=False для визуального отображения
           page = browser.new_page()

           register_page = CinescopeRegisterPage(page) # Создаем объект страницы регистрации cinescope
           register_page.open()
           register_page.register(f"PlaywrightTest {random_name}", random_email, random_password, random_password)# Выполняем регистрацию

           register_page.assert_was_redirect_to_login_page()  # Проверка редиректа на страницу /login
           register_page.make_screenshot_and_attach_to_allure() # Прикрепляем скриншот
           register_page.assert_alert_was_pop_up() # Проверка появления и исчезновения алерта

           # Пауза для визуальной проверки (нужно удалить в реальном тестировании)
           time.sleep(5)
           browser.close()
