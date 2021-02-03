import pytest


def test_navbar(dash_duo, dash_app):
    """Test for making sure everything in the navbar is being rendered including app name and links"""
    dash_duo.wait_for_page("http://localhost:8050/", timeout=pytest.page_timeout)
    assert dash_duo.find_element("#reflect-navbar").text.split("\n") == ["Reflect", "Projects", "About"]