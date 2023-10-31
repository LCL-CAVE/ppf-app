import time

import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc
from dash import html
import numpy as np
from dash.dependencies import Input, Output, State
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import datasets
from sklearn.svm import SVC

import utils.figures as figs

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
    external_stylesheets=[dbc.themes.ZEPHYR]
)
app.title = "Support Vector Machine"
server = app.server


def generate_data(n_samples, dataset, noise):
    if dataset == "moons":
        return datasets.make_moons(n_samples=n_samples, noise=noise, random_state=0)

    elif dataset == "circles":
        return datasets.make_circles(
            n_samples=n_samples, noise=noise, factor=0.5, random_state=1
        )

    elif dataset == "linear":
        X, y = datasets.make_classification(
            n_samples=n_samples,
            n_features=2,
            n_redundant=0,
            n_informative=2,
            random_state=2,
            n_clusters_per_class=1,
        )

        rng = np.random.RandomState(2)
        X += noise * rng.uniform(size=X.shape)
        linearly_separable = (X, y)

        return linearly_separable

    else:
        raise ValueError(
            "Data type incorrectly specified. Please choose an existing dataset."
        )


header = html.Div(
    dbc.Container(
        [
            html.Img(src=app.get_asset_url("cave-lux-logo.png"), className="mx-auto"),
            html.H4(
                "Support Vector Clustering App",
                # className="lead",
            ),
        ],
        fluid=True,
        # className="py-3",
    ),
    className="text-white p-2 mb-2",
)

# header = html.Div(
#     children=[
#         # Change App Name here
#         html.H4(
#             children=[
#                 html.A(
#                     "Support Vector Machine App",
#                 )
#             ],
#         ),
#         html.A(
#             children=[
#                 html.Img(src=app.get_asset_url("cave-lux-logo.png"))
#             ],
#             href="https://cave.daloos.uni.lu/",
#         ),
#     ],
#     className="bg-primary text-white p-2 mb-2")


dropdown_dataset = html.Div(
    [
        dbc.Label("Select Dataset"),
        dcc.Dropdown(options=[
            {"label": "Moons", "value": "moons"},
            {
                "label": "Linearly Separable",
                "value": "linear",
            },
            {
                "label": "Circles",
                "value": "circles",
            },
        ],
            clearable=False,
            value="moons",
            id="dropdown-select-dataset", )
    ],
    className="pb-3 m-4",
)

slider_sample_size = html.Div(
    [
        dbc.Label("Sample Size"),
        dmc.Slider(
            id="slider-dataset-sample-size",
            min=100,
            max=500,
            step=100,
            # marks={
            #     str(i): str(i)
            #     for i in [100, 200, 300, 400, 500]
            # },
            value=300,
            # marks=None,
            # mb=35,
            # tooltip={"placement": "bottom", "always_visible": True},
            # className="p-0",
        ),
    ],
    className="pb-3",
)

slider_noise_level = html.Div(
    [
        dbc.Label("Noise Level"),
        dcc.Slider(
            id="slider-dataset-noise-level",
            min=0,
            max=1,
            # marks={
            #     i / 10: str(i / 10)
            #     for i in range(0, 11, 2)
            # },
            step=0.1,
            marks=None,
            value=0.2,
            tooltip={"placement": "bottom", "always_visible": True},
            className="p-0",
        ),
    ],
    className="pb-3 m-4",
)

accordion_control = dmc.Accordion(
    children=[
        dmc.AccordionItem(
            [
                dmc.AccordionControl("Customization"),
                dmc.AccordionPanel(
                    slider_sample_size,
                ),
            ],
            value="customization",
        ),
        dmc.AccordionItem(
            [
                dmc.AccordionControl("Flexibility"),
                dmc.AccordionPanel(
                    "Configure temp appearance and behavior with vast amount of settings or overwrite any part of "
                    "component styles "
                ),
            ],
            value="flexibility",
        ),
    ],
)

slider_threshold = html.Div(
    [
        dbc.Label("Threshold"),
        dcc.Slider(
            id="slider-threshold",
            min=0,
            max=1,
            value=0.5,
            step=0.01,
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
            className="p-0",
        ),
    ],
    className="pb-3 m-4",
)

