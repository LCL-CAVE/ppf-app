import dash_mantine_components as dmc
import dash
from dash_iconify import DashIconify
from dash import html
from dash import Output, callback, Input, State
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import time
from datetime import datetime, timedelta, date

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,"
        "400;1,500;1,700;1,900&display=swap",
    ]
)
app.title = "sample mantine app"
server = app.server

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

dropdown_country = html.Div(
    [
        dmc.Select(
            label="Select country",
            id="country-select",
            # placeholder="Select a country",
            value="spain",
            radius='sm',
            data=[
                {"value": "spain", "label": "Spain"},
                {"value": "france", "label": "France"},
                {"value": "lux", "label": "Luxembourg"},
                {"value": "germany", "label": "Germany"},
                {"value": "austria", "label": "Austria"},
{"value": "austria1", "label": "Austria1"},
            ],
            mb=15,
            # style={"width": "100%", "color": "indigo"},
            className='dropdown_item',
        ),
    ]
)

dropdown_country2 = html.Div(
    [
        dmc.MultiSelect(
            label="Select countries",
            id="country-select2",
            placeholder="Select multiple countries",
            value="spain1",
            radius='sm',
            data=[
                {"value": "spain1", "label": "Spain"},
                {"value": "france1", "label": "France"},
                {"value": "lux1", "label": "Luxembourg"},
                {"value": "germany1", "label": "Germany"},
                {"value": "austria1", "label": "Austria"},
            ],
            mb=35,
            style={"width": "100%", "color": "indigo"},
        ),
    ]
)

datepicker_trainingperiod = html.Div(
    [
        dmc.DateRangePicker(
            label="Training period",
            id="training-period",
            value=[datetime.now().date(), datetime.now().date() + timedelta(days=180)],
            minDate=date(2020, 8, 5),
            mb=35,
            style={"width": "100%", "color": "indigo"},
        ),
    ]
)

datepicker_forecastingperiod = html.Div(
    [
        dmc.DateRangePicker(
            label="Forecasting period",
            id="forecasting-period",
            value=[datetime.now().date(), datetime.now().date() + timedelta(days=180)],
            minDate=date(2021, 8, 5),
            mb=35,
        ),
    ]
)

dropdown_power_type = html.Div(
    [
        dmc.Text("Select power type"),
        dmc.SegmentedControl(
            id="power-type",
            color="indigo",
            value="renew",
            fullWidth=True,
            radius='sm',
            data=[
                {"value": "renew", "label": "Renewable"},
                {"value": "non-renew", "label": "Non-renewable"},
            ],
            mb=10,
        ),
    ]
)

dropdown_power_renewable = html.Div(
    [
        dmc.Text("Select renewable power source"),
        dmc.SegmentedControl(
            id="power-renewable",
            color="indigo",
            value="solar",
            fullWidth=True,
            radius='sm',
            data=[
                {"value": "solar", "label": "Solar"},
                {"value": "wind", "label": "Wind"},
                {"value": "hydro", "label": "Hydro"},
            ],
            mb=10,
        ),
    ]
)

dropdown_power_non_renewable = html.Div(
    [
        dmc.Text("Select non-renewable power source"),
        dmc.SegmentedControl(
            id="power-non-renewable",
            color="indigo",
            value="gas",
            fullWidth=True,
            radius='sm',
            data=[
                {"value": "gas", "label": "Gas"},
                {"value": "nuck", "label": "Nuclear"},
                {"value": "coal", "label": "Coal"},
            ],
            mb=35,
        ),
    ]
)

chip_power_renewable = html.Div(
    [
        dmc.Text("Select non-renewable power sources"),
        dmc.ChipGroup(
            [
                dmc.Chip(
                    "Wind",
                    value="wind",
                    variant="filled",
                    radius="sm",
                    color="indigo",
                ),
                dmc.Chip(
                    "Solar",
                    value="solar",
                    variant="filled",
                    radius="sm",
                    color="indigo",
                ),
                dmc.Chip(
                    "Hydro",
                    value="hydro",
                    variant="filled",
                    radius="sm",
                    color="indigo",
                ),

            ],
            id="chips-power-renew",
            value=["solar", "hydro"],
            multiple=True,
            # grow=1,
            mb=10,
        ),
    ],

)

