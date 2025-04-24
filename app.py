from dash import Dash, html, dcc, callback, Output, Input, no_update
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from threading import Thread,Event
import datetime
import speech_recognition as sr
from functions.model_utils import Model
from functions.db_utils import update_chat,update_conv_and_fetch,clear_db,update_session_table,get_full_conv,get_chat_details
from functions.auth_utils import create_session

class CallCenter():
    def __init__(self,stop_event):
        # clear_db("conv")
        # clear_db("chat_update")
        self.session_id,self.session_ts=create_session()
        self.ticket_id=""
        self.stop_event = stop_event 

    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("\nListening... \n")
            r.pause_threshold = 20  # cut the audio for pause more than 8 sec

            while not self.stop_event.is_set():  # Check the stop event
                try:
                    audio_ = r.listen(source, 30, 20)  # 20 seconds first time, 10 second chunks
                    self.recog(audio_) #Call the recog function directly
                except sr.WaitTimeoutError:
                    print("No speech detected for a while. Continuing to listen...")
                    continue  # Continue listening if no speech is detected within the timeout
                except Exception as e:
                    print("Error in listening loop:", e)
                    break  # Exit loop on error
            print("Listening stopped.")

    def recog(self,audio_):
        r = sr.Recognizer()
        try:
            query = r.recognize_google(audio_, language='en-us')
            print(query)
            final_query = update_conv_and_fetch(query)
            self.analysis(final_query)

        except Exception as e:
            print("Unable to understand.", e)

    def analysis(self,conv):
        # conv=update_conv_and_fetch(conv)
        print("Hello inside Analysis")
        m=Model()
        transcript=m.transcript(conv)
        intent,summary,sentiment,suggestion,status=m.call_analysis(transcript)
        update_chat(intent,summary,sentiment,suggestion,status)
        # update_session_table(self.session_id,self.session_ts,intent,transcript)
        # self.create_ts=datetime.datetime.now()
        # update_existing_ticketID(self.session_id,self.ticket_id,intent,summary,self.create_ts,status)

    def existing_ticket(self,ticket_id):
        self.ticket_id=ticket_id
        self.create_ts=datetime.datetime.now()

# Global variables to manage the call state and thread
stop_listening_event = Event()
listening_thread = None
call_center_instance = None

def get_details():
    conv=get_full_conv()
    m=Model()
    transcript=m.transcript(conv)
    summary,suggestion,sentiment=get_chat_details()
    return transcript,summary,suggestion,sentiment


def start_call():
    global call_center_instance, listening_thread, stop_listening_event
    stop_listening_event.clear()  # Ensure the event is clear before starting
    call_center_instance = CallCenter(stop_listening_event)
    listening_thread = Thread(target=call_center_instance.listen)
    listening_thread.daemon = True  # Allow the main thread to exit even if this thread is running
    listening_thread.start()


def end_call():
    global stop_listening_event, listening_thread
    if listening_thread and listening_thread.is_alive():
        stop_listening_event.set()  # Signal the thread to stop
        listening_thread.join()  # Wait for the thread to finish
    print("Call ended.")

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

            html.H3("Summary", className="mt-4"),
            html.Div("Summary Here...", id="customer", className="customer-div"),
            html.Hr(),
            html.H3("Transcript"),
            html.Div("Transcript Here....", id="transcript", className="transcript-div"),

            # html.H3("Summary", className="mt-4"),
            # html.Div("Summary...", id="summary", className="summary-div"),

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
    ]),
    dcc.Interval(
        id='interval-component',
        interval=15 * 1000,  # in milliseconds (15 seconds)
        n_intervals=0  # number of times the interval has passed
    )
], fluid=True)

@callback(
    Output("transcript", "children"),
    Output("customer", "children"),
    Output("suggestions", "children"),
    Output("line-graph", "figure"),
    Output("call-toggle", "className"),
    Output("call-text", "children"),
    Input("call-toggle", "n_clicks"),
    Input("interval-component","n_intervals"),
    prevent_initial_call=True
)
def toggle_call_slider_and_update_dashboard(n_clicks,n_intervals):
    global listening_thread

    is_listening = listening_thread and listening_thread.is_alive()

    if n_clicks % 2 == 0:
        if is_listening:
            end_call()  # Stop the listening thread
        return no_update, no_update, no_update, no_update, "call-slider off", "Pick Up"
    else:
        if not is_listening:
            start_call() # start call if call is not in the middle of listening

        if is_listening:
            transcript,summary,suggestion,sentiment=get_details()

            x_values=[]
            for i in range(0,len(sentiment)+1):
                x_values.append(i)
            
            fig = go.Figure(
                data=[go.Scatter(
                    x=x_values,
                    y=sentiment,
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
            return transcript, summary, suggestion, fig, "call-slider on", "Listening..."
        else:
            return no_update,no_update,no_update,no_update, "call-slider on", "Listening..."
if __name__ == '__main__':
    app.run(debug=True)