dropdown_kernel = html.Div(
    [
        dbc.Label("Select Kernel"),
        dcc.Dropdown(id="dropdown-svm-parameter-kernel",
                     options=[
                         {
                             "label": "Radial basis function (RBF)",
                             "value": "rbf",
                         },
                         {"label": "Linear", "value": "linear"},
                         {
                             "label": "Polynomial",
                             "value": "poly",
                         },
                         {
                             "label": "Sigmoid",
                             "value": "sigmoid",
                         },
                     ],
                     value="rbf",
                     clearable=False,
                     )
    ],
    className="pb-3 m-4",
)

slider_cost = html.Div(
    [
        dbc.Label("Cost"),
        dcc.Slider(
            id="slider-svm-parameter-C-power",
            min=-2,
            max=4,
            value=0,
            marks=None,
            # marks={
            #     i: "{}".format(10 ** i)
            #     for i in range(-2, 5)
            # },
            tooltip={"placement": "bottom", "always_visible": True},
            className="p-0",
        ),
    ],
    className="pb-3 m-4",
)

slider_cost_coef = html.Div(
    [
        dcc.Slider(
            id="slider-svm-parameter-C-coef",
            min=1,
            max=9,
            value=1,
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
            className="p-0",
        ),
    ],
    className="pb-3 m-4",
)

slider_degree = html.Div(
    [
        dbc.Label("Degree"),
        dcc.Slider(
            id="slider-svm-parameter-degree",
            min=2,
            max=10,
            value=3,
            step=1,
            marks=None,
            # marks={
            #     str(i): str(i) for i in range(2, 11, 2)
            # },
            tooltip={"placement": "bottom", "always_visible": True},
            className="p-0",
        ),
    ],
    className="pb-3 m-4",
)

slider_gamma = html.Div(
    [
        dbc.Label("Gamma"),
        dcc.Slider(
            id="slider-svm-parameter-gamma-power",
            min=-5,
            max=0,
            value=-1,
            marks=None,
            # marks={
            #     i: "{}".format(10 ** i)
            #     for i in range(-5, 1)
            # },
            tooltip={"placement": "bottom", "always_visible": True},
            className="p-0",
        ),
    ],
    className="pb-3 m-4",
)

slider_gamma_coef = html.Div(
    [
        dcc.Slider(
            id="slider-svm-parameter-gamma-coef",
            min=1,
            max=9,
            value=5,
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
            className="p-0",
        ),
    ],
    className="pb-3 m-4",
)

radio_shrinking = html.Div(
    [
        dbc.Label("Shrinking"),
        dbc.RadioItems(
            id="radio-svm-parameter-shrinking",
            options=[
                {
                    "label": " Enabled",
                    "value": "True",
                },
                {
                    "label": " Disabled",
                    "value": "False",
                },
            ],
            value="True",
            inline=True,
        )
    ],
    className="pb-3 m-4",
)

controls = dbc.Card(
    [accordion_control, dropdown_dataset, slider_sample_size, slider_noise_level, slider_threshold, dropdown_kernel,
     slider_cost,
     slider_cost_coef, slider_degree, slider_gamma, slider_gamma_coef, radio_shrinking],
    body=True,
)

# tab1 = dbc.Tab([html.Div(id="div-graphs")], label="Performance Charts", className="p-4")
tab2 = dbc.Tab([dcc.Graph(id="graph-sklearn-svm")], label="Clustering Chart", className="p-4")
tab3 = dbc.Tab([dcc.Graph(id="graph-line-roc-curve")], label="ROC Curve", className="p-4")
tab4 = dbc.Tab([dcc.Graph(id="graph-pie-confusion-matrix")], label="Confusion Matrix", className="p-4")
# tab3 = dbc.Tab([table], label="Table", className="p-4")
tabs = dbc.Card(dbc.Tabs([tab2, tab3, tab4]))

app.layout = dbc.Container(
    [
        header,
        dbc.Row(
            [
                dbc.Col(
                    [
                        controls,
                    ],
                    width=4,
                ),
                dbc.Col([tabs], width=8),
            ]
        ),
    ],
    fluid=True,
    className="dbc p-4 m-4",
)