chip_power_non_renewable = html.Div(
    [
        dmc.Text("Select non-renewable power sources"),
        dmc.ChipGroup(
            [
                dmc.Chip(
                    "Nuclear",
                    value="nuke",
                    variant="filled",
                    radius="sm",
                    color="indigo",
                ),
                dmc.Chip(
                    "Coal",
                    value="coal",
                    variant="filled",
                    radius="sm",
                    color="indigo",
                ),
                dmc.Chip(
                    "Gas",
                    value="gas",
                    variant="filled",
                    radius="sm",
                    color="indigo",
                ),

            ],
            id="chips-power-non-renew",
            value=["nuke", "gas"],
            multiple=True,
            mb=35,
        ),
    ]
)

slider_demand_level = html.Div(
    [
        dmc.Text("Demand level"),
        dmc.Slider(
            id="sdfsdf",
            min=1000,
            max=5000,
            step=500,
            value=4000,
            mb=15,
            color="indigo",
            radius="xs",
            labelAlwaysOn=True,
            size="xs",
        ),
    ]
)

slider_capacity_level = html.Div(
    [
        dmc.Text("Capacity"),
        dmc.Slider(
            min=1000,
            max=5000,
            step=500,
            value=2000,
            mb=15,
            color="indigo",
            radius="xs",
            labelAlwaysOn=True,
            size="xs",
        ),
    ]
)

slider_capacity_growth = html.Div(
    [
        dmc.Text("Capacity growth rate"),
        dmc.Slider(
            min=1,
            max=2,
            step=0.25,
            marks=[
                {"value": 1.0, "label": "low"},
                {"value": 1.25, "label": "fairly medium"},
                {"value": 1.5, "label": "medium"},
                {"value": 1.75, "label": "fairly high"},
                {"value": 2.0, "label": "high"},
            ],
            mb=35,
            value=1.5,
            color="indigo",
            radius="xs",
            labelAlwaysOn=True,
            size="xs",
        ),
    ]
)

segmentedControl_kernel = html.Div([
    dmc.Text("Kernel type"),
    dmc.SegmentedControl(
        id="segmented-kernel",
        color="indigo",
        value="ng",
        fullWidth=True,
        radius='sm',
        data=[
            {"value": "react", "label": "React"},
            {"value": "ng", "label": "Angular"},
            {"value": "svelte", "label": "Svelte"},
            {"value": "vue", "label": "Vue"},
        ],

    ),
]
)

switch_shrinking = dmc.Switch(
    size="sm",
    radius="lg",
    label="Shrinking",
    checked=True
)


def create_accordion_label(label, image, description):
    return dmc.AccordionControl(
        dmc.Group(
            [
                image,
                html.Div(
                    [
                        dmc.Text(label),
                        dmc.Text(description, size="sm", weight=400, color="dimmed"),

                    ]
                ),
            ]
        )
    )


def create_accordion_content(content):
    return dmc.AccordionPanel(dmc.Text(content, size="sm"))


icon1 = DashIconify(
    icon="majesticons:data-line",
    color=dmc.theme.DEFAULT_COLORS["blue"][6],
    width=35,
)

icon2 = DashIconify(
    icon="uil:setting",
    color=dmc.theme.DEFAULT_COLORS["green"][6],
    width=35,
)

icon3 = DashIconify(
    icon="mdi:run-fast",
    color=dmc.theme.DEFAULT_COLORS["red"][6],
    width=35,
)

style = {
    "border": f"1px solid",
    "height": "100%",
}
style_sh = {
    "box-shadow": "rgba(0,0,255, 0.16) 0px 3px 6px, rgba(0, 0, 0, 0.23) 0px 3px 6px",
}

accordion_controls = dmc.Accordion(
    chevronPosition="right",
    variant="separated",
    radius="md",
    children=[
        dmc.AccordionItem(
            [
                create_accordion_label(
                    "Initialization",
                    icon1,
                    "Select country, source type, and capacity"
                ),
                create_accordion_content(
                    [
                        dmc.Divider(variant="solid", mb=30),
                        dropdown_country,
                        dropdown_country2,
                        dropdown_power_type,
                        dropdown_power_renewable,
                        dropdown_power_non_renewable,
                        chip_power_renewable,
                        chip_power_non_renewable,
                        slider_demand_level,
                        slider_capacity_level,
                        slider_capacity_growth
                    ],
                ),
            ],
            value="id1",
            className="accordion_item",
        ),
        dmc.AccordionItem(
            [
                create_accordion_label(
                    "Simulation",
                    icon2,
                    "Select training and forecasting periods"
                ),
                create_accordion_content(
                    [
                        dmc.Divider(variant="solid", mb=30),
                        datepicker_trainingperiod,
                        datepicker_forecastingperiod,
                    ]

                ),
            ],
            value="id2",
            style=style_sh,
        ),
        dmc.AccordionItem(
            [
                create_accordion_label(
                    "Miscellaneous",
                    icon3,
                    "Select if you need additional data calibration."
                ),
                create_accordion_content(
                    [
                        dmc.Divider(variant="solid", mb=30),
                        switch_shrinking,

                    ]

                ),
            ],
            value="id3",
            style=style_sh,
        ),

    ],
    mb=10,
)

textinput_session = dmc.TextInput(label="Session name",
                                  description="Please enter session name",
                                  # required=True,
                                  mb=20)
text_select_session = dmc.Text("or import a session", mb=20)

list_sessions = dmc.Group(
    children=[
        dmc.Anchor(
            "session #12131",
            href="#",
            style={'width': "100%"},
        ),
        dmc.Anchor(
            "session #25487",
            href="#",
            style={'width': "100%"},
        ),
        dmc.Anchor(
            "session #65648",
            href="#",
            style={'width': "100%"},
        ),
        dmc.Anchor(
            "session #45878",
            href="#",
            style={'width': "100%"},
        ),
    ]
)

# df11 = px.data.stocks()
# fig11 = px.line(df11, x='date', y="GOOG")
# fig11.update_layout(autosize=True,height=100,
# margin=dict(l=0, r=0, b=0, t=0),
#                     xaxis={'showticklabels': False},
#                     yaxis={'showticklabels': False})

row1 = html.Tr(
    [
        html.Td(
            dmc.Container(
                children=[
                    # dash.dcc.Graph(figure=fig11,),
                    dmc.Badge("Fuel -23% / 24h", variant="dot", color="indigo", size="lg"),
                ], ), ),
        html.Td(dmc.Container(dmc.Badge("Electricity +7% / 24h", variant="dot", color="green", size="lg"), )),
        html.Td(dmc.Container(dmc.Badge("Coal -12% / 24h", variant="dot", color="red", size="lg"), )),
        html.Td(dmc.Container(dmc.Badge("EU Carbon Emission +2% / 24h", variant="gradient",
                                        gradient={"from": "grape", "to": "pink", "deg": 35},
                                        size="lg"),
                              )),
    ]
)

style_cont = {
    "margin-top": 20,
    "margin-left": 25,
    "margin-right": 15,
}

style_cont2 = {
    "margin-top": 15,
    "margin-right": 15,
    "border": "solid rgba(0, 24, 249, 0.3) 1px",
    "border-radius": "10px",
    "width": "550px",
    'padding': 0,
    "box-shadow": "rgba(0, 24, 249, 0.16) 0px 3px 6px, rgba(0, 0, 0, 0.23) 0px 3px 6px",
}

style_cont3 = {
    "margin-top": 15,
    "margin-right": 25,
    "border": "solid rgba(0, 24, 249, 0.3) 1px",
    "border-radius": "10px",
    "width": "550px",
    'padding': 0,
    "box-shadow": "rgba(0, 24, 249, 0.16) 0px 3px 6px, rgba(0, 0, 0, 0.23) 0px 3px 6px",
}

temp_cont1 = html.Div([
    dmc.Skeleton(
        visible=False,
        children=dmc.Container(
            id="skeleton-graph-container1",
            children=dash.dcc.Graph(),
            style={'padding': 0},
        ),
    ), ], style=style_cont2)

temp_cont2 = html.Div([
    dmc.Skeleton(
        visible=False,
        children=dmc.Container(
            id="skeleton-graph-container2",
            children=dash.dcc.Graph(),
            style={'padding': 0},
        ),
    ), ], style=style_cont3)

temp_cont3 = html.Div([
    dmc.Skeleton(
        visible=False,
        children=dmc.Container(
            id="skeleton-graph-container3",
            children=dash.dcc.Graph(),
            style={'padding': 0},

        ),
    ), ], style=style_cont2)

temp_cont4 = html.Div([
    dmc.Skeleton(
        visible=False,
        children=dmc.Container(
            id="skeleton-graph-container4",
            children=dash.dcc.Graph(),
            style={'padding': 0},
        ),
    ), ], style=style_cont3)

row2 = html.Tr(
    [
        html.Td(
            temp_cont1,
            style={"padding": 0}
        ),
        html.Td(
            temp_cont2,
            style={"padding": 0}
        ),
    ], style={"padding": 0}
)

# row3 = html.Tr([html.Td("Barium"), html.Td("Barium")])
row4 = html.Tr(
    [
        html.Td(
            temp_cont3,
            style={"padding": 0}
        ),
        html.Td(
            temp_cont4,
            style={"padding": 0}
        )
    ],
    style={'padding': 0},

)

# row5 = html.Tr([html.Td("5")], style={"padding": 0})
body1 = [html.Tbody([row1])]

