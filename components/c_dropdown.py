import dash_mantine_components as dmc
from dash import html


# item_list : .json
# context: string e.g., "country"
def create_dropdown_group(item_list, context):
    return html.Div(
        [
            dmc.Select(
                label="Select " + context,
                id="dropdown_" + context,
                # placeholder="Select a country",
                value=item_list[0]["id"],
                radius='sm',
                mb=15,
                data=
                [
                    {
                        "value": item["id"],
                        "label": item["label"]
                    }
                    for item in item_list
                ],
            ),
        ],
        style={'width': "100%"},
    )