@app.callback(
    Output("slider-svm-parameter-gamma-coef", "marks"),
    [Input("slider-svm-parameter-gamma-power", "value")],
)
def update_slider_svm_parameter_gamma_coef(power):
    scale = 10 ** power
    return {i: str(round(i * scale, 8)) for i in range(1, 10, 2)}


@app.callback(
    Output("slider-svm-parameter-C-coef", "marks"),
    [Input("slider-svm-parameter-C-power", "value")],
)
def update_slider_svm_parameter_C_coef(power):
    scale = 10 ** power
    return {i: str(round(i * scale, 8)) for i in range(1, 10, 2)}


# @app.callback(
#     Output("slider-threshold", "value"),
#     [Input("button-zero-threshold", "n_clicks")],
#     [State("graph-sklearn-svm", "figure")],
# )
# def reset_threshold_center(n_clicks, figure):
#     if n_clicks:
#         Z = np.array(figure["data"][0]["z"])
#         value = -Z.min() / (Z.max() - Z.min())
#     else:
#         value = 0.4959986285375595
#     return value


# Disable Sliders if kernel not in the given list
@app.callback(
    Output("slider-svm-parameter-degree", "disabled"),
    [Input("dropdown-svm-parameter-kernel", "value")],
)
def disable_slider_param_degree(kernel):
    return kernel != "poly"


@app.callback(
    Output("slider-svm-parameter-gamma-coef", "disabled"),
    [Input("dropdown-svm-parameter-kernel", "value")],
)
def disable_slider_param_gamma_coef(kernel):
    return kernel not in ["rbf", "poly", "sigmoid"]


@app.callback(
    Output("slider-svm-parameter-gamma-power", "disabled"),
    [Input("dropdown-svm-parameter-kernel", "value")],
)
def disable_slider_param_gamma_power(kernel):
    return kernel not in ["rbf", "poly", "sigmoid"]


@app.callback(
    Output("graph-sklearn-svm", "figure"),
    Output("graph-line-roc-curve", "figure"),
    Output("graph-pie-confusion-matrix", "figure"),
    [
        Input("dropdown-svm-parameter-kernel", "value"),
        Input("slider-svm-parameter-degree", "value"),
        Input("slider-svm-parameter-C-coef", "value"),
        Input("slider-svm-parameter-C-power", "value"),
        Input("slider-svm-parameter-gamma-coef", "value"),
        Input("slider-svm-parameter-gamma-power", "value"),
        Input("dropdown-select-dataset", "value"),
        Input("slider-dataset-noise-level", "value"),
        Input("radio-svm-parameter-shrinking", "value"),
        Input("slider-threshold", "value"),
        Input("slider-dataset-sample-size", "value"),
    ],
)
def update_svm_graph(
        kernel,
        degree,
        C_coef,
        C_power,
        gamma_coef,
        gamma_power,
        dataset,
        noise,
        shrinking,
        threshold,
        sample_size,
):
    t_start = time.time()
    h = 0.3  # step size in the mesh

    # Data Pre-processing
    X, y = generate_data(n_samples=sample_size, dataset=dataset, noise=noise)
    X = StandardScaler().fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.4, random_state=42
    )

    x_min = X[:, 0].min() - 0.5
    x_max = X[:, 0].max() + 0.5
    y_min = X[:, 1].min() - 0.5
    y_max = X[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    C = C_coef * 10 ** C_power
    gamma = gamma_coef * 10 ** gamma_power

    if shrinking == "True":
        flag = True
    else:
        flag = False

    # Train SVM
    clf = SVC(C=C, kernel=kernel, degree=degree, gamma=gamma, shrinking=flag)
    clf.fit(X_train, y_train)

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].
    if hasattr(clf, "decision_function"):
        Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    else:
        Z = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]

    prediction_figure = figs.serve_prediction_plot(
        model=clf,
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
        Z=Z,
        xx=xx,
        yy=yy,
        mesh_step=h,
        threshold=threshold,
    )

    roc_figure = figs.serve_roc_curve(model=clf, X_test=X_test, y_test=y_test)

    confusion_figure = figs.serve_pie_confusion_matrix(
        model=clf, X_test=X_test, y_test=y_test, Z=Z, threshold=threshold
    )

    return prediction_figure, roc_figure, confusion_figure


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)
