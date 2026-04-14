import allure
import pytest
from enums.roles import Roles
from conftest import common_user, super_admin
from models.base_models import RegisterUserResponse, TestUser, LoginUserRequest, LoginUserResponse, \
    ResponseGetRefreshTokens, RequestPatchUser, RequestListUsers, ResponseListUsers


@allure.feature("Authentication & Authorization API")
class TestAuthAPI:

    @allure.story("User Registration")
    @allure.description("Тест проверяет регистрацию нового пользователя. Проверяется соответствие email, наличие ID и установленной роли USER.")
    def test_register_user(self, api_manager, test_user):
        """
        Тест на регистрацию пользователя.
        """
        with allure.step("Отправляем запрос на регистрацию"):
            response = api_manager.auth_api.register_user(test_data=test_user.model_dump())
        response_data = RegisterUserResponse(**response.json())

        with allure.step("Проверяем email в ответе"):
            assert response_data.email == test_user.email, "Email не совпадает"
        with allure.step("Проверяем, что ID пользователя присутствует"):
            assert response_data.id is not None, "ID пользователя отсутствует в ответе"
        with allure.step("Проверяем, что у пользователя установлена роль USER"):
            assert response_data.roles == [Roles.USER], "Роль USER должна быть у пользователя"

    @allure.story("User Registration and Login")
    @allure.description("Тест проверяет успешную регистрацию и последующую авторизацию пользователя. Проверяется наличие accessToken и корректность данных пользователя.")
    def test_register_and_login_user(self, api_manager, registered_user: TestUser):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        login_data = LoginUserRequest(
            email=registered_user.email,
            password=registered_user.password
        )

        with allure.step("Отправляем запрос на авторизацию"):
            response = api_manager.auth_api.login_user(login_data=login_data.model_dump())
        response_data = LoginUserResponse(**response.json())

        with allure.step("Проверяем, что accessToken присутствует в ответе"):
            assert response_data.accessToken is not None, "Токен доступа отсутствует в ответе"
        with allure.step(f"Проверяем email пользователя в ответе"):
            assert response_data.user.email == registered_user.email, f"Email не совпадает, ожидался {registered_user.email}"
        with allure.step(f"Проверяем имя пользователя в ответе"):
            assert response_data.user.fullName == registered_user.fullName, f"Имя не совпадает, ожидалось {registered_user.fullName}"

    @allure.story("User Logout")
    @allure.description("Тест проверяет выход пользователя из учетной записи. Проверяется успешный ответ сервера.")
    @pytest.mark.slow
    def test_get_logout_user(self, common_user, api_manager):
        """
        Тест на выход из учетной записи.
        """
        with allure.step("Отправляем запрос на выход"):
            response = common_user.api.user_api.get_user_logout()
        response_data = response.text

        with allure.step("Проверяем успешное завершение сессии"):
            assert response_data == "OK", "Ошибка выхода из учетной записи"

    @allure.story("Token Refresh")
    @allure.description("Тест проверяет обновление access и refresh токенов. Проверяется, что новые токены отличаются от старых и присутствуют в ответе.")
    def test_get_refresh_tokens(self, api_manager, registered_user: TestUser):
        """
        Тест на обновление токена.
        """
        login_data = LoginUserRequest(
            email=registered_user.email,
            password=registered_user.password
        )

        # Логин для получения начальных токенов
        with allure.step("Авторизуемся для получения начальных токенов"):
            response = api_manager.auth_api.login_user(login_data=login_data.model_dump())
        response_data = LoginUserResponse(**response.json())

        with allure.step("Отправляем запрос на обновление токенов"):
            response_refresh_tokens = api_manager.user_api.get_refresh_tokens(expected_status=200)
        response_get_tokens = ResponseGetRefreshTokens(**response_refresh_tokens.json())

        with allure.step("Проверяем, что новый accessToken получен"):
            assert response_get_tokens.accessToken is not None, "accessToken не был получен"
        with allure.step("Проверяем, что новый refreshToken получен"):
            assert response_get_tokens.refreshToken is not None, "refreshToken не был получен"
        with allure.step("Проверяем, что срок действия токена получен"):
            assert response_get_tokens.expiresIn is not None, "Срок действия токена не был получен"
        #with allure.step("Проверяем, что accessToken обновился"):
            #assert response_get_tokens.accessToken != response_data.accessToken, "accessToken не обновился"
        with allure.step("Проверяем, что refreshToken обновился"):
            assert response_get_tokens.refreshToken != response_data.refreshToken, "refreshToken не обновился"

    @allure.story("Unauthorized Token Refresh")
    @allure.description("Тест проверяет, что попытка обновить токены без активной сессии приводит к ошибке 401.")
    def test_unauthorized_refresh_tokens(self, api_manager):
        with allure.step("Выходим из аккаунта"):
            api_manager.user_api.get_user_logout(expected_status=200)
        with allure.step("Пытаемся обновить токены без авторизации"):
            api_manager.user_api.get_refresh_tokens(expected_status=401)

    @allure.story("Get User Info by ID")
    @allure.description("Тест проверяет, что суперадмин может получить информацию о пользователе по его ID. Проверяется соответствие ID.")
    def test_super_admin_get_user(self, api_manager, super_admin, creation_user_data: TestUser):
        """
        Тест на запрос юзера по ИД суперадмином.
        """
        with allure.step("Создаем нового пользователя"):
            response = super_admin.api.user_api.create_user(creation_user_data.model_dump())
        response_data = RegisterUserResponse(**response.json())
        user_id = response_data.id

        with allure.step(f"Запрашиваем информацию о пользователе с ID {user_id} как суперадмин"):
            response_get_info = super_admin.api.user_api.get_user_info(user_id)
        response_data_user = RegisterUserResponse(**response_get_info.json())

        with allure.step("Проверяем, что пользователь существует"):
            assert response_data, "Пользователя не существует"
        with allure.step("Проверяем, что ID в ответе совпадает с созданным"):
            assert response_data_user.id == user_id, "ИД не совпадает"

    @allure.story("Get User Info by ID")
    @allure.description("Тест проверяет, что администратор может получить информацию о пользователе по его ID. Проверяется соответствие ID.")
    def test_admin_get_user(self, api_manager, admin_user_with_creds, creation_user_data: TestUser):
        """
        Тест на запрос юзера по ИД админом.
        """
        with allure.step("Создаем нового пользователя"):
            response = admin_user_with_creds.api.user_api.create_user(creation_user_data.model_dump())
        response_data = RegisterUserResponse(**response.json())
        user_id = response_data.id

        with allure.step(f"Запрашиваем информацию о пользователе с ID {user_id} как админ"):
            response_get_info = admin_user_with_creds.api.user_api.get_user_info(user_id)
        response_data_user = RegisterUserResponse(**response_get_info.json())

        with allure.step("Проверяем, что пользователь существует"):
            assert response_data, "Пользователя не существует"
        with allure.step("Проверяем, что ID в ответе совпадает с созданным"):
            assert response_data_user.id == user_id, "ИД не совпадает"

    @allure.story("Get User Info by ID")
    @allure.description("Тест проверяет, что обычный пользователь не может получить информацию о другом пользователе по ID. Ожидается ошибка 403.")
    def test_get_user(self, api_manager, common_user):
        """
        Тест на запрос юзера по ИД обычным юзером.
        """
        with allure.step("Пытаемся запросить информацию о себе как обычный пользователь (должно быть запрещено)"):
            common_user.api.user_api.get_user_info(common_user.email, expected_status=403)

    @allure.story("Delete User by ID")
    @allure.description("Тест проверяет, что суперадмин может удалить пользователя по ID. Также проверяется, что повторное удаление невозможно (ошибка 404).")
    def test_super_admin_delete_user(self, api_manager, super_admin, creation_user_data: TestUser):
        """
        Тест на удаление юзера по ИД суперадмином.
        """
        with allure.step("Создаем нового пользователя"):
            response = super_admin.api.user_api.create_user(creation_user_data.model_dump())
        response_data = RegisterUserResponse(**response.json())
        user_id = response_data.id

        with allure.step(f"Удаляем пользователя с ID {user_id} как суперадмин"):
            super_admin.api.user_api.delete_user(user_id=user_id)
        with allure.step("Проверяем, что повторное удаление вызывает ошибку 404"):
            super_admin.api.user_api.delete_user(user_id=user_id, expected_status=404)

    @allure.story("Delete User by ID")
    @allure.description("Тест проверяет, что администратор НЕ может удалить пользователя по ID. Ожидается ошибка 403.")
    def test_admin_delete_user(self, api_manager, admin_user_with_creds, creation_user_data: TestUser):
        """
        Тест на удаление юзера по ИД админом.
        """
        with allure.step("Создаем нового пользователя"):
            response = admin_user_with_creds.api.user_api.create_user(creation_user_data.model_dump())
        response_data = RegisterUserResponse(**response.json())
        user_id = response_data.id

        with allure.step("Пытаемся удалить пользователя как админ (должно быть запрещено)"):
            admin_user_with_creds.api.user_api.delete_user(user_id=user_id, expected_status=403)

    @allure.story("Delete User by ID")
    @allure.description("Тест проверяет, что обычный пользователь может удалить свой собственный аккаунт. Повторная попытка приводит к ошибке 401.")
    @pytest.mark.slow
    def test_delete_user(self, api_manager, common_user):
        """
        Тест на удаление юзера по ИД обычным юзером.
        """
        user_id = common_user.id

        with allure.step("Аутентифицируем пользователя"):
            common_user.api.auth_api.authenticate(common_user.creds)
        with allure.step(f"Удаляем собственный аккаунт"):
            common_user.api.user_api.delete_user(user_id=user_id)
        with allure.step("Проверяем, что повторное удаление вызывает ошибку 401"):
            common_user.api.user_api.delete_user(user_id=user_id, expected_status=401)

    @allure.story("Update User Data by ID")
    @allure.description("Тест проверяет, что суперадмин может обновить данные пользователя (роль, верификация, бан). Проверяется успешность обновления.")
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

        with allure.step("Проверяем валидность patch-данных"):
            assert patch_data.roles, f"Поле роль пустое, ожидалось {allowed_roles}"
            assert all(role in allowed_roles for role in patch_data.roles), "Есть недопустимые роли"

        with allure.step("Создаем нового пользователя"):
            response = super_admin.api.user_api.create_user(creation_user_data.model_dump())
        response_data = RegisterUserResponse(**response.json())
        user_id = response_data.id

        with allure.step(f"Обновляем данные пользователя с ID {user_id} как суперадмин"):
            response_patch_user = super_admin.api.user_api.patch_user(patch_data.model_dump(), user_id)
        response_data_after_patch = RegisterUserResponse(**response_patch_user.json())

        with allure.step("Проверяем, что роль обновилась успешно"):
            assert response_data_after_patch.roles, "Поле роль пустое"
            assert all(role in allowed_roles for role in response_data_after_patch.roles), "Есть недопустимые роли"

    @allure.story("Update User Data by ID")
    @allure.description("Тест проверяет, что администратор НЕ может обновить данные пользователя. Ожидается ошибка 403.")
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

        with allure.step("Проверяем валидность patch-данных"):
            assert patch_data.roles, f"Поле роль пустое, ожидалось {allowed_roles}"
            assert all(role in allowed_roles for role in patch_data.roles), "Есть недопустимые роли"

        with allure.step("Создаем нового пользователя"):
            response = admin_user_with_creds.api.user_api.create_user(creation_user_data.model_dump())
        response_data = RegisterUserResponse(**response.json())
        user_id = response_data.id

        with allure.step("Пытаемся обновить данные пользователя как админ (должно быть запрещено)"):
            admin_user_with_creds.api.user_api.patch_user(patch_data.model_dump(), user_id, expected_status=403)

    @allure.story("Update User Data by ID")
    @allure.description("Тест проверяет, что обычный пользователь НЕ может обновить чужие данные. Ожидается ошибка 403.")
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

        with allure.step("Проверяем валидность patch-данных"):
            assert all(role in allowed_roles for role in patch_data.roles), "Есть недопустимые роли"

        user_id = common_user.id

        with allure.step("Пытаемся обновить свои данные как обычный пользователь (должно быть запрещено)"):
            common_user.api.user_api.patch_user(patch_data, user_id=user_id, expected_status=403)

    @allure.story("Create User")
    @allure.description("Тест проверяет, что суперадмин может создать нового пользователя. Проверяются все поля ответа.")
    def test_super_admin_create_user(self, api_manager, super_admin, creation_user_data: TestUser):
        """
        Тест на создание юзера суперадмином.
        """
        with allure.step("Отправляем запрос на создание пользователя как суперадмин"):
            response = super_admin.api.user_api.create_user(creation_user_data.model_dump())
        response_data = RegisterUserResponse(**response.json())

        with allure.step("Проверяем, что ID не пустой"):
            assert response_data != '', "ID должен быть не пустым"
        with allure.step(f"Проверяем email: {creation_user_data.email}"):
            assert response_data.email == creation_user_data.email
        with allure.step(f"Проверяем имя: {creation_user_data.fullName}"):
            assert response_data.fullName == creation_user_data.fullName
        with allure.step(f"Проверяем роли: {creation_user_data.roles}"):
            assert response_data.roles == creation_user_data.roles
        with allure.step("Проверяем статус верификации"):
            assert response_data.verified is True

    @allure.story("Create User")
    @allure.description("Тест проверяет, что администратор может создать нового пользователя. Проверяются все поля ответа.")
    def test_admin_create_user(self, api_manager, admin_user_with_creds, creation_user_data: TestUser):
        """
        Тест на создание юзера админом.
        """
        with allure.step("Отправляем запрос на создание пользователя как админ"):
            response = admin_user_with_creds.api.user_api.create_user(creation_user_data.model_dump())
        response_data = RegisterUserResponse(**response.json())

        with allure.step("Проверяем, что ID не пустой"):
            assert response_data != '', "ID должен быть не пустым"
        with allure.step(f"Проверяем email: {creation_user_data.email}"):
            assert response_data.email == creation_user_data.email
        with allure.step(f"Проверяем имя: {creation_user_data.fullName}"):
            assert response_data.fullName == creation_user_data.fullName
        with allure.step(f"Проверяем роли: {creation_user_data.roles}"):
            assert response_data.roles == creation_user_data.roles
        with allure.step("Проверяем статус верификации"):
            assert response_data.verified is True

    @allure.story("Create User")
    @allure.description("Тест проверяет, что обычный пользователь НЕ может создать нового пользователя. Ожидается ошибка 403.")
    def test_user_create_user(self, api_manager, common_user, creation_user_data: TestUser):
        """
        Тест на создание юзера обычным юзером.
        """
        with allure.step("Пытаемся создать пользователя как обычный пользователь (должно быть запрещено)"):
            # common_user.api.auth_api.authenticate(common_user.creds)
            common_user.api.user_api.create_user(creation_user_data.model_dump(), expected_status=403)

    @allure.story("Get Users List")
    @allure.description("Тест проверяет, что суперадмин может получить список пользователей с фильтрами (роль, страница, размер, сортировка).")
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
        with allure.step("Запрашиваем список пользователей как суперадмин"):
            response = super_admin.api.user_api.get_list_users(params)
        ResponseListUsers(**response.json())

    @allure.story("Get Users List")
    @allure.description("Тест проверяет, что администратор может получить список пользователей с фильтрами (роль, страница, размер, сортировка).")
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
        with allure.step("Запрашиваем список пользователей как админ"):
            response = admin_user_with_creds.api.user_api.get_list_users(params)
        ResponseListUsers(**response.json())

    @allure.story("Get Users List")
    @allure.description("Тест проверяет, что обычный пользователь НЕ может получить список пользователей. Ожидается ошибка 403.")
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
        with allure.step("Пытаемся запросить список пользователей как обычный пользователь (должно быть запрещено)"):
            common_user.api.user_api.get_list_users(params, expected_status=403)

