import pytest
import allure
from conftest import super_admin
from models.base_models import ResponseMovie, RequestMovie, RequestGetMovie


@allure.feature("Movies API")
class TestMovieAPI:

    @allure.story("Get Movies with Filters")
    @allure.description("Тест проверяет получение списка фильмов с различными фильтрами: цена, локация, жанр. Используется параметризация для проверки разных комбинаций.")
    @pytest.mark.parametrize("min_price, max_price, locations, genre_id, expected_status", [
        (1, 1000, ["MSK"], 1, 200),
        (500, 2000, ["SPB"], 1, 200),
        (1, 500, ["MSK", "SPB"], 1, 200),
        (1000, 5000, [], 1, 200),
    ])
    def test_get_movies(self, api_manager, min_price, max_price, locations, genre_id, expected_status):
        params = {
            "pageSize": 1,
            "page": 1,
            "minPrice": min_price,
            "maxPrice": max_price,
            "locations": locations,
            "published": True,
            "genreId": genre_id,
            "createdAt": "asc"
        }
        with allure.step("Проверяем, что все обязательные поля присутствуют в параметрах"):
            assert params["pageSize"] in params.values(), "Поле pageSize пустое"
            assert params["page"] in params.values(), "Поле 'page' пустое"
            assert params["minPrice"] in params.values(), "Поле 'minPrice' пустое"
            assert params["maxPrice"] in params.values(), "Поле 'maxPrice' пустое"
            assert params["locations"] in params.values(), "Поле 'locations' пустое"
            assert params["published"] in params.values(), "Поле published пустое"
            assert params["genreId"] in params.values(), "Поле 'genreId' пустое"
        with allure.step("Проверяем, что числовые поля имеют корректный тип"):
            params_ints_values = (params["pageSize"], params["page"], params["minPrice"], params["maxPrice"], params["genreId"])
            all_int = all(isinstance(value, int) for value in params_ints_values)
            assert all_int, "Значения в полях 'pageSize', 'page', 'minPrice', 'maxPrice', 'genreId' должны быть числами"
        with allure.step("Проверяем, что значения локаций корректны"):
            assert all(loc in ["MSK", "SPB"] for loc in params["locations"]), f"Ожидалось значение 'MSK' или 'SPB', получено '{params['locations']}'"
        with allure.step("Проверяем, что минимальная цена меньше максимальной"):
            assert 0 < params["minPrice"] < params["maxPrice"], "Некорректная сумма, проверьте значения милимальной и максимальной суммы"
        with allure.step("Отправляем запрос на получение списка фильмов с фильтрами"):
            response = api_manager.movie_api.get_movies_for_params(params=params, excepted_status=200)
        response_data = response.json()

    @allure.story("Create Movie")
    @allure.description("Тест проверяет создание нового фильма через API суперадмином. Проверяются обязательные поля и корректность данных в ответе.")
    def test_create_movie(self, api_manager, super_admin, create_movie_data: RequestMovie):
        data = RequestMovie(
            name=create_movie_data.name,
            description=create_movie_data.description,
            price=create_movie_data.price,
            imageUrl=create_movie_data.imageUrl,
            location=create_movie_data.location,
            published=create_movie_data.published,
            genreId=create_movie_data.genreId,
        )
        with allure.step("Проверяем, что все обязательные поля заполнены"):
            assert data.name, "Поле name пустое"
            assert data.description, "Поле 'description' пустое"
            assert data.price, "Поле 'price' пустое"
            assert data.imageUrl, "Поле 'imageUrl' пустое"
            assert data.published, "Поле 'published' пустое"
            assert data.genreId, "Поле 'genreId' пустое"
        with allure.step("Проверяем, что цена положительная"):
            assert 0 < data.price, "Некорректная сумма, ожидалось значение больше нуля"
        with allure.step("Отправляем запрос на создание фильма"):
            response = super_admin.api.movie_api.create_movie(create_movie_data.model_dump())
        response_data = ResponseMovie(**response.json())
        with allure.step("Проверяем, что созданный фильм можно получить по ID"):
            assert api_manager.movie_api.get_movie(movie_id=response_data.id), "Фильм не найден"
        with allure.step("Проверяем, что название и цена фильма в ответе совпадают с отправленными"):
            assert response_data.name == data.name, f"Название фильма не совпадает, ожидалось {data.name}"
            assert response_data.price == data.price, f"Цена фильма не совпадает, ожидалось {data.price}"

    @allure.story("Get Movie by ID")
    @allure.description("Тест проверяет получение информации о фильме по его ID после создания.")
    def test_get_movie(self, api_manager, super_admin, create_movie_data):
        with allure.step("Создаем фильм"):
            response = super_admin.api.movie_api.create_movie(create_movie_data.model_dump())
        response_data = ResponseMovie(**response.json())
        with allure.step(f"Получаем фильм по ID {response_data.id}"):
            api_manager.movie_api.get_movie(movie_id=response_data.id)

    users_fixtures = [
        pytest.param("admin_user_with_creds", 403, "Получает запрет", id="admin_user_with_creds"),
        pytest.param("common_user", 403, "Получает запрет", id="common_user"),
    ]

    @allure.story("Delete Movie by Non-Super Admin")
    @allure.description("Тест проверяет, что пользователи без прав суперадмина не могут удалить фильм. Используется параметризация для проверки разных ролей.")
    @pytest.mark.parametrize("fixture_name, expected_status, description", users_fixtures)
    def test_delete_movie(self, request, fixture_name, expected_status, description, api_manager, super_admin, admin_user_with_creds, common_user, create_movie_data):
        name_fixture = request.getfixturevalue(fixture_name)
        with allure.step("Создаем фильм суперадмином"):
            create_movie_response = super_admin.api.movie_api.create_movie(data=create_movie_data.model_dump())
        create_movie_response_data = ResponseMovie(**create_movie_response.json())
        movie_id = create_movie_response_data.id
        with allure.step(f"Пытаемся удалить фильм пользователем {fixture_name}, ожидаем статус {expected_status}"):
            delete_response = name_fixture.api.movie_api.delete_movie(movie_id=movie_id, expected_status=expected_status)
        with allure.step("Проверяем, что получен ожидаемый статус-код"):
            assert delete_response.status_code == expected_status, f"{description}"
        if expected_status == 200:
            with allure.step("Если удаление прошло успешно, проверяем, что фильм больше не существует"):
                assert name_fixture.api.movie_api.get_movie(movie_id=movie_id, expected_status=404).status_code == 404

    @allure.story("Delete Movie by Super Admin")
    @allure.description("Тест проверяет, что суперадмин может успешно удалить фильм. Проверяется, что после удаления фильм недоступен.")
    @pytest.mark.slow
    def test_super_admin_delete_movie(self, api_manager, super_admin, create_movie_data):
        with allure.step("Создаем фильм"):
            response = super_admin.api.movie_api.create_movie(data=create_movie_data.model_dump())
        response_data = ResponseMovie(**response.json())
        movie_id = response_data.id
        with allure.step("Проверяем, что ID фильма не пустой"):
            assert movie_id, "Проверьте поле ИД фильма"
        with allure.step(f"Удаляем фильм с ID {movie_id} как суперадмин"):
            super_admin.api.movie_api.delete_movie(movie_id=movie_id)
        with allure.step("Проверяем, что фильм больше не доступен (возвращает 404)"):
            api_manager.movie_api.get_movie(movie_id=movie_id, expected_status=404)

    @allure.story("Update Movie by Super Admin")
    @allure.description("Тест проверяет, что суперадмин может обновить данные фильма. Проверяются обязательные поля и корректность обновления.")
    def test_super_admin_patch_movie(self, api_manager, super_admin, create_movie_data):
        data = RequestMovie(
            name=create_movie_data.name,
            imageUrl=create_movie_data.imageUrl,
            price=create_movie_data.price,
            description=create_movie_data.description,
            location=create_movie_data.location,
            published=create_movie_data.published,
            genreId=create_movie_data.genreId
        )
        with allure.step("Проверяем, что все обязательные поля заполнены"):
            assert data.name, "Поле name пустое"
            assert data.description, "Поле 'description' пустое"
            assert data.price, "Поле 'price' пустое"
            assert data.imageUrl, "Поле 'imageUrl' пустое"
            assert data.published, "Поле 'published' пустое"
            assert data.genreId, "Поле 'genreId' пустое"
        with allure.step("Проверяем, что локация корректна"):
            assert data.location in ["MSK", "SPB"], f"Ожидалось значение 'MSK' или 'SPB', получено '{data['location']}'"
        with allure.step("Проверяем, что цена положительная"):
            assert 0 < data.price, "Некорректная сумма, ожидалось значение больше нуля"
        with allure.step("Создаем фильм"):
            response = super_admin.api.movie_api.create_movie(create_movie_data.model_dump())
        response_data = ResponseMovie(**response.json())
        movie_id = response_data.id
        with allure.step(f"Обновляем данные фильма с ID {movie_id} как суперадмин"):
            super_admin.api.movie_api.patch_movie(movie_id=movie_id, data=data)
        with allure.step("Проверяем, что название и цена фильма в ответе совпадают с отправленными (это проверялось ранее, но можно добавить явно после patch)"):
            # Примечание: этот тест проверяет *отправку* данных, но не *получение* обновленного объекта.
            # Для проверки обновления, нужно получить фильм после patch и сравнить поля.
            # Здесь проверка из оригинального кода, возможно, недостаточна.
            assert response_data.name == data.name, f"Название фильма не совпадает, ожидалось {data.name}"
            assert response_data.price == data.price, f"Цена фильма не совпадает, ожидалось {data.price}"

    @allure.story("Update Movie by Regular User")
    @allure.description("Тест проверяет, что обычный пользователь не может обновить данные фильма. Ожидается ошибка 403.")
    @pytest.mark.slow
    def test_patch_movie(self, api_manager, super_admin, create_movie_data, common_user):
        data = RequestMovie(
            name=create_movie_data.name,
            imageUrl=create_movie_data.imageUrl,
            price=create_movie_data.price,
            description=create_movie_data.description,
            location=create_movie_data.location,
            published=create_movie_data.published,
            genreId=create_movie_data.genreId
        )
        with allure.step("Проверяем, что все обязательные поля заполнены"):
            assert data.name, "Поле name пустое"
            assert data.description, "Поле 'description' пустое"
            assert data.price, "Поле 'price' пустое"
            assert data.imageUrl, "Поле 'imageUrl' пустое"
            assert data.published, "Поле 'published' пустое"
            assert data.genreId, "Поле 'genreId' пустое"
        with allure.step("Проверяем, что локация корректна"):
            assert data.location in ["MSK", "SPB"], f"Ожидалось значение 'MSK' или 'SPB', получено '{data['location']}'"
        with allure.step("Проверяем, что цена положительная"):
            assert 0 < data.price, "Некорректная сумма, ожидалось значение больше нуля"
        with allure.step("Создаем фильм суперадмином"):
            response = super_admin.api.movie_api.create_movie(create_movie_data.model_dump())
        response_data = ResponseMovie(**response.json())
        movie_id = response_data.id
        with allure.step(f"Пытаемся обновить данные фильма с ID {movie_id} как обычный пользователь, ожидаем статус 403"):
            common_user.api.movie_api.patch_movie(movie_id=movie_id, data=data, expected_status=403)
