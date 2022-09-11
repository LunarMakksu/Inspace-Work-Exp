import time
import pathlib
import os

import pandas as pd
from dash import dash, dcc, html
from dash.dependencies import State, Input, Output
import dash_daq as daq

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
app.title = "Inspace Information Dashboard"
# This is for gunicorn
server = app.server

# Mapbox
MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"
MAPBOX_STYLE = "mapbox://styles/plotlymapbox/cjyivwt3i014a1dpejm5r7dwr"

# Dash_DAQ elements

utc = html.Div(
    id="control-panel-utc",
    children=[
        daq.LEDDisplay(
            id="control-panel-utc-component",
            value="16:23",
            label="Time",
            size=40,
            color="#fec036",
            backgroundColor="#2b2b2b",
        )
    ],
    n_clicks=0,
)

mag_indicator = html.Div(
    id="control-panel-magnetometer",
    children=[
        daq.GraduatedBar(
            id="control-panel-magnetometer-component",
            label="Magnetometer Level",
            min=0,
            max=100,
            value=76,
            step=1,
            showCurrentValue=True,
            color="#fec036",
        )
    ],
    n_clicks=0,
)

speed = html.Div(
    id="control-panel-speed",
    children=[
        daq.Gauge(
            id="control-panel-speed-component",
            label="Speed",
            min=0,
            max=40,
            showCurrentValue=True,
            value=27.859,
            size=175,
            units="1000km/h",
            color="#fec036",
        )
    ],
    n_clicks=0,
)

elevation = html.Div(
    id="control-panel-elevation",
    children=[
        daq.Tank(
            id="control-panel-elevation-component",
            label="Elevation",
            min=0,
            max=1000,
            value=650,
            units="kilometers",
            showCurrentValue=True,
            color="#303030",
        )
    ],
    n_clicks=0,
)

temperature = html.Div(
    id="control-panel-temperature",
    children=[
        daq.Tank(
            id="control-panel-temperature-component",
            label="Temperature",
            min=0,
            max=500,
            value=290,
            units="Kelvin",
            showCurrentValue=True,
            color="#303030",
        )
    ],
    n_clicks=0,
)

battery_indicator = html.Div(
    id="control-panel-battery-generation",
    children=[
        daq.GraduatedBar(
            id="control-panel-power-generation-component",
            label="Battery-generation",
            min=0,
            max=100,
            value=85,
            step=0.01,
            showCurrentValue=True,
            color="#fec036",
        )
    ],
    n_clicks=0,
)

longitude = html.Div(
    id="control-panel-longitude",
    children=[
        daq.LEDDisplay(
            id="control-panel-longitude-component",
            value="0000.0000",
            label="Longitude",
            size=24,
            color="#fec036",
            style={"color": "#black"},
            backgroundColor="#2b2b2b",
        )
    ],
    n_clicks=0,
)

latitude = html.Div(
    id="control-panel-latitude",
    children=[
        daq.LEDDisplay(
            id="control-panel-latitude-component",
            value="0050.9789",
            label="Latitude",
            size=24,
            color="#fec036",
            style={"color": "#black"},
            backgroundColor="#2b2b2b",
        )
    ],
    n_clicks=0,
)

#solar_panel_0 = daq.Indicator(
    #className="panel-lower-indicator",
    #id="control-panel-solar-panel-0",
    #label="Solar-Panel-0",
    #labelPosition="bottom",
    #value=True,
    #color="#fec036",
    #style={"color": "#black"},
#)

#solar_panel_1 = daq.Indicator(
    #className="panel-lower-indicator",
    #id="control-panel-solar-panel-1",
    #label="Solar-Panel-1",
    #labelPosition="bottom",
    #value=True,
    #color="#fec036",
    #style={"color": "#black"},
#)

#camera = daq.Indicator(
    #className="panel-lower-indicator",
    #id="control-panel-camera",
    #label="Camera",
    #labelPosition="bottom",
    #value=True,
    #color="#fec036",
    #style={"color": "#black"},
#)

#thrusters = daq.Indicator(
    #className="panel-lower-indicator",
    #id="control-panel-thrusters",
    #label="Thrusters",
    #labelPosition="bottom",
    #value=True,
    #color="#fec036",
    #style={"color": "#black"},
#)

#motor = daq.Indicator(
    #className="panel-lower-indicator",
    #id="control-panel-motor",
    #label="Motor",
    #labelPosition="bottom",
    #value=True,
    #color="#fec036",
    #style={"color": "#black"},
#)

communication_signal = daq.Indicator(
    className="panel-lower-indicator",
    id="control-panel-communication-signal",
    label="Signal",
    labelPosition="bottom",
    value=True,
    color="#fec036",
    style={"color": "#black"},
)

map_toggle = daq.ToggleSwitch(
    id="control-panel-toggle-map",
    value=True,
    label=["Hide path", "Show path"],
    color="#ffe102",
    style={"color": "#black"},
)

