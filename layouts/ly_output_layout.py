from dash import html
from components.c_kpi_group import create_kpi_group
from components.c_display_chart_group import create_display_chart_group
from controls.cl_button_output_group import create_btn_output_group
import dash_mantine_components as dmc


def create_output_layout():
    start_date_train_initial = "2018-01-01"
    finish_date_train_initial = "2019-01-01"
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
                            create_display_chart_group(start_date_train_initial,finish_date_train_initial),
                            colSpan=3,
                            id="output-layout",
                        )

                    )
                ]
            )
        ],
        className="table-output",
    )
