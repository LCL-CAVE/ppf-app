import dash_mantine_components as dmc
from dash import html


# category_list : .json
# context: string e.g., "demand"
def create_slider(item, context):
    return dmc.Container(
        [
            dmc.Text(item["label"]),
            dmc.Slider(
                id="slider_" + context + "_" + item["id"],
                min=item["min"],
                max=item["max"],
                step=item["step"],
                value=item["value"],
                mb=item["margin_bottom"],
                color="indigo",
                radius="xs",
                marks=item["mark"],
                labelAlwaysOn=item["label_on"],
                size="xs",
                # style={'width': "100%"},
            ),
        ],
        mb=15,
    )
