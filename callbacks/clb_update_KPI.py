import numpy as np

# @app.callback(Output('text_kpi_avg_capture_price', 'children'),
#               Output('text_kpi_avg_production', 'children'),
#               Output('text_kpi_avg_price', 'children'),
#               Input('interval-component', 'n_intervals'))
# def update_kpi(n):
#     return str(np.round(50 + 10 * np.random.rand(), 2)) + " euro", str(
#         np.round(7400 + 300 * np.random.rand(), 2)) + " GW/h", str(np.round(50 + 10 * np.random.rand(), 2)) + " euro"