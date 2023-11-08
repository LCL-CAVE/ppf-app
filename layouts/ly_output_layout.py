from dash import html
from components.c_kpi_group import create_kpi_group
from components.c_display_chart_group import create_display_chart_group
from controls.cl_button_output_group import create_btn_output_group
import dash_mantine_components as dmc
from components.c_button_time_group import create_btn_time_group


def create_output_layout():
    return html.Table(
        [
            html.Tbody(
                [
                    html.Tr(
                        create_kpi_group()
                        +
                        create_btn_output_group(),
                        className="tr-row-kpi",
                    )
                ]
                +
                create_display_chart_group(),
            )
        ],
        className="table-output",
    )
