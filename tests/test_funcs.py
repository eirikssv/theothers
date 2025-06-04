import datetime
import sys
import types
import pytest

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
sys.modules['pandas'] = types.ModuleType('pandas')

# Provide minimal Pillow structure
PIL_module = types.ModuleType('PIL')
Image_module = types.ModuleType('Image')
PIL_module.Image = Image_module
sys.modules['PIL'] = PIL_module
sys.modules['PIL.Image'] = Image_module

from pages.mods.funcs import bubblecolor

@pytest.mark.parametrize(
    "day_diff,expected",
    [
        (0, 'green'),
        (3, 'green'),
        (4, 'yellow'),
        (5, 'yellow'),
        (6, 'orange'),
        (8, 'orange'),
        (9, 'red'),
    ]
)
def test_bubblecolor(day_diff, expected):
    latest = datetime.date(2023, 1, 10)
    eval_date = latest - datetime.timedelta(days=day_diff)
    assert bubblecolor(latest, eval_date) == expected
