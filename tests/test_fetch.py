import sys
import types
from unittest.mock import patch, Mock

# Create dummy modules with attributes used in funcs
streamlit = types.ModuleType('streamlit')
sys.modules['streamlit'] = streamlit

streamlit_option_menu = types.ModuleType('streamlit_option_menu')
streamlit_option_menu.option_menu = lambda *args, **kwargs: None
sys.modules['streamlit_option_menu'] = streamlit_option_menu

streamlit_folium = types.ModuleType('streamlit_folium')
streamlit_folium.st_folium = lambda *args, **kwargs: None
streamlit_folium.folium_static = lambda *args, **kwargs: None
sys.modules['streamlit_folium'] = streamlit_folium

sys.modules['folium'] = types.ModuleType('folium')

# Mock plotly package and submodules
plotly_module = types.ModuleType('plotly')
plotly_module.express = types.ModuleType('express')
plotly_module.graph_objects = types.ModuleType('graph_objects')
sys.modules['plotly'] = plotly_module
sys.modules['plotly.express'] = plotly_module.express
sys.modules['plotly.graph_objects'] = plotly_module.graph_objects

sys.modules['last_seddel'] = types.ModuleType('last_seddel')

pd_module = types.ModuleType('pandas')

class DummyDataFrame(list):
    def __init__(self, data=None):
        super().__init__(data or [])

pd_module.DataFrame = DummyDataFrame
sys.modules['pandas'] = pd_module
import pandas as pd

PIL_module = types.ModuleType('PIL')
Image_module = types.ModuleType('Image')
PIL_module.Image = Image_module
sys.modules['PIL'] = PIL_module
sys.modules['PIL.Image'] = Image_module

from pages.mods.funcs import fetch_landing_data


def test_fetch_landing_data():
    sample = [
        {"year": 2022, "amount": 100},
        {"year": 2022, "amount": 200},
    ]

    mock_response = Mock()
    mock_response.json.return_value = sample
    mock_response.raise_for_status.return_value = None

    with patch('pages.mods.funcs.requests.get', return_value=mock_response) as mock_get:
        df = fetch_landing_data(2022)
        mock_get.assert_called_once()

    expected = pd.DataFrame(sample)
    assert isinstance(df, pd.DataFrame)
    assert df == expected
