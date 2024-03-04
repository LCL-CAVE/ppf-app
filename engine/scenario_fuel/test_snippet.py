from engine.scenario_fuel.eng_read_scenario_fuel import serve_read_scenario_fuel
from utils.fig_multiple_scatter import serve_fig_multiple_scatter
import plotly.express as px

fuelType = 'coal'  # can be 'gas', 'coal', or 'carbon'
initialFuelPrice = 75  # Euro
growthRate = 0.2
START_DATE_FUTURE = "2024-01-01 00:00"
END_DATE_FUTURE = "2030-01-01 00:00"

df = serve_read_scenario_fuel(fuelType, initialFuelPrice, growthRate, START_DATE_FUTURE, END_DATE_FUTURE)

# fig = px.scatter(df, x="timestamp", y="value")
fig = serve_fig_multiple_scatter(df, "D", "Coal Price")

fig.show()
