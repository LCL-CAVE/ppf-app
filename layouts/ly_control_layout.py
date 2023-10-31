from controls.cl_control_accordion import create_control_accordion
import dash_mantine_components as dmc


def create_control_layout():
    return dmc.Stack(
        id="accordion-control-layout",
        children=[
            create_control_accordion(),
            dmc.Button(
                "Start",
                id="load-button",
                variant="outline",
                fullWidth=True,
            ),
            dmc.Text("This work is licensed under [creative commons license].",
                     underline=True,
                     size="xs",
                     mt=20, mb=20),
        ],
    )
