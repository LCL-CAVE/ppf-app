from dash import html
from components.c_date_picker import create_date_picker


# item_list : .json
# context: string e.g., "demand"
def create_date_picker_group(item_list, context):
    return html.Div(
        [
            create_date_picker(item, context)
            for item in item_list
        ],
    )
