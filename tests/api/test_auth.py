import pytest
from enums.roles import Roles
from conftest import common_user, super_admin
from models.base_models import RegisterUserResponse, TestUser, LoginUserRequest, LoginUserResponse, \
    ResponseGetRefreshTokens, RequestPatchUser, RequestListUsers, ResponseListUsers


class TestAuthAPI:
    def test_register_user(self, api_manager, test_user):
        """
        Тест на регистрацию пользователя.
        """

        response = api_manager.auth_api.register_user(test_data=test_user.model_dump())
        response_data = RegisterUserResponse(**response.json())
        assert response_data.email == test_user.email, "Email не совпадает"
        assert response_data.id is not None, "ID пользователя отсутствует в ответе"
        assert response_data.roles == [Roles.USER], "Роль USER должна быть у пользователя"

    def test_register_and_login_user(self, api_manager, registered_user: TestUser):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        login_data = LoginUserRequest(
            email=registered_user.email,
            password=registered_user.password
        )
        response = api_manager.auth_api.login_user(login_data=login_data.model_dump())
        response_data = LoginUserResponse(**response.json())
        assert response_data.accessToken is not None, "Токен доступа отсутствует в ответе"
        assert response_data.user.email == registered_user.email, f"Email не совпадает, ожидался {registered_user.email}"
        assert response_data.user.fullName == registered_user.fullName, f"Имя не совпадает, ожидалось {registered_user.fullName}"

    @pytest.mark.slow
    def test_get_logout_user(self, common_user, api_manager):
        """
        Тест на выход из учетной записи.
        """
        response = common_user.api.user_api.get_user_logout()
        response_data = response.text
        assert response_data == "OK", "Ошибка выхода из учетной записи"

    def test_get_refresh_tokens(self, api_manager, registered_user: TestUser):
        """
        Тест на обновление токена.
        """
        login_data = LoginUserRequest(
            email=registered_user.email,
            password=registered_user.password
        )
        response = api_manager.auth_api.login_user(login_data=login_data.model_dump())
        response_data = LoginUserResponse(**response.json())
        response_refresh_tokens = api_manager.user_api.get_refresh_tokens(expected_status=200)
        response_get_tokens = ResponseGetRefreshTokens(**response_refresh_tokens.json())
        assert response_get_tokens.accessToken is not None, "accessToken не был получен"
        assert response_get_tokens.refreshToken is not None, "refreshToken не был получен"
        assert response_get_tokens.expiresIn is not None, "Срок действия токена не был получен"
        assert response_get_tokens.accessToken != response_data.accessToken, "accessToken не обновился"
        assert response_get_tokens.refreshToken != response_data.refreshToken, "refreshToken не обновился"

    def test_unauthorized_refresh_tokens(self, api_manager):
        api_manager.user_api.get_refresh_tokens(expected_status=401)

    def test_super_admin_get_user(self, api_manager, super_admin, creation_user_data: TestUser):
        """
        Тест на запрос юзера по ИД суперадмином.
        """
        response = super_admin.api.user_api.create_user(creation_user_data.model_dump())
        response_data = RegisterUserResponse(**response.json())
        user_id = response_data.id
        response_get_info = super_admin.api.user_api.get_user_info(user_id)
        response_data_user = RegisterUserResponse(**response_get_info.json())
        assert response_data, "Пользователя не существует"
        assert response_data_user.id == user_id, "ИД не совпадает"

    def test_admin_get_user(self, api_manager, admin_user_with_creds, creation_user_data):
        """
        Тест на запрос юзера по ИД админом.
        """
        response = admin_user_with_creds.api.user_api.create_user(creation_user_data.model_dump())
        response_data = RegisterUserResponse(**response.json())
        user_id = response_data.id
        response_get_info = admin_user_with_creds.api.user_api.get_user_info(user_id)
        response_data_user = RegisterUserResponse(**response_get_info.json())
        assert response_data, "Пользователя не существует"
        assert response_data_user.id == user_id, "ИД не совпадает"

    def test_get_user(self, api_manager, common_user):
        """
        Тест на запрос юзера по ИД обычным юзером.
        """
        common_user.api.user_api.get_user_info(common_user.email, expected_status=403)

    def test_super_admin_delete_user(self, api_manager, super_admin, creation_user_data: TestUser):
        """
        Тест на удаление юзера по ИД суперадмином.
        """
        response = super_admin.api.user_api.create_user(creation_user_data.model_dump())
        response_data = RegisterUserResponse(**response.json())
        user_id = response_data.id
        super_admin.api.user_api.delete_user(user_id=user_id)
        super_admin.api.user_api.delete_user(user_id=user_id, expected_status=404)


    def test_admin_delete_user(self, api_manager, admin_user_with_creds, creation_user_data: TestUser):
        """
        Тест на удаление юзера по ИД админом.
        """
        response = admin_user_with_creds.api.user_api.create_user(creation_user_data.model_dump())
        response_data = RegisterUserResponse(**response.json())
        user_id = response_data.id
        admin_user_with_creds.api.user_api.delete_user(user_id=user_id, expected_status=403)

    @pytest.mark.slow
    def test_delete_user(self, api_manager, common_user):
        """
        Тест на удаление юзера по ИД обычным юзером.
        """
        user_id = common_user.id
        common_user.api.auth_api.authenticate(common_user.creds)
        common_user.api.user_api.delete_user(user_id=user_id)
        common_user.api.user_api.delete_user(user_id=user_id, expected_status=401)


    def test_super_admin_patch_method(self, api_manager, super_admin, creation_user_data: TestUser):
        """
        Тест на изменение данных юзера по ИД суперадмином.
        """
        patch_data = RequestPatchUser(
            roles=[Roles.ADMIN],
            verified=True,
            banned=False
        )
        allowed_roles = {"USER", "ADMIN", "SUPER_ADMIN"}
        assert patch_data.roles, f"Поле роль пустое, ожидалось {allowed_roles}"
        assert all(role in allowed_roles for role in patch_data.roles), "Есть недопустимые роли"
        response = super_admin.api.user_api.create_user(creation_user_data.model_dump())
        response_data = RegisterUserResponse(**response.json())
        user_id = response_data.id
        response_patch_user = super_admin.api.user_api.patch_user(patch_data.model_dump(), user_id)
        response_data_after_patch = RegisterUserResponse(**response_patch_user.json())
        assert response_data_after_patch.roles, "Поле роль пустое"
        assert all(role in allowed_roles for role in response_data_after_patch.roles), "Есть недопустимые роли"

    def test_admin_patch_method(self, api_manager, admin_user_with_creds, creation_user_data: TestUser):
        """
        Тест на изменение данных юзера по ИД админом.
        """
        patch_data = RequestPatchUser(
            roles=[Roles.ADMIN],
            verified=True,
            banned=False
        )
        allowed_roles = {"USER", "ADMIN", "SUPER_ADMIN"}
        assert patch_data.roles, f"Поле роль пустое, ожидалось {allowed_roles}"
        assert all(role in allowed_roles for role in patch_data.roles), "Есть недопустимые роли"
        response = admin_user_with_creds.api.user_api.create_user(creation_user_data.model_dump())
        response_data = RegisterUserResponse(**response.json())
        user_id = response_data.id
        admin_user_with_creds.api.user_api.patch_user(patch_data.model_dump(), user_id, expected_status=403)

    def test_user_patch_method(self, api_manager, common_user):
        """
        Тест на изменение данных юзера по ИД обычным юзером.
        """
        patch_data = RequestPatchUser(
            roles=[Roles.ADMIN],
            verified=True,
            banned=False
        )
        allowed_roles = {"USER", "ADMIN", "SUPER_ADMIN"}
        assert all(role in allowed_roles for role in patch_data.roles), "Есть недопустимые роли"
        user_id = common_user.id
        common_user.api.user_api.patch_user(patch_data, user_id=user_id, expected_status=403)


    def test_super_admin_create_user(self, api_manager, super_admin, creation_user_data: TestUser):
        """
        Тест на создание юзера суперадмином.
        """
        response = super_admin.api.user_api.create_user(creation_user_data.model_dump())
        response_data = RegisterUserResponse(**response.json())
        assert response_data != '', "ID должен быть не пустым"
        assert response_data.email == creation_user_data.email
        assert response_data.fullName == creation_user_data.fullName
        assert response_data.roles == creation_user_data.roles
        assert response_data.verified is True

    def test_admin_create_user(self, api_manager, admin_user_with_creds, creation_user_data: TestUser):
        """
        Тест на создание юзера админом.
        """
        response = admin_user_with_creds.api.user_api.create_user(creation_user_data.model_dump())
        response_data = RegisterUserResponse(**response.json())
        assert response_data != '', "ID должен быть не пустым"
        assert response_data.email == creation_user_data.email
        assert response_data.fullName == creation_user_data.fullName
        assert response_data.roles == creation_user_data.roles
        assert response_data.verified is True

    def test_user_create_user(self, api_manager, common_user, creation_user_data: TestUser):
        """
        Тест на создание юзера обычным юзером.
        """
        #common_user.api.auth_api.authenticate(common_user.creds)
        common_user.api.user_api.create_user(creation_user_data.model_dump(), expected_status=403)


    def test_get_super_admin_users_list(self, api_manager, super_admin):
        """
        Тест на запрос списка юзеров с Парамами суперадмином.
        """
        params = RequestListUsers(
            roles=[Roles.ADMIN],
            pageSize=4,
            page=2,
            createAt="asc"
        )
        response = super_admin.api.user_api.get_list_users(params)
        ResponseListUsers(**response.json())

    def test_get_admin_users_list(self, api_manager, admin_user_with_creds):
        """
        Тест на запрос списка юзеров с Парамами админом.
        """
        params = RequestListUsers(
            roles=[Roles.ADMIN],
            pageSize=4,
            page=2,
            createAt="asc"
        )
        response = admin_user_with_creds.api.user_api.get_list_users(params)
        ResponseListUsers(**response.json())

    @pytest.mark.slow
    def test_get_user_list(self, api_manager, common_user):
        """
        Тест на запрос списка юзеров с Парамами обычным юзером.
        """
        params = RequestListUsers(
            roles=[Roles.ADMIN],
            pageSize=4,
            page=2,
            createAt="asc"
        )
        common_user.api.user_api.get_list_users(params, expected_status=403)
