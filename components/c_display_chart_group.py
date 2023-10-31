import dash_mantine_components as dmc
from dash import html
from components.c_display_chart import create_display_chart
from controls.cl_json_parser import parse_json
import os


# category_list : .json
def create_display_chart_group():
    item_list = parse_json(
        os.path.join(
            os.path.dirname('./params/'),
            'chart.json')
    )
    kpi_item_list = parse_json(
        os.path.join(
            os.path.dirname('./params/'),
            'kpi.json')
    )
    return [
        html.Tr(
            html.Td(
                create_display_chart(item),
                className="td-col-chart",
                colSpan=len(kpi_item_list),
            ),
        )
        for item in item_list
    ]
