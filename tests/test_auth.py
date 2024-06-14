from time import sleep
from status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from tests.settings import CORRECT_LOCATION_DATA


def test_obtain_token(request_api):
    """Проверка получения токена."""

    cookies = request_api.get_token().get_dict()
    assert "token" in cookies.keys()
    assert len(cookies["token"])
    assert isinstance(cookies["token"], str)


def test_correct_auth(request_api):
    """Проверка ответа с корректным токеном."""

    response = request_api.create_favorite_location(**CORRECT_LOCATION_DATA)
    assert response.status_code == HTTP_200_OK


def test_incorrect_token_auth(request_api):
    """Проверка ответа с некорректным токеном."""

    token = "incorrect token"
    response = request_api.get_response(
        method="POST",
        url=request_api.base_url + request_api.favorites_url,
        data=CORRECT_LOCATION_DATA,
        cookies={"token": token},
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_expired_token_auth(request_api):
    """Проверка ответа с просроченным токеном."""

    cookies = request_api.get_token().get_dict()
    sleep(2)
    response = request_api.get_response(
        method="POST",
        url=request_api.base_url + request_api.favorites_url,
        data=CORRECT_LOCATION_DATA,
        cookies=cookies,
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED
