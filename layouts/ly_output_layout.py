from dash import html
from components.c_kpi_group import create_kpi_group
from components.c_display_chart_group import create_display_chart_group
from controls.cl_button_output_group import create_btn_output_group
import dash_mantine_components as dmc


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
                [
                    html.Tr(
                        html.Td(
                            create_display_chart_group(),
                            colSpan=3,
                            id="output-layout",
                        )

                    )
                ]
            )
        ],
        className="table-output",
        # style={"border": "1px solid #DCDCDC"}
    )
