import logging
import pytest
import requests

from tests.settings import LOG_FILE_PATH, LOG_LEVEL

logging.basicConfig(
    level=LOG_LEVEL,
    filename=LOG_FILE_PATH,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class ApiRequest:
    """Базовый класс запросов к API."""

    base_url: str = "https://regions-test.2gis.com/v1/"
    favorites_url: str = "favorites"
    token_url: str = "auth/tokens"
    # headers: dict = {"Content-Type": "application/json"}
    cookies: str = ""
    # timeout: int = 5

    def get_response(self, method, url, data=dict(), cookies="", log=True):
        """Универсальный метод запроса."""

        response = requests.request(
            method=method,
            url=url,
            data=data,
            cookies=cookies,
        )
        if log:
            logging.info(self.make_log(response))
        return response

    @staticmethod
    def make_log(response):
        return f"""
            REQUEST:
            URL: {response.request.url}, METHOD: {response.request.method}, BODY: {response.request.body}
            RESPONSE:
            STATUS_CODE: {response.status_code}, DATA: {response.content}
        """

    def get_token(self, url=''):
        """Возвращает cookies с токеном."""

        url = url if url else self.token_url
        response = self.get_response('POST', self.base_url + url)
        return response.cookies

    def create_favorite_location(self, title, lat, lon, color=None, token=True):
        """Возвращает ответ на запрос создания избранного места."""

        data = {"title": title, "lat": lat, "lon": lon}
        if color:
            data["color"] = color
        cookies = self.get_token().get_dict() if token else self.cookies
        url = self.base_url + self.favorites_url
        return self.get_response("POST", url, data, cookies)


@pytest.fixture()
def request_api():
    return ApiRequest()
