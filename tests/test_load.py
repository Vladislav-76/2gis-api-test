from threading import Thread

import pytest
from status import HTTP_200_OK

from tests.settings import CORRECT_LOCATION_DATA, REQUESTS_NUMBERS


@pytest.mark.parametrize("requests", REQUESTS_NUMBERS)
def test_load(request_api, requests):
    """Проверка статуса ответа при отправке параллельных запросов."""

    response_statuses_is_ok = []

    def get_response_status():
        status = request_api.create_favorite_location(**CORRECT_LOCATION_DATA)
        response_statuses_is_ok.append(status == HTTP_200_OK)

    requests_pool = (Thread(target=get_response_status) for _ in range(requests))
    for request in requests_pool:
        request.start()

    assert all(response_statuses_is_ok)
