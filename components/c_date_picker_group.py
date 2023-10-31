import dash_mantine_components as dmc
from dash import html
import time
from datetime import datetime, timedelta, date


# item_list : .json
# context: string e.g., "demand"
def create_date_picker_group(item_list, context):
    return dmc.Group(
        [
            html.Div(
                [
                    dmc.DateRangePicker(
                        label=item["label"],
                        id="date_picker_" + context + "_" + item["label"].lower(),
                        value=[
                            date(
                                item['initial_year'],
                                item['initial_month'],
                                item['initial_day'],
                            ),
                            date(
                                item['initial_year'],
                                item['initial_month'],
                                item['initial_day'],
                            ) + timedelta(days=365)
                        ],
                        minDate=date(
                            item['min_year'],
                            item['min_month'],
                            item['min_day'],
                        ),
                        maxDate=date(
                            item['max_year'],
                            item['max_month'],
                            item['max_day'],
                        ),
                        mb=10,
                    ),
                ],
                style={'width': "100%"},
            )
            for item in item_list
        ],
        mb=15
    )
