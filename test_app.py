from dash.testing.application_runners import import_app
from selenium.webdriver.common.by import By

def test_header_present(dash_duo):
    """Test that the header title is present on the page."""
    app = import_app("app")
    dash_duo.start_server(app)
    
    # Check if an H1 element is present and contains the expected title text
    header = dash_duo.find_element("h1")
    assert header is not None
    assert "Soul Foods" in header.text

def test_visualization_present(dash_duo):
    """Test that the line chart visualization graph is present."""
    app = import_app("app")
    dash_duo.start_server(app)
    
    # Check if the graph component exists by its id
    graph = dash_duo.find_element("#sales-line-chart")
    assert graph is not None

def test_region_picker_present(dash_duo):
    """Test that the region filter radio button component is present."""
    app = import_app("app")
    dash_duo.start_server(app)
    
    # Check if the radio items component exists by its id
    region_filter = dash_duo.find_element("#region-filter")
    assert region_filter is not None