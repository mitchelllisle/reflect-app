import pytest


def test_create_page(dash_duo, dash_app):
    """Test for checking that the home page is the create page and that all elements exist"""
    dash_duo.wait_for_page("http://localhost:8050/", timeout=pytest.page_timeout)
    dash_duo.wait_for_text_to_equal(
        "#add-project-generate-name", "Generate one for me", timeout=pytest.element_timeout)
    dash_duo.wait_for_text_to_equal("#add-project-save", "Create", timeout=pytest.element_timeout)
