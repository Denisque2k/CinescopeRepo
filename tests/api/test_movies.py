import pytest
import allure
from conftest import super_admin
from models.base_models import ResponseMovie, RequestMovie, RequestGetMovie



class TestMovieAPI:
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
        assert params["pageSize"] in params.values(), "Поле pageSize пустое"
        assert params["page"] in params.values(), "Поле 'page' пустое"
        assert params["minPrice"] in params.values(), "Поле 'minPrice' пустое"
        assert params["maxPrice"] in params.values(), "Поле 'maxPrice' пустое"
        assert params["locations"] in params.values(), "Поле 'locations' пустое"
        assert params["published"] in params.values(), "Поле published пустое"
        assert params["genreId"] in params.values(), "Поле 'genreId' пустое"
        params_ints_values = (params["pageSize"], params["page"], params["minPrice"], params["maxPrice"], params["genreId"])
        all_int = all(isinstance(value, int) for value in params_ints_values)
        assert all_int, "Значения в полях 'pageSize', 'page', 'minPrice', 'maxPrice', 'genreId' должны быть числами"
        assert all(loc in ["MSK", "SPB"] for loc in params["locations"]), f"Ожидалось значение 'MSK' или 'SPB', получено '{params["locations"]}'"
        assert 0 < params["minPrice"] < params["maxPrice"], "Некорректная сумма, проверьте значения милимальной и максимальной суммы"
        response = api_manager.movie_api.get_movies_for_params(params=params, excepted_status=200)
        response_data = response.json()



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
        assert data.name, "Поле name пустое"
        assert data.description, "Поле 'description' пустое"
        assert data.price, "Поле 'price' пустое"
        assert data.imageUrl, "Поле 'imageUrl' пустое"
        assert data.published, "Поле 'published' пустое"
        assert data.genreId, "Поле 'genreId' пустое"
        assert 0 < data.price, "Некорректная сумма, ожидалось значение больше нуля"
        response = super_admin.api.movie_api.create_movie(create_movie_data.model_dump())
        response_data = ResponseMovie(**response.json())
        assert api_manager.movie_api.get_movie(movie_id=response_data.id), "Фильм не найден"
        assert response_data.name == data.name, f"Название фильма не совпадает, ожидалось {data.name}"
        assert response_data.price == data.price, f"Цена фильма не совпадает, ожидалось {data.price}"


    def test_get_movie(self, api_manager, super_admin, create_movie_data):
       response = super_admin.api.movie_api.create_movie(create_movie_data.model_dump())
       response_data = ResponseMovie(**response.json())
       api_manager.movie_api.get_movie(movie_id=response_data.id)


    users_fixtures = [
        pytest.param("admin_user_with_creds", 403, "Получает запрет", id="admin_user_with_creds"),
        pytest.param("common_user", 403, "Получает запрет", id="common_user"),
    ]
    @pytest.mark.parametrize("fixture_name, expected_status, description", users_fixtures)
    def test_delete_movie(self, request, fixture_name, expected_status, description, api_manager, super_admin, admin_user_with_creds, common_user, create_movie_data):
        name_fixture = request.getfixturevalue(fixture_name)

        create_movie_response = super_admin.api.movie_api.create_movie(data=create_movie_data.model_dump())
        create_movie_response_data = ResponseMovie(**create_movie_response.json())
        movie_id = create_movie_response_data.id

        delete_response = name_fixture.api.movie_api.delete_movie(movie_id=movie_id, expected_status=expected_status)
        assert delete_response.status_code == expected_status, f"{description}"
        if expected_status == 200:
            assert name_fixture.api.movie_api.get_movie(movie_id=movie_id, expected_status=404).status_code == 404

    @pytest.mark.slow
    def test_super_admin_delete_movie(self, api_manager, super_admin, create_movie_data):
        response = super_admin.api.movie_api.create_movie(data=create_movie_data.model_dump())
        response_data = ResponseMovie(**response.json())
        movie_id = response_data.id
        assert movie_id, "Проверьте поле ИД фильма"
        super_admin.api.movie_api.delete_movie(movie_id=movie_id)
        api_manager.movie_api.get_movie(movie_id=movie_id, expected_status=404)

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
        assert data.name, "Поле name пустое"
        assert data.description, "Поле 'description' пустое"
        assert data.price, "Поле 'price' пустое"
        assert data.imageUrl, "Поле 'imageUrl' пустое"
        assert data.published, "Поле 'published' пустое"
        assert data.genreId, "Поле 'genreId' пустое"
        assert data.location in ["MSK", "SPB"], f"Ожидалось значение 'MSK' или 'SPB', получено '{data["location"]}'"
        assert 0 < data.price, "Некорректная сумма, ожидалось значение больше нуля"
        response = super_admin.api.movie_api.create_movie(create_movie_data.model_dump())
        response_data = ResponseMovie(**response.json())
        movie_id = response_data.id
        super_admin.api.movie_api.patch_movie(movie_id=movie_id, data=data)
        assert response_data.name == data.name, f"Название фильма не совпадает, ожидалось {data.name}"
        assert response_data.price == data.price, f"Цена фильма не совпадает, ожидалось {data.price}"

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
        assert data.name, "Поле name пустое"
        assert data.description, "Поле 'description' пустое"
        assert data.price, "Поле 'price' пустое"
        assert data.imageUrl, "Поле 'imageUrl' пустое"
        assert data.published, "Поле 'published' пустое"
        assert data.genreId, "Поле 'genreId' пустое"
        assert data.location in ["MSK", "SPB"], f"Ожидалось значение 'MSK' или 'SPB', получено '{data["location"]}'"
        assert 0 < data.price, "Некорректная сумма, ожидалось значение больше нуля"
        response = super_admin.api.movie_api.create_movie(create_movie_data.model_dump())
        response_data = ResponseMovie(**response.json())
        movie_id = response_data.id
        common_user.api.movie_api.patch_movie(movie_id=movie_id, data=data, expected_status=403)







