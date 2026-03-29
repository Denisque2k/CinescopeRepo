from conftest import test_user

# В некоторых тестах я пока что ручками накидывал данные, прошу не бить палками((( для парочки проверок возможно понадобится сделать пару кредов.
# Негативные сценарии также в некоторых тестах делал ручками.

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

    def test_get_logout_user(self, api_manager, user_creds):
        """
        Тест на выход из учетной записи.
        """
        api_manager.auth_api.authenticate_user(user_creds)
        response = api_manager.user_api.get_user_logout(expected_status=200)
        response_data = response.text
        assert response_data == "OK", "Ошибка выхода из учетной записи"

    def test_get_refresh_tokens(self, api_manager, registered_user):
        """
        Тест на обновление токена.
        """
        login_data = {
            "email": "testovyi@email.com",
            "password": "12345678AaA"
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

    def test_admin_get_user(self, api_manager, admin_creds):
        """
        Тест на запрос юзера по ИД админом.
        """
        api_manager.auth_api.authenticate_admin(admin_creds)
        user_id = "55fad028-ab2c-4180-aedb-674d7fa0b465"
        response_get = api_manager.user_api.get_user_info(user_id, expected_status=200)
        response_data = response_get.json()
        assert response_data, "Пользователя не существует"
        assert response_data["id"] == user_id, "ИД не совпадает"

    def test_get_user(self, api_manager, user_creds):
        """
        Тест на запрос юзера по ИД обычным юзером.
        """
        api_manager.auth_api.authenticate_user(user_creds)
        user_id = "55fad028-ab2c-4180-aedb-674d7fa0b465"
        response = api_manager.user_api.get_user_info(user_id, expected_status=200)
        response_data = response.json()

    def test_delete_user(self, api_manager, user_creds):
        """
        Тест на удаление юзера по ИД обычным юзером.
        """
        api_manager.auth_api.authenticate_user(user_creds)
        user_id = "8ef023ac-ab74-4e24-8a99-172c65163d07"
        api_manager.user_api.delete_user(user_id, expected_status=200)
        #Чел может сам себя удалить, просто ответ АПИшки прилетает пустой
        #Пока что данные подкдывал ручками
    def test_admin_delete_user(self, api_manager, admin_creds):
        """
        Тест на удаление юзера по ИД админом.
        """
        api_manager.auth_api.authenticate_admin(admin_creds)
        user_id = "8ef023ac-ab74-4e24-8a99-172c65163d07"
        api_manager.user_api.delete_user(user_id, expected_status=200)
        #И здесь чел удалится)

    def test_admin_patch_method(self, api_manager, admin_creds):
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
        allowed_roles = ["USER", "ADMIN", "SUPER_ADMIN"]
        user_id = "55fad028-ab2c-4180-aedb-674d7fa0b465"
        api_manager.auth_api.authenticate_admin(admin_creds)
        response = api_manager.user_api.patch_user(patch_data, user_id, expected_status=200)
        response_data = response.json()
        assert response_data["roles"], "Поле роль пустое"
        assert all(role in allowed_roles for role in patch_data["roles"]), "Есть недопустимые роли"


    def test_user_patch_method(self, api_manager, user_creds):
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
        allowed_roles = ["USER", "ADMIN", "SUPER_ADMIN"]
        user_id = "55fad028-ab2c-4180-aedb-674d7fa0b465"
        api_manager.auth_api.authenticate_user(user_creds)
        response = api_manager.user_api.patch_user(patch_data, user_id, expected_status=200)
        response_data = response.json()
        assert response_data["roles"], "Поле роль пустое"
        assert all(role in allowed_roles for role in patch_data["roles"]), "Есть недопустимые роли"


    def test_admin_create_user(self, api_manager, admin_creds, test_user):
        """
        Тест на создание юзера админом.
        """
        create_user = {
        "fullName": test_user["fullName"],
        "email": test_user["email"],
        "password": test_user["password"],
        "verified": False,
        "banned": False
    }
        api_manager.auth_api.authenticate_admin(admin_creds)
        response = api_manager.user_api.create_admin_user_api(create_user)
        response_data = response.json()
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    def test_user_create_user(self, api_manager, user_creds, create_user):
        """
        Тест на создание юзера обычным юзером.
        """
        api_manager.auth_api.authenticate_user(user_creds)
        response = api_manager.user_api.create_admin_user_api(create_user)
        response_data = response.json()
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"


    def test_get_admin_users_list(self, api_manager, admin_creds):
        """
        Тест на запрос списка юзеров с Парамами админом.
        """
        params = {"roles": "SUPER_ADMIN",
                  "pageSize": 4,
                  "page": 1,
                  "createAt": "asc"}
        api_manager.auth_api.authenticate_admin(admin_creds)
        response = api_manager.user_api.get_list_users(params=params)
        response_data = response.json()
        assert isinstance(response_data["pageSize"], int), "Параметр PageSize должен быть целым числом"
        assert isinstance(response_data["page"], int), "Параметр Page должен быть целым числом"

    def test_get_user_list(self, api_manager, user_creds):
        """
        Тест на запрос списка юзеров с Парамами обычным юзером.
        """
        params = {"roles": "SUPER_ADMIN",
                  "pageSize": 4,
                  "page": 1.5,
                  "createAt": "asc"}
        api_manager.auth_api.authenticate_user(user_creds)
        response = api_manager.user_api.get_list_users(params=params)
        response_data = response.json()
        assert isinstance(response_data["pageSize"], int), "Параметр PageSize должен быть целым числом"
        assert isinstance(response_data["page"], int), "Параметр Page должен быть целым числом"