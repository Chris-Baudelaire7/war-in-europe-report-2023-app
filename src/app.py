from flask import Flask
from dash import Dash, html
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from layout import layout
from navbar import navbar


# Parameters

app_params = {
    "server": Flask(__name__),
    "title": "War in The World",
    "update_title": "Wait a moment...",
    "url_base_pathname": "/",
    "external_stylesheets": [dbc.themes.CYBORG, dbc.icons.BOOTSTRAP],
    "suppress_callback_exceptions": True,
    "meta_tags": [{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}]
}

server_params = {"debug": False}


# Create app

app = Dash(__name__, **app_params)
server = app.server

app.layout = html.Div(className="app", children=[
    navbar, layout
])

app.run_server(**server_params, port="0.0.0.0:2322")
