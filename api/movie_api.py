from custom_requester.custom_requester import CustomRequester
from constants import BASE_URL_MOVIES, GET_MOVIES, POST_MOVIE, GET_MOVIE, DELETE_MOVIE

class MovieAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL_MOVIES)
        self.session = session

    def get_movies_for_params(self, params, excepted_status=200):
        return self.send_request(
            method="GET",
            endpoint=GET_MOVIES,
            params=params,
            expected_status=excepted_status
        )

    def create_movie(self, create_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint=POST_MOVIE,
            data=create_data,
            expected_status=expected_status
        )

    def get_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=f"{GET_MOVIE}{movie_id}",
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method="DELETE",
            endpoint=f"{DELETE_MOVIE}{movie_id}",
            expected_status=expected_status
        )
