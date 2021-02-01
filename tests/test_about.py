from reflect.app import app
from reflect import __version__
import pytest


def test_about_page(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_text_to_equal("#add-project-generate-name", "Generate one for me", timeout=4)

    dash_duo.wait_for_page("http://localhost:8050/about", timeout=10)
    dash_duo.wait_for_text_to_equal("#about-version", __version__, timeout=4)
