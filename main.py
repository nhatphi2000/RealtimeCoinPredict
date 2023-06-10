import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from train import get_train_data
from crypto_data import get_formatted_coin_list
from dash.dependencies import Input, Output

app = dash.Dash()
server = app.server
# Example usage

train = get_train_data("bitcoin")
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
                        options=[
                            {"label": "BTC", "value": "bitcoin"},
                            {"label": "ETH", "value": "ethereum"},
                            {"label": "ADA", "value": "cardano"}
                        ],
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
                            title='Scatter Plot',
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
                                x=train.index,
                                y=train["Close"],
                                mode='lines+markers',
                                name="Close Price",
                            )
                        ],
                        "layout": go.Layout(
                            title='Scatter Plot',
                            xaxis={'title': 'Date'},
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
    [Input("coin-dropdown", "value")]
)
def update_graphs(coin):
    train = get_train_data(coin)

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
                x=train.index,
                y=train["Close"],
                mode='lines+markers',
                name="Close Price",
            )
        ],
        "layout": go.Layout(
            title='Predicted Closing Price',
            xaxis={'title': 'Date'},
            yaxis={'title': 'Closing Rate (USD)'}
        )
    }

    return actual_figure, predict_figure


if __name__=='__main__':
    app.run_server(debug=True)