body = [html.Tbody([row2, row4])]

table_layout = html.Table(body, style={'border': 'none !important', })

table_layout1 = dmc.Table(body1,
                          withColumnBorders=True,
                          withBorder=True,
                          # style={"border-left": "solid #eee 1px"},
                          #   style={"padding-top": -25, "margin-top": -25,
                          #          "padding-left": -25, "margin-left": -25,
                          #          "padding-right": -150, "margin-right": -150},
                          style={
                              "height": "150%",
                              'width': "100%",
                              "justify-content": "center",
                              "align-items": "center",
                              "text-align": "center",
                              "vertical-align": "center",
                          }
                          )

switch_darkTheme = dmc.Switch(
    id="dark-switch",
    offLabel=DashIconify(icon="radix-icons:sun", width=20),
    onLabel=DashIconify(icon="radix-icons:moon", width=20),
    size="lg",
)

method_description = dmc.Text(
    """This web-app is designed to forecasts
      future electricity prices based on market fundamentals using 
      a combination of fundamental market modeling, inverse optimization
       techniques, and machine learning. The model is calibrated 
       with machine learning to align with real market conditions 
       and can handle noisy price data and operational complexities 
       in the electricity sector. The ultimate goal is to compute 
       contract prices for Power Purchase Agreements
     (PPAs) to assist large industrial consumers in meeting their
      sustainability targets.""",
    size="xs",
    color="dimmed",
    mt=50,
    style={
        "text-align": "justify",
        "text-justify": "inner-word"
    }
)

drawer = html.Div(
    [
        dmc.Button("Advanced setting", id="drawer-demo-button"),
        dmc.Drawer(
            html.Div(children=[

                textinput_session,
                text_select_session,
                list_sessions
            ]),
            title="Advanced setting",
            id="drawer-simple",
            padding="md",
            zIndex=10000,
        ),
    ]
)

header = dmc.Header(
    height=60,
    children=
    [
        dmc.Grid(
            children=
            [
                dmc.Col(
                    dmc.Text(
                        "Power Price App",
                        ml=50,
                        mt=10,
                        color="blue",
                    ),
                    span=4,
                    style=
                    {"text-align": "left"},
                ),
                dmc.Col(
                    html.A(),
                    span=4,
                ),
                dmc.Col(
                    html.Img(
                        src=app.get_asset_url("cave-lux-logo.png"),
                        style={
                            "max-width": 150,
                            "text-align": "right",
                            "margin-right": 50,
                        }
                    ),
                    span=4,
                    style=
                    {"text-align": "right", }),
            ],
            style={"border": "none !important"},
        )],

)

modal_confirm_solve = dmc.Modal(
    title="Good news",
    id="modal-simple",
    zIndex=10000,
    children=[
        dmc.Text("The simulation is successfully finished!"),
        dmc.Space(h=20),
        dmc.Group(
            [
                dmc.Button("OK", id="modal-submit-button"),
            ],
            position="right",
        ),
    ],
)

container_app = dmc.Paper(

    dmc.Grid(

        children=
        [

            dmc.Col(header, style={"padding-bottom": 0, "margin-bottom": 0,
                                   # "box-shadow": "rgba(0, 0, 0, 0.1) 0px 10px 15px -3px, rgba(0, 0, 0, 0.05) 0px 4px 6px -2px",
                                   }, span=12),
            dmc.Col(
                table_layout1,
                span=12,
                style={"padding-bottom": 20, "padding-top": 0, "margin": 0},
            ),

            dmc.Col(
                children=dmc.LoadingOverlay(
                    dmc.Stack(
                        id="loading-form",
                        children=[

                            accordion_controls,
                            dmc.Button(
                                "Start", id="load-button", variant="outline", fullWidth=True, style=style_sh,
                            ),
                            switch_darkTheme,
                            method_description,
                            dmc.Text("This work is licensed under [creative commons license].", underline=True,
                                     size="xs",
                                     mt=20, mb=20),
                            drawer,
                        ],
                    ),
                ),
                span="auto",
                style=style_cont,
            ),
            # dmc.Grid(children=
            #         [dmc.Col(temp_cont1, span=4),
            # dmc.Col(temp_cont2, span=4),
            # dmc.Col(temp_cont3, span=4),]),
            dmc.Col([table_layout], span=8, ),
        ],
        # gutter="xl",
        style={"padding-top": 0, "margin-top": 0}
    ),
    # fluid=True,
    # px="xl",

    id="skeleton-loading"
)

# print(dmc.theme.DEFAULT_COLORS)

app.layout = dmc.MantineProvider(
    id="theme-app",
    children=[modal_confirm_solve, container_app],
    withGlobalStyles=True,
    inherit=True,
    withNormalizeCSS=True,
    theme={
        "colorScheme": "light",
    },

    # theme={"colorScheme": "dark",
    #            "fontFamily": "Roboto"},
)


@callback(
    Output('theme-app', 'theme'),
    Output("skeleton-graph-container1", "children"),
    Output("skeleton-graph-container2", "children"),
    Output("skeleton-graph-container3", "children"),
    Output("skeleton-graph-container4", "children"),
    Output("loading-form", "children"),
    Input('theme-app', 'theme'),
    Input("skeleton-loading", "n_clicks"),
    Input("dark-switch", "checked"),
    Input("load-button", "n_clicks"),
    prevent_intial_call=True
)
def update_graph(theme, n_clicks1, isThemeDark, n_clicks2):
    if isThemeDark:
        theme.update({'colorScheme': 'dark'})
    else:
        theme.update({'colorScheme': 'light'})

    df = px.data.gapminder()
    figM = px.choropleth(df, locations="iso_alpha",
                         hover_name="country",  # column to add to hover information
                         color_continuous_scale=px.colors.sequential.Plasma, )
    figM.update_geos(
        visible=True, resolution=110, scope="europe",
        showcountries=True, countrycolor="Black",
        showsubunits=True, subunitcolor="Blue",
        showframe=False, fitbounds=False,
        bgcolor='rgba(0,0,0,0)',
        # projection_scale=1,
        # domain_row=100,

    )
    figM.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                       autosize=True,
                       legend={'visible': False},
                       plot_bgcolor='rgba(0,0,0,0)',
                       paper_bgcolor='rgba(0,0,0,0)',
                       mapbox_style="open-street-map",
                       )

    df = px.data.stocks()  # iris is a pandas DataFrame
    fig = px.area(df, x='date', y="GOOG")
    fig.update_layout(
        margin=dict(l=0, r=5, b=50, t=10),
        yaxis={'ticklabelposition': 'inside', 'showgrid': False},
        xaxis={'ticklabelposition': 'inside', 'showgrid': False},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        autosize=True,
        legend={'visible': False})

    dfx = px.data.iris()  # iris is a pandas DataFrame
    figx = px.scatter(dfx, x="sepal_width", y="sepal_length", color="species", )
    figx.update_layout(
        margin=dict(l=0, r=5, b=50, t=10),
        yaxis={'ticklabelposition': 'inside', 'showgrid': False},
        xaxis={'ticklabelposition': 'inside',
               'showgrid': False
               },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend={'visible': False})

    dfy = px.data.iris()  # iris is a pandas DataFrame
    figy = px.scatter(dfy, x="sepal_width", y="sepal_length", color="species", )
    figy.update_layout(
        margin=dict(l=0, r=5, b=50, t=10),
        yaxis={'ticklabelposition': 'inside', 'showgrid': False},
        xaxis={'ticklabelposition': 'inside',
               'showgrid': False
               },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend={'visible': False})

    fig1 = dash.dcc.Graph(figure=figM,
                          # config={'responsive': True},
                          # style={
                          #     "width": "100px",
                          # },
                          # responsive=True
                          )
    fig2 = dash.dcc.Graph(figure=fig,
                          # config={'responsive': True},
                          # style={
                          #     "width": "100px",
                          # },
                          # responsive=True
                          )
    fig3 = dash.dcc.Graph(figure=figx,
                          # config={'responsive': True},
                          # style={
                          #     "width": "100px",
                          # },
                          # responsive=True
                          )
    fig4 = dash.dcc.Graph(figure=figy,
                          # config={'responsive': True},
                          # style={
                          #     "width": "100px",
                          # },
                          # responsive=True
                          )
    time.sleep(1)
    return theme, fig1, fig2, fig3, fig4, dash.no_update


@callback(
    Output("drawer-simple", "opened"),
    Input("drawer-demo-button", "n_clicks"),
    prevent_initial_call=True,
)
def drawer_demo(n_clicks):
    return True


# @callback(
#     Output("loading-form", "children"),
#     Input("load-button", "n_clicks"),
#     prevent_initial_call=True,
# )
# def func(n_clicked):
#     time.sleep(2)
#     return dash.no_update


@callback(
    Output("modal-simple", "opened"),
    Input("load-button", "n_clicks"),
    Input("modal-submit-button", "n_clicks"),
    State("modal-simple", "opened"),
    prevent_initial_call=True,
)
def func(nc1, nc2, opened):
    time.sleep(1)
    return not opened


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)
