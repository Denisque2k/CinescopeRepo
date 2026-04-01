from custom_requester.custom_requester import CustomRequester
from constants import BASE_URL, GET_USER_INFO, DELETE_USER, GET_LOGOUT_ENDPOINT, GET_REFRESH_TOKENS, PATCH_USER, CREATE_USER, GET_USER_LIST

class UserAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL)
        self.session = session

    def get_user_info(self, user_locator):
        return self.send_request("GET",f"user/{user_locator}")

    def get_user_logout(self, expected_status=200):
        """
        Выход из учетной записи.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=GET_LOGOUT_ENDPOINT,
            expected_status=expected_status
        )

    def get_refresh_tokens(self, expected_status=200):
        """
        Обновление refresh-token.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=GET_REFRESH_TOKENS,
            expected_status=expected_status
        )

    def delete_user(self, user_id, expected_status=204):
        """
        Удаление пользователя.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"{DELETE_USER}{user_id}",
            expected_status=expected_status
        )

    def patch_user(self, patch_data, user_id, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=f"{PATCH_USER}{user_id}",
            data=patch_data,
            expected_status=expected_status
        )

    def create_user(self, user_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint=CREATE_USER,
            data=user_data,
            expected_status=expected_status
        )

    def get_list_users(self, params, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=GET_USER_LIST,
            params=params,
            expected_status=expected_status
        )