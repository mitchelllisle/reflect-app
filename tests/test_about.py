from reflect import __version__
import pytest


def test_about_page(dash_duo, dash_app):
    dash_duo.wait_for_page("http://localhost:8050/about", timeout=pytest.page_timeout)
    dash_duo.wait_for_text_to_equal("#about-version", __version__, timeout=pytest.element_timeout)
