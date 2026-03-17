from http import HTTPStatus


class OverLimitError(Exception):
    status_code = HTTPStatus.TOO_MANY_REQUESTS
