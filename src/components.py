import dash
from dash import html
import dash_daq as daq
import dash_ag_grid as dag
from dash import html
from data_preparation import *


defaultColDef = {
    "resizable": True,
    "wrapHeaderText": True,
    "autoHeaderHeight": True,
}


columnDefs = [
    {
        "headerName": "Countries Europe",
        "stickyLabel": True,
        "children": [
            {"field": "country", "pinned": True, },
        ],
    },
    {
        "headerName": "Total events and fatalities",
        "children": [
            {"field": "events"},
            {"field": "fatalities"},
        ],
    },

    {
        "headerName": "Total events by type",
        "stickyLabel": True,
        "children": [
            {"field": col} for col in list(df["event_type"].unique())
        ],
    },

    {
        "headerName": "Total event by Disorder Type",
        "stickyLabel": True,
        "children": [
            {"field": col} for col in list(df["disorder_type"].unique())
        ],
    },

    {
        "headerName": "City with most events",
        "stickyLabel": True,
        "children": [
            {"field": col} for col in ["location", "Events"]
        ],
    },
]

grid = dag.AgGrid(
    id="get-started-example-basic",
    rowData=data.to_dict("records"),
    columnDefs=columnDefs,
    className="ag-theme-alpine-dark",
    style={'height': '500px'},
    defaultColDef=defaultColDef
)


active_tab_style = {
    "font-family": "serif",
    "border-bottom": "none"
}

tab_style = {"marginLeft": "auto"}


theme = {
    'dark': True,
    'detail': 'lightgray',
}


def daq_comp(classname):
    return html.Div(className="div-daq", children=[
        daq.DarkThemeProvider(
            theme=theme,
            children=[
                html.Div(className="daq", children=[
                    daq.Slider(
                        id=classname,
                        min=1,
                        max=40,
                        value=10,
                        targets={"10": {"label": "Ideal"}},
                        color="gray",
                        className='dark-theme-control'
                    )
                ])
            ]
        )
    ])


def my_img():
    return html.Img(
        src=dash.get_asset_url("profile_picture.png"),
        className="div-img img-responsive rounded-square mb-4",
        style={"height": "160px", "width": "180px"}
    )
