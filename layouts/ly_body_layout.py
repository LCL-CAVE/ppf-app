from layouts.ly_control_layout import create_control_layout
from layouts.ly_output_layout import create_output_layout
import dash_mantine_components as dmc
import os




def create_body_layout():

    return dmc.Grid(
        children=
        [
            dmc.Col(
                create_control_layout(),
                span="auto",
                className="control-col",
            ),
            dmc.Col(
                create_output_layout(),
                span=9,
                # style={"padding": 0, 'margin': 0}
            ),
        ],


    )
