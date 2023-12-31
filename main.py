import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from crypto_data import get_formatted_coin_list
from predict_data import predictLSTM
from predict_data_RNN import predict_RNN
from predict_data_XGboost import predict_XGboost
from dash.dependencies import Input, Output

app = dash.Dash()
server = app.server
# Example usage

train, valid, predict, df = predictLSTM("bitcoin","Close")
trainRNN, validRNN, predictRNN, dfRNN = predict_RNN("bitcoin","Close")
trainXGboost, validXGboost, predictXGboost, dfXGboost = predict_XGboost("bitcoin","Close")
coinList=get_formatted_coin_list() #lay danh sach coin, tuy nhien bi gioi han lan get api




app.layout = html.Div([
    html.H1("Stock Price Analysis Dashboard", style={"textAlign": "center"}),

    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label="Actual Coin closing price", children=[
            html.Div([

                html.Div([
                    html.Label("Select a coin and type:"),
                    dcc.Dropdown(
                        id="coin-dropdown",
                        options=coinList,
                        value="bitcoin"
                    ),
                     dcc.Dropdown(
                        id="type-dropdown",
                        options=[
                                    {'label': 'Close Price', 'value': 'Close'},
                                    {'label': 'Rate of Change', 'value': 'ROC'},
                                ],
                        value="Close"
                    )
                ], style={"margin-bottom": "20px"}),

                dcc.Loading(
                    id="loading-graphs",
                    type="circle",
                     children=[
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
                                        line=dict(color="orange"),
                                        name="LSTM Predictions Price"
                                    ),
                                    go.Scatter(
                                        x=validRNN.index,
                                        y=validRNN["Predictions"],
                                        mode='lines+markers',
                                        line=dict(color="green"),
                                        name="RNN Predictions Price"
                                    ),
                                     go.Scatter(
                                        x=validXGboost.index,
                                        y=validXGboost["Predictions"],
                                        mode='lines+markers',
                                        line=dict(color="purple"),
                                        name="XGboost Predictions Price"
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
                                        marker=dict(color="orange")
                                    ),
                                    go.Bar(
                                        x=["RNN"],
                                        y=predictRNN["Predictions"],
                                        name="RNN",
                                        marker=dict(color="green")
                                    ),
                                    go.Bar(
                                        x=["XGboost"],
                                        y=predictXGboost["Predictions"],
                                        name="XGboost",
                                        marker=dict(color="purple")
                                    )
                                ],
                                "layout": go.Layout(
                                    title='Predicted Next Day Closing Price',
                                    xaxis={'title': 'Bar Name'},
                                    yaxis={'title': 'Closing Rate (USD)'}
                                )
                            }
                        ), 
                     ]
                ),
            ])
        ]),
    ])
])

@app.callback(
    Output("actual-graph", "figure"),
    Output("predict-graph", "figure"),
    Output("next-predict-graph", "figure"),
    [Input("coin-dropdown", "value"),Input("type-dropdown", "value")]
)
def update_graphs(coin,type):
    train, valid, predict, df = predictLSTM(coin,type)
    trainRNN, validRNN,predictRNN, dfRNN = predict_RNN(coin,type)
    trainXGboost, validXGboost, predictXGboost, dfXGboost = predict_XGboost(coin,type)

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
                name="LSTM Predictions Price",
            ),
            go.Scatter(
                x=validRNN.index,
                y=validRNN["Predictions"],
                mode='lines+markers',
                name="RNN Predictions Price",
            ),
             go.Scatter(
                x=validXGboost.index,
                y=validXGboost["Predictions"],
                mode='lines+markers',
                name="XGboost Predictions Price",
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
                marker=dict(color="orange")
            ),
            go.Bar(
                x=["RNN"],
                y=predictRNN["Predictions"],
                name="RNN",
                marker=dict(color="green")
            ),
            go.Bar(
                x=["XGboost"],
                y=predictXGboost["Predictions"],
                name="XGboost",
                marker=dict(color="purple")
            ),
            
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