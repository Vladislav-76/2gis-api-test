from status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from tests.settings import CORRECT_LOCATION_DATA


def test_connect_token(request_api):
    """Проверка соединения с эндпойнтом https://regions-test.2gis.com/v1/auth/tokens"""

    response = request_api.get_response("POST", request_api.base_url + request_api.token_url)
    assert response.status_code == HTTP_200_OK


def test_connect_favorites(request_api):
    """Проверка соединения с эндпойнтом https://regions-test.2gis.com/v1/favorites"""

    response = request_api.get_response(
        method="POST",
        url=request_api.base_url + request_api.favorites_url,
        data=CORRECT_LOCATION_DATA,
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED
