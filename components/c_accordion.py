import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify as dicon


# category_list : .json
def create_accordion(category_list):
    return dmc.Accordion(
        chevronPosition="right",
        variant="separated",
        radius="md",
        mb=10,
        children=[
            dmc.AccordionItem(
                value=category['item']['value'],
                className="accordion_item",
                children=[
                    dmc.AccordionControl(
                        dmc.Group(
                            [
                                dicon(
                                    icon=category['item']['icon'],
                                    color=dmc.theme.DEFAULT_COLORS[category['item']['icon_color']][6],
                                    width=35,
                                ),
                                html.Div(
                                    [
                                        dmc.Text(
                                            category['item']['label']
                                        ),
                                        dmc.Text(
                                            category['item']['text'],
                                            size="sm",
                                            weight=400,
                                            color="dimmed"
                                        ),
                                    ]
                                ),
                            ]
                        )
                    ),
                    dmc.AccordionPanel(
                        [
                            dmc.Divider(
                                variant="solid",
                                mb=30
                            ),
                            # category['content'],
                            dmc.Text(category['content'], size="sm")
                        ],
                    )
                ]
            )
            for category in category_list
        ],
    )
