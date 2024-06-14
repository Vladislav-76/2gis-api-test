import pytest
from datetime import datetime, timedelta
from status import HTTP_400_BAD_REQUEST

from tests.settings import (
    CORRECT_LOCATION_DATA,
    LOCATION_RESPONSE_TYPES,
    OPTIONAL_LOCATION_FIELDS,
    REQUIED_LOCATION_FIELDS,
)


def test_structure(request_api):
    """Проверка структуры ответа."""

    data = request_api.create_favorite_location(**CORRECT_LOCATION_DATA).json()
    fields_names_is_correct = (field in LOCATION_RESPONSE_TYPES for field in data)
    assert all(fields_names_is_correct)
    fields_types_is_correct = (isinstance(data[field], LOCATION_RESPONSE_TYPES[field]) for field in data)
    assert all(fields_types_is_correct)


@pytest.mark.parametrize("optional_field", OPTIONAL_LOCATION_FIELDS)
def test_optional_fields(request_api, optional_field):
    """Проверка ответа на запрос без необязательных полей."""

    fields = CORRECT_LOCATION_DATA.copy()
    del fields[optional_field]
    data = request_api.create_favorite_location(**fields).json()
    fields_names_is_correct = (data[field] == value for field, value in fields.items())
    assert all(fields_names_is_correct)
    assert data[optional_field] is None


@pytest.mark.parametrize("required_field", REQUIED_LOCATION_FIELDS)
def test_required_fields(request_api, required_field):
    """Проверка ответа на запрос без обязательных полей."""

    fields = CORRECT_LOCATION_DATA.copy()
    del fields[required_field]
    response = request_api.get_response(
        method="POST",
        url=request_api.base_url + request_api.favorites_url,
        data=fields,
        cookies=request_api.get_token().get_dict(),
    )
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_id_increasing(request_api):
    first_id = request_api.create_favorite_location(**CORRECT_LOCATION_DATA).json()["id"]
    second_id = request_api.create_favorite_location(**CORRECT_LOCATION_DATA).json()["id"]
    assert first_id < second_id


def test_created_at(request_api):
    time_string = request_api.create_favorite_location(**CORRECT_LOCATION_DATA).json()["created_at"]
    try:
        iso_time = datetime.fromisoformat(time_string)
    except ValueError:
        iso_time = False
    assert iso_time
    if iso_time:
        time_now = datetime.now(iso_time.tzinfo)
        assert iso_time > time_now - timedelta(seconds=10)
        assert iso_time <= time_now
