from components.c_slider_group import create_slider_group
from components.c_accordion import create_accordion
from components.c_date_picker_group import create_date_picker_group
from components.c_dropdown import create_dropdown_group
from controls.cl_json_parser import parse_json
import os
from dash import html


def create_control_accordion():
    json_category = parse_json(
        os.path.join(
            os.path.dirname('./params/'),
            'category.json')
    )

    category_with_content = [
        {
            "item": json_category[0],
            "content": create_dropdown_group(parse_json(os.path.join(
                os.path.dirname('./params/'),
                'country.json')
            ),
                json_category[0]["value"]),
        },
        {
            "item": json_category[1],
            "content": create_date_picker_group(parse_json(os.path.join(
                os.path.dirname('./params/'),
                'time_horizon.json')
            ),
                json_category[1]["value"]),
        },
        {
            "item": json_category[2],
            "content": create_slider_group(parse_json(os.path.join(
                os.path.dirname('./params/'),
                'capacity.json')
            ),
                json_category[2]["value"]),
        },
        {
            "item": json_category[3],
            "content": create_slider_group(parse_json(os.path.join(
                os.path.dirname('./params/'),
                'demand.json')
            ),
                json_category[3]["value"]),
        },
        {
            "item": json_category[4],
            "content": create_slider_group(parse_json(os.path.join(
                os.path.dirname('./params/'),
                'price.json')
            ),
                json_category[4]["value"]),
        }
    ]
    return html.Div(
        create_accordion(category_with_content)
    )
