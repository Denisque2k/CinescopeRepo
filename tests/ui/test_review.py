from models.page_object_models import TestAddReview
from playwright.sync_api import sync_playwright
from utils.data_generator import DataGenerator
import time
import allure
import pytest

@allure.epic("Тестирование UI")
@allure.feature("Тестирование написания и сохранения отзывов под фильмами")
@pytest.mark.ui
class TestReviewOnFilm:
    @allure.title("Проверка на успешное написание и сохранение отзыва")
    def test_review_on_film(self, registered_user):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()
            test_review_page = TestAddReview(page)

            with allure.step("Открыть страницу добавления отзыва"):
                test_review_page.open()

            with allure.step(f"Авторизоваться как пользователь {registered_user.email}"):
                test_review_page.login(registered_user.email, registered_user.password)

            with allure.step("Перейти на страницу фильма"):
                test_review_page.go_to_movie_page()

            review_text = "Random review text"
            with allure.step(f"Написать текст отзыва: '{review_text}'"):
                test_review_page.write_text_review(review_text)

            rating = DataGenerator.generate_random_num_for_one_to_five()
            with allure.step(f"Установить рейтинг: {rating} из 5"):
                test_review_page.choose_rating(rating)

            with allure.step("Проверить появление подтверждающего уведомления"):
                test_review_page.assert_alert_was_pop_up()

            with allure.step("Сделать скриншот и прикрепить к отчету"):
                test_review_page.make_screenshot_and_attach_to_allure()

            time.sleep(5)
            browser.close()