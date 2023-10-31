import dash_mantine_components as dmc
from dash import html


# category_list : .json
def create_kpi(item):
    return dmc.Container(
        [
            dmc.Badge(
                item["label"],
                color=item["color"],
                size="lg"),
            dmc.Text(
                str(item["value"]) + " " + item["unit"],
                size="xl")
        ]
    )
