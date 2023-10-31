import dash_mantine_components as dmc
from dash import html


# category_list : .json
def create_btn_output(item):
    return dmc.Button(
        item['label'],
        mt=item['margin_top'],
        id="btn_" + "output_selector_" + item['id'],
        variant=item["type"],
        fullWidth=True,
        className="btn-output-selector",
    )
