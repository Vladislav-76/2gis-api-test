from datetime import datetime, timedelta

import pytest
from status import HTTP_400_BAD_REQUEST

from tests.settings import (CORRECT_LOCATION_COLORS, CORRECT_LOCATION_DATA,
                            CORRECT_LOCATION_LATS, CORRECT_LOCATION_LONS,
                            CORRECT_LOCATION_TITLES, INCORRECT_LOCATION_COLORS,
                            INCORRECT_LOCATION_LATS, INCORRECT_LOCATION_LONS,
                            INCORRECT_LOCATION_TITLES, LOCATION_RESPONSE_TYPES,
                            OPTIONAL_LOCATION_FIELDS, REQUIED_LOCATION_FIELDS)


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
    """Проверка возрастания id."""
    first_id = request_api.create_favorite_location(**CORRECT_LOCATION_DATA).json()["id"]
    second_id = request_api.create_favorite_location(**CORRECT_LOCATION_DATA).json()["id"]
    assert first_id < second_id


def test_created_at(request_api):
    """Проверка корректности формата и правильности указания времени."""

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


@pytest.mark.parametrize("title", CORRECT_LOCATION_TITLES)
def test_correct_titles(request_api, title):
    """Проверка сохранения корректных значений названия."""

    fields = CORRECT_LOCATION_DATA.copy()
    fields["title"] = title
    response_title = request_api.create_favorite_location(**fields).json()["title"]
    assert response_title == title


@pytest.mark.parametrize("title", INCORRECT_LOCATION_TITLES)
def test_incorrect_titles(request_api, title):
    """Проверка невозможности сохранения некорректных значений названия."""

    fields = CORRECT_LOCATION_DATA.copy()
    fields["title"] = title
    response = request_api.create_favorite_location(**fields)
    assert response.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.parametrize("lat", CORRECT_LOCATION_LATS)
def test_correct_lats(request_api, lat):
    """Проверка сохранения корректных значений широты."""

    fields = CORRECT_LOCATION_DATA.copy()
    fields["lat"] = lat
    response_lat = request_api.create_favorite_location(**fields).json()["lat"]
    assert response_lat == lat


@pytest.mark.parametrize("lat", INCORRECT_LOCATION_LATS)
def test_incorrect_lats(request_api, lat):
    """Проверка невозможности сохранения некорректных значений широты."""

    fields = CORRECT_LOCATION_DATA.copy()
    fields["lat"] = lat
    response = request_api.create_favorite_location(**fields)
    assert response.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.parametrize("lon", CORRECT_LOCATION_LONS)
def test_correct_lons(request_api, lon):
    """Проверка сохранения корректных значений долготы."""

    fields = CORRECT_LOCATION_DATA.copy()
    fields["lon"] = lon
    response_lon = request_api.create_favorite_location(**fields).json()["lon"]
    assert response_lon == lon


@pytest.mark.parametrize("lon", INCORRECT_LOCATION_LONS)
def test_incorrect_lons(request_api, lon):
    """Проверка невозможности сохранения некорректных значений долготы."""

    fields = CORRECT_LOCATION_DATA.copy()
    fields["lon"] = lon
    response = request_api.create_favorite_location(**fields)
    assert response.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.parametrize("color", CORRECT_LOCATION_COLORS)
def test_correct_colors(request_api, color):
    """Проверка сохранения корректных значений цвета."""

    fields = CORRECT_LOCATION_DATA.copy()
    fields["color"] = color
    response_color = request_api.create_favorite_location(**fields).json()["color"]
    assert response_color == color


@pytest.mark.parametrize("color", INCORRECT_LOCATION_COLORS)
def test_incorrect_colors(request_api, color):
    """Проверка невозможности сохранения некорректных значений цвета."""

    fields = CORRECT_LOCATION_DATA.copy()
    fields["color"] = color
    response = request_api.create_favorite_location(**fields)
    assert response.status_code == HTTP_400_BAD_REQUEST
