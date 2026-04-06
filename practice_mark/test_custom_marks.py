import pytest

import time

@pytest.mark.smoke
def test_addition():
    assert 1 + 1 == 2

@pytest.mark.regression
def test_subtraction():
    assert 5 - 3 == 2

@pytest.mark.smoke
def test_multiplication():
    assert 2 * 3 == 6

@pytest.mark.slow
def test_division():
    assert 10 / 2 == 5

@pytest.mark.api
@pytest.mark.slow
def test_string_concatenation():
    time.sleep(5)
    assert "Hello " + "World" == "Hello World"

@pytest.mark.api
def test_string_upper():
    assert "hello".upper() == "HELLO"

@pytest.mark.smoke
@pytest.mark.api
def test_list_append():
    lst = [1, 2, 3]
    lst.append(4)
    assert lst == [1, 2, 3, 4]

@pytest.mark.skip(reason="Временно отключен")
def test_list_remove():
    lst = [1, 2, 3, 4]
    lst.remove(3)
    assert lst == [1, 2, 4]

@pytest.mark.healthcheck
def test_dict_get():
    d = {'key': 'value'}
    assert d.get('key') == 'value'

@pytest.mark.regression
@pytest.mark.integration
def test_dict_set():
    d = {}
    d['key'] = 'value'
    assert d['key'] == 'value'