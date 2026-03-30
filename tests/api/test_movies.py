import constants
from api.api_manager import ApiManager
from api.api_manager_movies import ApiManagerMovies

class TestMovieAPI:
    def test_get_movies(self, api_manager_movies):
        params = {
        "pageSize": 1,
        "page": 1,
        "minPrice": 1,
        "maxPrice": 1000,
        "locations": ["MSK"],
        "published": True,
        "genreId": 1,
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
        response = api_manager_movies.movie_api.get_movies_for_params(params=params, excepted_status=200)
        response_data = response.json()



    def test_create_movie(self, api_manager_movies, admin_creds, create_movie_data):
        data = create_movie_data
        assert data["name"] in data.values(), "Поле name пустое"
        assert data["description"] in data.values(), "Поле 'description' пустое"
        assert data["price"] in data.values(), "Поле 'price' пустое"
        assert data["imageUrl"] in data.values(), "Поле 'imageUrl' пустое"
        assert data["published"] in data.values(), "Поле 'published' пустое"
        assert data["genreId"] in data.values(), "Поле 'genreId' пустое"
        data_ints_values = (data["price"], data["genreId"])
        all_int = all(isinstance(value, int) for value in data_ints_values)
        assert all_int, "Значения в полях 'price', 'genreId' должны быть целыми числами"
        assert data["location"] in ["MSK", "SPB"], f"Ожидалось значение 'MSK' или 'SPB', получено '{data["location"]}'"
        assert 0 < data["price"], "Некорректная сумма, ожидалось значение больше нуля"
        api_manager_movies.auth_api.authenticate_admin(admin_creds)
        response = api_manager_movies.movie_api.create_movie(data)
        response_data = response.json()
        common_keys = data.keys() & response_data.keys()
        assert all(data[k] == response_data[k] for k in common_keys)

    def test_get_movie(self, api_manager_movies):
       response = api_manager_movies.movie_api.get_movie(movie_id=26260)
       response_data = response.json()

    def test_delete_movie(self, api_manager_movies, admin_creds):
        api_manager_movies.auth_api.authenticate_admin(admin_creds)
        movie_id = "True"
        assert movie_id, "Проверьте поле ИД фильма"
        assert isinstance(movie_id, int), "Укажите корректное значение ИД фильма"
        response = api_manager_movies.movie_api.delete_movie(movie_id=movie_id)

    def test_patch_movie(self, api_manager_movies, admin_creds):
        data = {
            "name": "Here movie name",
            "description": "Here movie description",
            "price": 350,
            "location": "MSK",
            "imageUrl": "https://image888.url",
            "published": True,
            "genreId": 1
        }
        assert data["name"] in data.values(), "Поле name пустое"
        assert data["description"] in data.values(), "Поле 'description' пустое"
        assert data["price"] in data.values(), "Поле 'price' пустое"
        assert data["imageUrl"] in data.values(), "Поле 'imageUrl' пустое"
        assert data["published"] in data.values(), "Поле 'published' пустое"
        assert data["genreId"] in data.values(), "Поле 'genreId' пустое"
        data_ints_values = (data["price"], data["genreId"])
        all_int = all(isinstance(value, int) for value in data_ints_values)
        assert all_int, "Значения в полях 'price', 'genreId' должны быть целыми числами"
        assert data["location"] in ["MSK", "SPB"], f"Ожидалось значение 'MSK' или 'SPB', получено '{data["location"]}'"
        assert 0 < data["price"], "Некорректная сумма, ожидалось значение больше нуля"
        api_manager_movies.auth_api.authenticate_admin(admin_creds)
        response = api_manager_movies.movie_api.patch_movie(movie_id=26260, data=data)
        response_data = response.json()

    def test_get_genres(self, api_manager_movies):
        response = api_manager_movies.movie_api.get_genres_list()
        response_data = response.json()








