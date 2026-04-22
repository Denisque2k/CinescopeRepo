from playwright.sync_api import Page

class CinescopeRegisterPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://dev-cinescope.coconutqa.ru/register"

        # Локаторы элементов
        self.home_button = "a[href='/' and text()='Cinescope']"
        self.all_movies_button = "a[href='/movies' and text()='Все фильмы']"

        self.full_name_input = "input[name='fullName']"
        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"
        self.password_repeat = "input[name='passwordRepeat']"

        self.register_button = "button[text()='Зарегистрироваться']"
        self.sign_button ="button[text()='Войти']"