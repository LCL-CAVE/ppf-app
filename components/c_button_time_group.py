import dash_mantine_components as dmc
from controls.cl_json_parser import parse_json
from dash import html
import os


def create_btn_time_group():
    btn_list = parse_json(
        os.path.join(
            os.path.dirname('./params/'),
            'time_group.json')
    )
    return dmc.SegmentedControl(
            id="btn_time_group_display",
            value=btn_list[-1]["id"],
            data=[
                {"value": item["id"], "label": item["label"]}
                for item in btn_list
            ],
            className="btn-time-grouper",
            color="#0000FF",
            size="sm",
        )

