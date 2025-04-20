from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Helpdesk Assistant", className="text-center my-4"),

    dbc.Row([
        # Left Column – 55% Width
        dbc.Col([
            dbc.Row(
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.Input(id="input1", type="text", placeholder="Enter Ticket ID...", size="md"),
                            dbc.Button("Search", id="search-btn", n_clicks=0, color="primary", size="md")
                        ],
                        className="mb-3"
                    ),
                    width="auto",
                    style={"maxWidth": "550px", "width": "100%"}
                ),
                justify="start"
            ),

            html.Hr(),
            html.H3("Transcript"),
            html.Div("Transcript Here....", className="transcript-div", style={
                "border": "1px solid #ccc", "padding": "10px", "minHeight": "150px"}),

            html.H3("Summary", className="mt-4"),
            html.Div("Summary...", className="summary-div", style={
                "border": "1px solid #ccc", "padding": "10px", "minHeight": "100px"}),

        ], md=4),  # 55%

        # Right Column – 45% Width
        dbc.Col([
            html.H2("Sentiment Graph"),
            html.Div(
                dcc.Graph(),
                style={
                    "border": "1px solid #ccc",
                    "padding": "10px",
                    "borderRadius": "5px",
                    "backgroundColor": "#f9f9f9"
                }
            ),

            html.H3("Suggestions", className="mt-4"),
            html.Div("Suggestions will appear here...", className="suggestions-div", style={
                "border": "1px solid #ccc",
                "padding": "10px",
                "minHeight": "150px"  # same as transcript
            })
        ], md=7)  # 45%
    ])
], fluid=True)

if __name__ == '__main__':
    app.run(debug=True)
