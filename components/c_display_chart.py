import dash_mantine_components as dmc
from dash import html


# category_list : .json
def create_display_chart(item):
    return dmc.Image(
        src="/assets/eecc.png",
        alt=item["id"],
    )
