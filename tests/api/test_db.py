import pytest
import allure


@allure.feature("Database API")
class TestDB:
    @pytest.mark.db
    @allure.story("Database Requests")
    @allure.description(
        "Тест проверяет запросы к базе данных: получение пользователя по ID и проверку существования пользователя по email.")
    def test_db_requests(self, super_admin, db_helper, created_test_user):
        with allure.step("Проверяем, что созданный пользователь в тесте совпадает с пользователем, полученным из БД по ID"):
            assert created_test_user == db_helper.get_user_by_id(created_test_user.id)
        with allure.step("Проверяем, что пользователь с email 'api1@gmail.com' существует в БД"):
            assert db_helper.user_exists_by_email("api1@gmail.com")

    @pytest.mark.db
    @allure.story("Delete Movie Database Requests")
    @allure.description( "Тест проверяет запросы к базе данных при удалении фильма: проверка отсутствия, создание, проверка наличия, удаление, проверка отсутствия.")
    def test_delete_movie_requests(self, super_admin, db_helper, create_test_movie_hardcode):
        with allure.step("Проверяем, что фильма с ID 101010 нет в БД"):
            assert db_helper.movie_exists_by_id(101010) is False, "Фильм не найден"
        with allure.step("Создаем тестовый фильм в БД"):
            db_helper.create_test_movie(create_test_movie_hardcode)
        with allure.step("Проверяем, что фильм с ID 101010 теперь существует в БД"):
            assert db_helper.get_movie_by_id(101010), "Фильм не найден"
        with allure.step("Проверяем, что фильм по запросу GET также можно получить через API"):
            super_admin.api.movie_api.get_movie(movie_id=101010)
        with allure.step("Удаляем фильм через API"):
            super_admin.api.movie_api.delete_movie(movie_id=101010)
        with allure.step("Проверяем, что фильм с ID 101010 больше не существует в БД после удаления"):
            assert db_helper.movie_exists_by_id(101010) is False, "Фильм не был удален"
        with allure.step("Проверяем через API, что фильм был удален"):
            super_admin.api.movie_api.get_movie(movie_id=101010, expected_status=404)

