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
        params_ints_values = (params["pageSize"], params["page"], params["minPrice"], params["maxPrice"], params["genreId"])
        all_int = all(isinstance(value, int) for value in params_ints_values)
        assert all_int, "Значения в полях 'pageSize', 'page', 'minPrice', 'maxPrice', 'genreId' должны быть числами"
        assert all(loc in ["MSK", "SPB"] for loc in params["locations"]), f"Ожидалось значение 'MSK' или 'SPB', получено '{params["locations"]}'"
        assert 0 < params["minPrice"] < params["maxPrice"], "Некорректная сумма, проверьте значения милимальной и максимальной суммы"
        response = api_manager_movies.movie_api.get_movies_for_params(params=params, excepted_status=200)
        response_data = response.json()



    def test_create_movie(self, api_manager_movies, admin_creds):
        create_data = {
            "name": "Название фильма было неоднозначное",
            "imageUrl": "https://imagehzchtoeto.url",
            "price": 150,
            "description": "Описание фильма было многосмысленным",
            "location": "SPB",
            "published": True,
            "genreId": 1
        }
        api_manager_movies.auth_api.authenticate_admin(admin_creds)
        response = api_manager_movies.movie_api.create_movie(create_data)
        response_data = response.json()

    def test_get_movie(self, api_manager_movies):
       response = api_manager_movies.movie_api.get_movie(movie_id=895)
       response_data = response.json()

    def test_delete_movie(self, api_manager_movies, admin_creds):
        api_manager_movies.auth_api.authenticate_admin(admin_creds)
        response = api_manager_movies.movie_api.delete_movie(movie_id="Допишу в некст раз")



