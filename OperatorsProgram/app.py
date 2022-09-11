from dash import Dash, dash_table, html
import pandas as pd
import plotly.express as px
from datetime import date, time, datetime

today = '07-09-2022'
today_real = date.today()
FILEPATH = 'PHNX_FM_PHNX_MOBC_Status_Beacon'
external_stylesheets = ['style2.css']

datapds = pd.read_csv(f'{FILEPATH}-{today}.csv')

app = Dash(__name__,external_stylesheets=external_stylesheets)

app.layout = html.Div(
                dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in datapds.columns],
                    data=datapds.to_dict('records'),
                    editable = True,
                    row_selectable='multi',
                    #row_deletable=True,
                    #fixed_columns={ 'headers': True, 'data': 1 },
                    style_cell={'textAlign': 'center'},
                    style_table={
                                'overflowX': 'scroll',
                                'minWidth': '100%',
                                'padding-bottom': '10px',},
                ),
                style={'padding': '30px'}
            )
if __name__ == '__main__':
    app.run_server(debug=True)