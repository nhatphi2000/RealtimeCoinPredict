import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from crypto_data import get_formatted_coin_list
from predict_data import predictLSTM
from dash.dependencies import Input, Output

app = dash.Dash()
server = app.server
# Example usage

train, valid, predict, df = predictLSTM("bitcoin")
coinList=get_formatted_coin_list() #lay danh sach coin, tuy nhien bi gioi han lan get api




app.layout = html.Div([
    html.H1("Stock Price Analysis Dashboard", style={"textAlign": "center"}),

    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Bitcoin USD Stock Data', children=[
            html.Div([
                html.H2("Actual BTC closing price", style={"textAlign": "center"}),

                html.Div([
                    html.Label("Select a coin:"),
                    dcc.Dropdown(
                        id="coin-dropdown",
                        options=coinList,
                        value="bitcoin"
                    )
                ], style={"margin-bottom": "20px"}),

                dcc.Graph(
                    id="actual-graph",
                    figure={
                        "data": [
                            go.Scatter(
                                x=train.index,
                                y=train["Close"],
                                mode='lines+markers',
                                name="Close Price",
                            )
                        ],
                        "layout": go.Layout(
                            title='Actual Closing Price',
                            xaxis={'title': 'Date'},
                            yaxis={'title': 'Closing Rate (USD)'}
                        )
                    }
                ),
                 dcc.Graph(
                    id="predict-graph",
                    figure={
                        "data": [
                            go.Scatter(
                                x=valid.index,
                                y=valid["Close"],
                                mode='lines+markers',
                                line=dict(color="#0000ff"),
                                name="Close Price",
                            ),
                            go.Scatter(
                                x=valid.index,
                                y=valid["Predictions"],
                                mode='lines+markers',
                                line=dict(color="#ffe476"),
                                name="Predictions Price"
                            )
                        ],
                        "layout": go.Layout(
                            title='Comparision Predicted Closing Price',
                            xaxis={'title': 'Date'},
                            yaxis={'title': 'Closing Rate (USD)'}
                        )
                    }
                ),
                 dcc.Graph(
                    id="next-predict-graph",
                    figure={
                        "data": [
                            go.Bar(
                                x=["LSTM"],
                                y=predict["Predictions"],
                                name="LSTM",
                                width=0.5
                            )
                        ],
                        "layout": go.Layout(
                            title='Predicted Next Day Closing Price',
                            xaxis={'title': 'Bar Name'},
                            yaxis={'title': 'Closing Rate (USD)'}
                        )
                    }
                ),
            ])
        ]),
    ])
])

@app.callback(
    Output("actual-graph", "figure"),
    Output("predict-graph", "figure"),
    Output("next-predict-graph", "figure"),
    [Input("coin-dropdown", "value")]
)
def update_graphs(coin):
    train, valid, predict, df = predictLSTM(coin)

    actual_figure = {
        "data": [
            go.Scatter(
                x=train.index,
                y=train["Close"],
                mode='lines+markers',
                name="Close Price",
            )
        ],
        "layout": go.Layout(
            title='Actual Closing Price',
            xaxis={'title': 'Date'},
            yaxis={'title': 'Closing Rate (USD)'}
        )
    }

    predict_figure = {
        "data": [
            go.Scatter(
                x=valid.index,
                y=valid["Close"],
                mode='lines+markers',
                name="Close Price",
            ),
            go.Scatter(
                x=valid.index,
                y=valid["Predictions"],
                mode='lines+markers',
                name="Predictions Price",
            ),
        ],
        "layout": go.Layout(
            title='Comparision Predicted Closing Price',
            xaxis={'title': 'Date'},
            yaxis={'title': 'Closing Rate (USD)'}
        )
    }

    next_predict_figure = {
        "data": [
            go.Bar(
                x=["LSTM"],
                y=predict["Predictions"],
                name="LSTM",
                width=0.5
            )
        ],
        "layout": go.Layout(
            title='Predicted Next Day Closing Price',
            xaxis={'title': 'Bar Name'},
            yaxis={'title': 'Closing Rate (USD)'}
        )
    }

    return actual_figure, predict_figure, next_predict_figure


if __name__=='__main__':
    app.run_server(debug=True)