hourweek_toggle = daq.ToggleSwitch(
    id="control-panel-toggle-minute",
    value=True,
    label=["Past Hour", "Past Week"],
    color="#ffe102",
    style={"color": "#black"},
)

satellite_dropdown = dcc.Dropdown(
    id="satellite-dropdown-component",
    options=[
        {"label": "Faraday-Phoenix", "value": "Faraday-Phoenix"},
        {"label": "Prometheus 2", "value": "Prometheus 2"},
    ],
    clearable=False,
    value="Faraday-Phoenix",
)

app.layout = html.Div(children=[
    html.H1(children='Panel'),

    html.Div(children='''
        Inspace Missions
    '''),
    ],
)

#Satellite location tracker
#flattens map for scaling

def flatten_path(xy1, xy2):
    diff_rate = (xy2 - xy1) / 100
    res_list = []
    for i in range(100):
        res_list.append(xy1 + i * diff_rate)
    return res_list


map_data = [
    {
        "type": "scattermapbox",
        "lat": [0],
        "lon": [0],
        "hoverinfo": "text+lon+lat",
        "text": "Satellite Path",
        "mode": "lines",
        "line": {"width": 2, "color": "#707070"},
    },
    {
        "type": "scattermapbox",
        "lat": [0],
        "lon": [0],
        "hoverinfo": "text+lon+lat",
        "text": "Current Position",
        "mode": "markers",
        "marker": {"size": 10, "color": "#fec036"},
    },
]

map_layout = {
    "mapbox": {
        "accesstoken": MAPBOX_ACCESS_TOKEN,
        "style": MAPBOX_STYLE,
        "center": {"lat": 45},
    },
    "showlegend": False,
    "autosize": True,
    "paper_bgcolor": "#1e1e1e",
    "plot_bgcolor": "#1e1e1e",
    "margin": {"t": 0, "r": 0, "b": 0, "l": 0},
}

map_graph = html.Div(
    id="world-map-wrapper",
    children=[
        map_toggle,
        dcc.Graph(
            id="world-map",
            figure={"data": map_data, "layout": map_layout},
            config={"displayModeBar": False, "scrollZoom": False},
        ),
    ],
)

# Histogram

histogram = html.Div(
    id="histogram-container",
    children=[
        html.Div(
            id="histogram-header",
            children=[
                html.H1(
                    id="histogram-title", children=["Power Generation"]
                ),
                hourweek_toggle,
            ],
        ),
        dcc.Graph(
            id="histogram-graph",
            figure={
                "data": [
                    {
                        "x": [i for i in range(99)], #supposedly miliamps
                        "y": [i for i in range(7)], #past days, up to a week (UTC)
                        "type": "scatter",
                        "marker": {"color": "#fec036"},
                    }
                ],
                "layout": {
                    "margin": {"t": 30, "r": 35, "b": 40, "l": 50},
                    "xaxis": {"dtick": 5, "gridcolor": "#636363", "showline": False},
                    "yaxis": {"showgrid": False},
                    "plot_bgcolor": "#2b2b2b",
                    "paper_bgcolor": "#2b2b2b",
                    "font": {"color": "gray"},
                },
            },
            config={"displayModeBar": False},
        ),
    ],
)

