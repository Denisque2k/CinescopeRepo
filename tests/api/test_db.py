class TestDB:
    def test_db_requests(self, super_admin, db_helper, created_test_user):
        assert created_test_user == db_helper.get_user_by_id(created_test_user.id)
        assert db_helper.user_exists_by_email("api1@gmail.com")

    def test_delete_movie_requests(self, super_admin, db_helper, create_test_movie_hardcode):
        assert db_helper.movie_exists_by_id(101010) is False, "Фильм не найден"
        db_helper.create_test_movie(create_test_movie_hardcode)
        assert db_helper.get_movie_by_id(101010), "Фильм не найден"
        super_admin.api.movie_api.delete_movie(movie_id=101010)
        assert db_helper.movie_exists_by_id(101010) is False, "Фильм не был удален"
