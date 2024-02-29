import dash_mantine_components as dmc
from dash import html


# category_list : .json
# context: string e.g., "demand"
def create_num_input(item, context):
    return dmc.Group(
        [
            dmc.NumberInput(
                label=item["label"],
                # description="Sccc",
                id="num_input_" + context + "_" + item["id"],
                min=item["min"],
                max=item["max"],
                step=item["step"],
                value=item["value"],
                stepHoldDelay=500,
                stepHoldInterval=100,
                # mb=item["margin_bottom"],
                # color="indigo",
                # radius="xs",
                # marks=item["mark"],
                # labelAlwaysOn=item["label_on"],
                # size="xs",
                style={'width': "45%"},
            ),
            dmc.NumberInput(
                label=item["label_change"],
                # description="Sccc",
                id="num_input_" + context + "_" + item["id_change"],
                min=item["min_change"],
                max=item["max_change"],
                step=item["step_change"],
                value=item["value_change"],
                stepHoldDelay=500,
                stepHoldInterval=100,
                # mb=item["margin_bottom"],
                # color="indigo",
                # radius="xs",
                # marks=item["mark"],
                # labelAlwaysOn=item["label_on"],
                # size="xs",
                style={'width': "45%"},
            ),
        ],
        mb=item["margin_bottom"],
    )
