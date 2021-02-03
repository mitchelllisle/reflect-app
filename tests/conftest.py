from reflect.app import app
import pytest


def pytest_configure():
    pytest.page_timeout = 10
    pytest.element_timeout = 4


@pytest.fixture(scope="function")
def dash_app(dash_duo):
    dash_duo.start_server(app)
