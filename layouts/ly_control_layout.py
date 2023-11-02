from controls.cl_control_accordion import create_control_accordion
from controls.cl_button_run import create_btn_run
import dash_mantine_components as dmc


def create_control_layout():
    return dmc.Stack(
        id="div-control-layout",
        children=[
            create_control_accordion(),
            create_btn_run(),
            dmc.Text(
                "This work is licensed under [creative commons license].",
                underline=True,
                size="xs",
                mt=20,
                mb=20
            ),
        ],
    )
