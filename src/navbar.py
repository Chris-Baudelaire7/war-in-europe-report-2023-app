from dash import html
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify


navbar = html.Div(className="header container-fluid p-2 mb-4", children=[
    html.Div(className="d-flex flex-column flex-lg-row align-items-center justify-content-center justify-content-md-between", children=[
        html.Div(className="d-flex flex-column flex-lg-row align-items-center", children=[
            html.Div(className="d-flex flex-column flex-md-row align-items-center justify-content-center", children=[

                html.Div(className="text-center d-inline-block mb-2 mb-xl", children=[
                    html.H2(className="d-flex align-items-center title", children=[
                       html.Span("Analytics", className="text-white"),
                       html.Span("Paper", className="text-red",
                                 style={'color': 'red'})
                    ]),
                ])
            ]),

            html.Div(className="ms ms-lg-4 d-xl d-xl-block", children=[
                html.H5(
                    "Armed Conflicts Location And Events Data Report: Europe - 2023",
                    className="title-header text-lg-center text-xl"
                ),
                html.H6("Statistical Analysis Report And Data Visualization",
                        className="subtitle-header text-muted text-center text-md-start")
            ]),
        ]),

        html.Div(className="mt-4 mt-lg-0", children=[
            dbc.Nav(className="ms-auto d-flex flex-row align-items-center justify-content-center", navbar=True, children=[

                dmc.Tooltip(
                    label="Data and Source Code",
                    position="bottom",
                    withArrow=True,
                    arrowSize=6,
                    color="black",
                    transition="scale",
                    transitionDuration=300,
                    ff="serif",
                    className="m3 ms-3",
                    children=[
                        dbc.Button(href="https://github.com/Chris-Baudelaire7/war-in-europe-report-2023-app", className="btn", children=[
                            DashIconify(icon="radix-icons:github-logo",
                                        width=30), " See on github"
                        ])
                    ]
                ),

            ])
        ])
    ])
])
