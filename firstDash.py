from dash import Dash, html, dcc, callback, Output, Input, no_update
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import numpy as np

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
            html.Div("Transcript Here....", id="transcript", className="transcript-div"),

            html.H3("Summary", className="mt-4"),
            html.Div("Summary...", id="summary", className="summary-div"),

        ], md=5),

        dbc.Col(
            [
                # Top Row: Call Slider aligned with Search bar
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            id="call-toggle",
                            children=[
                                html.Div(id="call-knob", className="call-knob"),
                                html.Span(id="call-text", children="Pick Up"),
                            ],
                            className="call-slider off",
                            n_clicks=0
                        ),
                        width="auto",
                        style={"marginBottom": "15px"}
                    ),
                    justify="end"
                ),

                html.H2("Sentiment Graph"),
                html.Div(
                    dcc.Graph(id="line-graph"),
                    className="graph-div"
                ),

                html.H3("Suggestions", className="mt-4"),
                html.Div("Suggestions will appear here...", id="suggestions", className="suggestions-div")
            ],
            md=7
        )
    ])
], fluid=True)

@callback(
    Output("transcript", "children"),
    Output("summary", "children"),
    Output("suggestions", "children"),
    Output("line-graph", "figure"),
    Output("call-toggle", "className"),
    Output("call-text", "children"),
    Input("call-toggle", "n_clicks"),
    prevent_initial_call="initial_duplicate"
)
def toggle_call_slider_and_update_dashboard(n_clicks):
    summary="""In this call, Ramesh Kumar contacts ABC Bank's online banking support after facing login issues with his account. He informs the agent, Priya, that despite entering the correct credentials, he's receiving an “Invalid Credentials” error. After verifying his identity, Priya learns that Ramesh had recently changed his password. She suspects the system may have flagged his account due to multiple login attempts or session timeout. To resolve the issue, Priya guides him through the password reset process, including submitting his user ID and mobile number, entering the received OTP, and setting a new secure password. Ramesh successfully logs in with the new credentials and expresses his gratitude. Priya confirms that everything is now functioning properly and offers further assistance, which Ramesh declines. The call ends on a positive note, with both parties exchanging pleasantries. The issue is resolved efficiently with courteous and professional support."""
    transcript="""Agent: Good afternoon! You've reached ABC Bank's Online Banking Support. My name is Priya. May I know who I'm speaking with?\n
Customer: Hi Priya, this is Ramesh Kumar. I'm having some trouble logging into my online banking account.\n
Agent: I'm sorry to hear that, Mr. Kumar. I'll be happy to assist you. Could you please confirm your registered mobile number and the last 4 digits of your account number for verification?\n
Customer: Sure. My mobile number is 9876543210, and the last 4 digits of my account number are 3321.\n
Agent: Thank you for verifying the details. May I know what exactly happens when you try to log in?\n
Customer: Yeah, I enter my user ID and password, but it says "Invalid Credentials." I'm sure I'm entering the correct details.\n
Agent: Understood. Just to confirm, have you recently changed your password?\n
Customer: Yes, I changed it last week. It worked fine then, but today it's not letting me in.\n
Agent: Alright. It's possible the system flagged it due to multiple login attempts or a session timeout. Let's try resetting the password once again just to be sure. Would you like me to walk you through the steps?\n
Customer: Yes, please. That would help.\n
Agent: Great. First, go to our official website and click on “Forgot Password” under the login fields. Are you there?\n
Customer: Yes, I'm on that page.\n
Agent: Perfect. Now enter your User ID and the registered mobile number, then click “Submit.” You should receive a one-time password on your phone.\n
Customer: Got it. Just entered the OTP… Done.\n
Agent: Now, you can create a new password. Please make sure it's at least 8 characters, with a mix of letters, numbers, and a special character.\n
Customer: Okay, I've reset it.\n
Agent: Wonderful. Now try logging in with the new password.\n
Customer: Hold on… logging in… Yep, I'm in! That worked. Thanks a lot, Priya!\n
Agent: You're most welcome, Mr. Kumar! Is there anything else I can help you with today?\n
Customer: Nope, that was all. Thanks again for the help!\n
Agent: Anytime! Have a great day and thank you for banking with ABC Bank. Take care!\n
Customer: You too. Bye!\n"""
    suggestion="""Follow-Up Reminder: "Before you go, I recommend updating your password recovery options to ensure future access to your account is easier. Would you like to update them now?"\n
Customer Satisfaction Check: "I'm glad I could assist you today, Mr. Kumar. If you need any further assistance, don't hesitate to reach out. Would you be able to rate your experience for me?"\n
Offer Additional Help: "If you ever encounter any more issues or need further assistance, feel free to call or chat with us again. We're here to help anytime!\n"""
    
    x_values = np.arange(1, 51)

# Generate y values to simulate a "roller coaster" of emotions (random fluctuations)
    y_values = np.sin(np.linspace(0, 10, 50)) + np.random.normal(0, 0.5, 50)
    
    fig = go.Figure(
        data=[go.Scatter(
            x=x_values,
            y=y_values,
            mode='lines+markers',
            name='Customer Sentiment',
            line=dict(color='green')
        )],
        layout=go.Layout(
            title='Customer Sentiment',
            xaxis_title='Iterations',
            yaxis_title='Sentiment',
            hovermode='closest'
        )
    )

    # Toggle button state
    if n_clicks % 2 == 0:
        return no_update, no_update, no_update, no_update, "call-slider off", "Pick Up"
    else:
        return transcript, summary, suggestion, fig, "call-slider on", "Listening..."

if __name__ == '__main__':
    app.run(debug=True)
