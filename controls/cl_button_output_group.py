from components.c_button_output import create_btn_output
import dash_mantine_components as dmc
from dash import html
from controls.cl_json_parser import parse_json
import os


def create_btn_output_group():
    item_list = parse_json(
        os.path.join(
            os.path.dirname('./params/'),
            'output_selector.json')
    )
    return [
        html.Th(
            dmc.Container(
                [
                    dmc.Badge(
                        "Select Outputs",
                        variant="outline",
                        size="lg",
                        color='gray',
                        fullWidth=True),
                ]
                # +
                # [
                #     dmc.SegmentedControl(
                #         id="segmented",
                #         value="ng",
                #         data=[
                #             {"value": "react", "label": "React"},
                #             {"value": "ng", "label": "Angular"},
                #             {"value": "svelte", "label": "Svelte"},
                #             {"value": "vue", "label": "Vue"},
                #         ],
                #         orientation="vertical",
                #         fullWidth=True,
                #         color="blue",
                #         mt=20,
                #     )
                # ]
                # +
                # [
                #     dmc.ChipGroup(
                #         [
                #             dmc.Chip(
                #                 x,
                #                 value=x,
                #                 variant="outline",
                #                 style={"width": "100%",},
                #
                #
                #             )
                #             for x in ["React", "Django", "Dash", "Vue"]
                #         ],
                #         id="chips-values",
                #         value=["React", "Dash"],
                #         multiple=True,
                #         align="flex-start"
                #         # style={"width": "100%", "orientation": "vertical"},
                #         # grow=1,
                #     )
                # ]
                +
                [
                    create_btn_output(item)
                    for item in item_list
                ],
                className="cont-output-selector",
            ),
            rowSpan=10,
            className="col-total-output-selector",
        ),
    ]
