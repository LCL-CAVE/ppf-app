import dash_mantine_components as dmc
from dash import html
from components.c_slider import create_slider


# category_list : .json
# context: string e.g., "demand"
def create_slider_group(item_list, context):
    return html.Div(
        [
            create_slider(item, context)

            # style={'width': "100%"},
            for item in item_list
        ],
        # mb=15
    )
