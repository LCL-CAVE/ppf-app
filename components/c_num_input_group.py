from dash import html
from components.c_num_input import create_num_input


# category_list : .json
# context: string e.g., "demand"
def create_num_input_group(item_list, context):
    return html.Div(
        [
            create_num_input(item, context)
            for item in item_list
        ],
    )
