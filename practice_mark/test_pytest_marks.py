import pytest


@pytest.mark.skip(reason="Временно отключен")
def test_example():
    assert 1 + 1 == 2

skip_test = True
@pytest.mark.skipif(skip_test, reason="Тест отключен вручную")
def test_skipif_demo():
    assert True

@pytest.mark.xfail(reason="Функция еще не реализована")
def test_future_feature():
    assert 1 == 2

@pytest.mark.xfail(reason="Баг в системе")
def test_fixed_bug():
    assert 2 + 2 == 4

@pytest.fixture
def setup_data():
    print("Setup")

def test_with_fixture(setup_data):
    assert True

@pytest.mark.usefixtures("setup_data")
def test_with_usefixtures():
    assert True

