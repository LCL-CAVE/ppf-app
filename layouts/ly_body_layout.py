from layouts.ly_control_layout import create_control_layout
from layouts.ly_output_layout import create_output_layout
import dash_mantine_components as dmc


def create_body_layout():
    return dmc.Grid(
        children=
        [
            dmc.Col(
                [
                    create_control_layout(),
                    # dmc.Text(
                    #     "This work is licensed under [creative commons license].",
                    #     underline=True,
                    #     size="xs",
                    #     mt=20,
                    #     mb=20
                    # ),
                ],
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