# Control panel + map
main_panel_layout = html.Div(
    id="panel-upper-lower",
    children=[
        dcc.Interval(id="interval", interval=1 * 2000, n_intervals=0),
        map_graph,
        html.Div(
            id="panel",
            children=[
                histogram,
                html.Div(
                    id="panel-lower",
                    children=[
                        html.Div(
                            id="panel-lower-0",
                            children=[elevation, temperature, mag_indicator, speed, utc,]
                        ),
                        html.Div(
                            id="panel-lower-1",
                            children=[
                                html.Div(
                                    id="panel-lower-led-displays",
                                    children=[latitude, longitude],
                                ),
                                #html.Div(
                                   # id="panel-lower-indicators",
                                    #children=[
                                       # html.Div(
                                          #  id="panel-lower-indicators-0",
                                         #   children=[solar_panel_0, thrusters],
                                       # ),
                                       # html.Div(
                                        #    id="panel-lower-indicators-1",
                                        #    children=[solar_panel_1, motor],
                                        #),
                                       # html.Div(
                                        #    id="panel-lower-indicators-2",
                                       #     children=[camera, communication_signal],
                                       # ),
                                   # ],
                               # ),
                                html.Div(
                                    id="panel-lower-graduated-bars",
                                    children=[mag_indicator, battery_indicator],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)

# Data generation

# Pandas
APP_PATH = str(pathlib.Path(__file__).parent.resolve())

# Satellite H45-K1 data
df_non_gps_h_0 = pd.read_csv(
    os.path.join(APP_PATH, os.path.join("dummy_data", "non_gps_data_h_0.csv"))  # _h = week data
)
df_non_gps_m_0 = pd.read_csv(
    os.path.join(APP_PATH, os.path.join("dummy_data", "non_gps_data_m_0.csv"))  #_m = day data
)
df_gps_m_0 = pd.read_csv(
    os.path.join(APP_PATH, os.path.join("dummy_data", "gps_data_m_0.csv"))
)
df_gps_h_0 = pd.read_csv(
    os.path.join(APP_PATH, os.path.join("dummy_data", "gps_data_h_0.csv"))
)

# Satellite L12-5 data
df_non_gps_h_1 = pd.read_csv(
    os.path.join(APP_PATH, os.path.join("dummy_data", "non_gps_data_h_1.csv"))
)
df_non_gps_m_1 = pd.read_csv(
    os.path.join(APP_PATH, os.path.join("dummy_data", "non_gps_data_m_1.csv"))
)
df_gps_m_1 = pd.read_csv(
    os.path.join(APP_PATH, os.path.join("dummy_data", "gps_data_m_1.csv"))
)
df_gps_h_1 = pd.read_csv(
    os.path.join(APP_PATH, os.path.join("dummy_data", "gps_data_h_1.csv"))
)

# Satellite Faraday-Phoenix data


# Root                                                          Fuel is actually magnetometer reading
root_layout = html.Div(
    id="root",
    children=[
        dcc.Store(id="store-placeholder"),
        dcc.Store(
            id="store-data",
            data={
                "day_data_0": {
                    "elevation": [df_non_gps_h_0["elevation"][i] for i in range(60)],
                    "temperature": [
                        df_non_gps_h_0["temperature"][i] for i in range(60)
                    ],
                    "speed": [df_non_gps_h_0["speed"][i] for i in range(60)],
                    "latitude": [
                        "{0:09.4f}".format(df_gps_h_0["lat"][i]) for i in range(60)
                    ],
                    "longitude": [
                        "{0:09.4f}".format(df_gps_h_0["lon"][i]) for i in range(60)
                    ],
                    "fuel": [df_non_gps_h_0["fuel"][i] for i in range(60)],
                    "battery": [df_non_gps_h_0["battery"][i] for i in range(60)],
                },
                "minute_data_0": {
                    "elevation": [df_non_gps_m_0["elevation"][i] for i in range(60)],
                    "temperature": [
                        df_non_gps_m_0["temperature"][i] for i in range(60)
                    ],
                    "speed": [df_non_gps_m_0["speed"][i] for i in range(60)],
                    "latitude": [
                        "{0:09.4f}".format(df_gps_m_0["lat"][i]) for i in range(60)
                    ],
                    "longitude": [
                        "{0:09.4f}".format(df_gps_m_0["lon"][i]) for i in range(60)
                    ],
                    "fuel": [df_non_gps_m_0["fuel"][i] for i in range(60)],
                    "battery": [df_non_gps_m_0["battery"][i] for i in range(60)],
                },
                "hour_data_1": {
                    "elevation": [df_non_gps_h_1["elevation"][i] for i in range(60)],
                    "temperature": [
                        df_non_gps_h_1["temperature"][i] for i in range(60)
                    ],
                    "speed": [df_non_gps_h_1["speed"][i] for i in range(60)],
                    "latitude": [
                        "{0:09.4f}".format(df_gps_h_1["lat"][i]) for i in range(60)
                    ],
                    "longitude": [
                        "{0:09.4f}".format(df_gps_h_1["lon"][i]) for i in range(60)
                    ],
                    "fuel": [df_non_gps_h_1["fuel"][i] for i in range(60)],
                    "battery": [df_non_gps_h_1["battery"][i] for i in range(60)],
                },
                "minute_data_1": {
                    "elevation": [df_non_gps_m_1["elevation"][i] for i in range(60)],
                    "temperature": [
                        df_non_gps_m_1["temperature"][i] for i in range(60)
                    ],
                    "speed": [df_non_gps_m_1["speed"][i] for i in range(60)],
                    "latitude": [
                        "{0:09.4f}".format(df_gps_m_1["lat"][i]) for i in range(60)
                    ],
                    "longitude": [
                        "{0:09.4f}".format(df_gps_m_1["lon"][i]) for i in range(60)
                    ],
                    "fuel": [df_non_gps_m_1["fuel"][i] for i in range(60)],
                    "battery": [df_non_gps_m_1["battery"][i] for i in range(60)],
                },
            },
        ),
        # For the case no components were clicked, we need to know what type of graph to preserve
        dcc.Store(id="store-data-config", data={"info_type": "", "satellite_type": 0}),
        #side_panel_layout,
        main_panel_layout,
    ],
)

app.layout = root_layout






if __name__ == "__main__":
    app.run_server(debug=True)
