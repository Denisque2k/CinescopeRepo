from conftest import common_user, super_admin


class TestAuthAPI:
    def test_register_user(self, api_manager, test_user):
        """
        Тест на регистрацию пользователя.
        """

        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    def test_register_and_login_user(self, api_manager, registered_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"

    def test_get_logout_user(self, common_user, api_manager):
        """
        Тест на выход из учетной записи.
        """
        common_user.api.auth_api.authenticate(common_user.creds)
        response = common_user.api.user_api.get_user_logout()
        response_data = response.text
        assert response_data == "OK", "Ошибка выхода из учетной записи"

    def test_get_refresh_tokens(self, api_manager, registered_user):
        """
        Тест на обновление токена.
        """
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()
        response_get = api_manager.user_api.get_refresh_tokens(expected_status=200)
        response_get_data = response_get.json()
        assert "accessToken" in response_get_data, "Токен не был получен"
        assert "refreshToken" in response_get_data, "Токен не был получен"
        assert "expiresIn" in response_get_data, "Срок действия токена не был получен"
        assert response_get_data["refreshToken"] != response_data["refreshToken"], "Токен не изменился"
        #Так и не понял, должен ли обновляться accessToken

    def test_super_admin_get_user(self, api_manager, super_admin, creation_user_data):
        """
        Тест на запрос юзера по ИД суперадмином.
        """
        response = super_admin.api.user_api.create_user(creation_user_data).json()
        user_id = response["id"]
        response_get = super_admin.api.user_api.get_user_info(user_id)
        response_data = response_get.json()
        assert response_data, "Пользователя не существует"
        assert response_data["id"] == user_id, "ИД не совпадает"

    def test_admin_get_user(self, api_manager, admin_user, creation_user_data):
        """
        Тест на запрос юзера по ИД админом.
        """
        response = admin_user.api.user_api.create_user(creation_user_data).json()
        user_id = response["id"]
        response_get = admin_user.api.user_api.get_user_info(user_id)
        response_data = response_get.json()
        assert response_data, "Пользователя не существует"
        assert response_data["id"] == user_id, "ИД не совпадает"

    def test_get_user(self, api_manager, common_user):
        """
        Тест на запрос юзера по ИД обычным юзером.
        """
        common_user.api.user_api.get_user_info(common_user.email, expected_status=403)

    def test_super_admin_delete_user(self, api_manager, super_admin, creation_user_data):
        """
        Тест на удаление юзера по ИД суперадмином.
        """
        response = super_admin.api.user_api.create_user(creation_user_data).json()
        user_id = response["id"]
        super_admin.api.user_api.delete_user(user_id=user_id)

    def test_admin_delete_user(self, api_manager, admin_user, creation_user_data):
        """
        Тест на удаление юзера по ИД админом.
        """
        response = admin_user.api.user_api.create_user(creation_user_data).json()
        user_id = response["id"]
        admin_user.api.user_api.delete_user(user_id=user_id)

    def test_delete_user(self, api_manager, common_user):
        """
        Тест на удаление юзера по ИД обычным юзером.
        """
        user_id = common_user.id
        common_user.api.auth_api.authenticate(common_user.creds)
        common_user.api.user_api.delete_user(user_id=user_id)

    def test_super_admin_patch_method(self, api_manager, super_admin, creation_user_data):
        """
        Тест на изменение данных юзера по ИД суперадмином.
        """
        patch_data = {
            "roles": [
                "ADMIN"
                    ],
            "verified": True,
            "banned": False
        }
        allowed_roles = {"USER", "ADMIN", "SUPER_ADMIN"}
        assert patch_data["roles"], "Поле роль пустое"
        assert all(role in allowed_roles for role in patch_data["roles"]), "Есть недопустимые роли"
        response = super_admin.api.user_api.create_user(creation_user_data).json()
        user_id = response["id"]
        response_patch_user = super_admin.api.user_api.patch_user(patch_data, user_id)
        response_data = response_patch_user.json()
        assert response_data["roles"], "Поле роль пустое"
        assert all(role in allowed_roles for role in response_data["roles"]), "Есть недопустимые роли"

    def test_admin_patch_method(self, api_manager, admin_user, creation_user_data):
        """
        Тест на изменение данных юзера по ИД админом.
        """
        patch_data = {
            "roles": [
                "USER"
                    ],
            "verified": True,
            "banned": False
        }
        allowed_roles = {"USER", "ADMIN", "SUPER_ADMIN"}
        assert patch_data["roles"], "Поле роль пустое"
        assert all(role in allowed_roles for role in patch_data["roles"]), "Есть недопустимые роли"
        response = admin_user.api.user_api.create_user(creation_user_data).json()
        user_id = response["id"]
        response_patch_user = admin_user.api.user_api.patch_user(patch_data, user_id)
        response_data = response_patch_user.json()
        assert response_data["roles"], "Поле роль пустое"
        assert all(role in allowed_roles for role in response_data["roles"]), "Есть недопустимые роли"

    def test_user_patch_method(self, api_manager, common_user):
        """
        Тест на изменение данных юзера по ИД обычным юзером.
        """
        patch_data = {
            "roles": [
                "ADMIN"
                    ],
            "verified": True,
            "banned": False
        }
        allowed_roles = {"USER", "ADMIN", "SUPER_ADMIN"}
        assert patch_data.get("roles") in allowed_roles, "Есть недопустимые роли"
        user_id = common_user.id
        common_user.api.auth_api.authenticate(common_user.creds)
        common_user.api.user_api.patch_user(patch_data, user_id=user_id, expected_status=403)


    def test_super_admin_create_user(self, api_manager, super_admin, creation_user_data):
        """
        Тест на создание юзера суперадмином.
        """
        response = super_admin.api.user_api.create_user(creation_user_data).json()
        assert response.get('id') and response['id'] != '', "ID должен быть не пустым"
        assert response.get('email') == creation_user_data['email']
        assert response.get('fullName') == creation_user_data['fullName']
        assert response.get('roles', []) == creation_user_data['roles']
        assert response.get('verified') is True

    def test_admin_create_user(self, api_manager, admin_user, creation_user_data):
        """
        Тест на создание юзера админом.
        """
        response = admin_user.api.user_api.create_user(creation_user_data).json()
        assert response.get('id') and response['id'] != '', "ID должен быть не пустым"
        assert response.get('email') == creation_user_data['email']
        assert response.get('fullName') == creation_user_data['fullName']
        assert response.get('roles', []) == creation_user_data['roles']
        assert response.get('verified') is True

    def test_user_create_user(self, api_manager, common_user, creation_user_data):
        """
        Тест на создание юзера обычным юзером.
        """
        common_user.api.auth_api.authenticate(common_user.creds)
        common_user.api.user_api.create_user(creation_user_data, expected_status=403)


    def test_get_super_admin_users_list(self, api_manager, super_admin):
        """
        Тест на запрос списка юзеров с Парамами суперадмином.
        """
        params = {"roles": "SUPER_ADMIN",
                  "pageSize": 4,
                  "page": 1,
                  "createAt": "asc"}
        allowed_roles = {"USER", "ADMIN", "SUPER_ADMIN"}
        assert params.get("roles") in allowed_roles, "Есть недопустимые роли"
        assert isinstance(params["pageSize"], int), "Параметр PageSize должен быть целым числом"
        assert isinstance(params["page"], int), "Параметр Page должен быть целым числом"
        response = super_admin.api.user_api.get_list_users(params=params)
        response_data = response.json()
        assert isinstance(response_data["pageSize"], int), "Параметр PageSize должен быть целым числом"
        assert isinstance(response_data["page"], int), "Параметр Page должен быть целым числом"

    def test_get_admin_users_list(self, api_manager, admin_user):
        """
        Тест на запрос списка юзеров с Парамами админом.
        """
        params = {"roles": "SUPER_ADMIN",
                  "pageSize": 4,
                  "page": 1,
                  "createAt": "asc"}
        allowed_roles = {"USER", "ADMIN", "SUPER_ADMIN"}
        assert params.get("roles") in allowed_roles, "Есть недопустимые роли"
        assert isinstance(params["pageSize"], int), "Параметр PageSize должен быть целым числом"
        assert isinstance(params["page"], int), "Параметр Page должен быть целым числом"
        response = admin_user.api.user_api.get_list_users(params=params)
        response_data = response.json()
        assert isinstance(response_data["pageSize"], int), "Параметр PageSize должен быть целым числом"
        assert isinstance(response_data["page"], int), "Параметр Page должен быть целым числом"

    def test_get_user_list(self, api_manager, common_user):
        """
        Тест на запрос списка юзеров с Парамами обычным юзером.
        """
        params = {"roles": "SUPER_ADMIN",
                  "pageSize": 4,
                  "page": 1,
                  "createAt": "asc"}
        allowed_roles = {"USER", "ADMIN", "SUPER_ADMIN"}
        assert params.get("roles") in allowed_roles, "Есть недопустимые роли"
        assert isinstance(params["pageSize"], int), "Параметр PageSize должен быть целым числом"
        assert isinstance(params["page"], int), "Параметр Page должен быть целым числом"
        common_user.api.user_api.get_list_users(params=params, expected_status=403)
