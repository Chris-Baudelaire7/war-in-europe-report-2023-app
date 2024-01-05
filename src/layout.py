import dash_deck as ddk
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc
from dash import html, dcc
from components import *
from data_preparation import *
from graphs_and_callback import *


access_api_token = "pk.eyJ1IjoiY2hyaXMtYmF1ZGVsYWlyZSIsImEiOiJjbHB6dWYxb2wxOWdmMnJvOGtzaDVyb3Y2In0.pXQ81pAk9gRoUHXDnNsjJg"


r, tooltip = total_events_Deck()




layout = html.Div(className="layout px-0 px-lg-3 px-xl-5 pb-5 mx-0 mx-xl-3 mx-auto", children=[

    html.Div(className="row", children=[
        html.Div(className="col-lg-8", children=[
            html.Div(className="", children=[
                ddk.DeckGL(r.to_json(), id="deck-gl", tooltip=tooltip, mapboxKey=access_api_token),
            ])
        ]),

        html.Div(className="col-lg-4", children=[

            # html.Div(className="col-11 mx-auto mb-3", children=[
            #     html.Span(id="country-chosen", className=""),
            #     dcc.Dropdown(
            #         id="select-country",
            #         options=[{"label": "Europe", "value": "Europe"}] + [{"label": x, "value": x} for x in df.country.unique()],
            #         value="Europe",
            #         placeholder="Choose a country",
            #     )
            # ]),
            html.Div(className="", children=[
                daq_comp("daq-slider-events"),
                dcc.Graph(config=dict(displayModeBar=False), id="distribution_events"),
            ]),
            
            html.Div(className="mt-3", id="test", children=[
                
            ]),
            
            html.Div(className="mt-3", children=[
                daq_comp("daq-slider-fatalities"),
                dcc.Graph(config=dict(displayModeBar=False), id="distribution_fatalities"),
            ]),

            #timeline
        ]),
    ]),


    html.Div(className="row intro mt-3 mt-lg-5 text-center", children=[
        dcc.Markdown(
            """
            ##### All wars perpetrated in Europe from January 1st to December 8th, 2023
            
            **On this map, the height and color represent the number of armed conflicts, while the heat map indicates the number of fatalities.**
            
            **We observe a significant concentration on the heat map in Ukraine, where the war against Russia has led to a high number of casualties and has been particularly intense.**
            
            *You can zoom out to get a better view of the heat map.*
            """,

            className="text-dark",
        ),

        html.Div(className="col mt-2 number", children=[
            html.Span(f"{len(df)}", className="text-warning fs-3"),
            html.Span(" armed conflicts"),

            html.Br(),

            html.Span(f"{df['fatalities'].sum()}", className="text-danger fs-3"),
            html.Span(" deaths recorded"),

            html.Br(),

            html.Span(f"89%", className="text-primary fs-3"),
            html.Span(" of the wars in Ukraine")
        ])
    ]),

    # html.Div(className="my-5", style={"fontFamily": "serif"}, children=[
    #     dmc.Alert(title="War in Ukraine🇺🇦 !", color="red", children=[
    #         dcc.Markdown(
    #             """                
    #             monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupesterroristes, laj facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflits égionaux et des cellules terroristes dans de nombreux pays.""",

    #             className="text-dark comments",
    #         ),
    #     ])
    # ]),


    # --------------------------------------------------------------------------------------------------------------------

    html.H3("Trend over the course of the year", className="my-5"),

    html.Div(className="row align-items-center mt-3", children=[
        html.Div(className="col-md-6", children=[
            
            dcc.Loading(
                dcc.Graph(config=dict(displayModeBar=False), id="timeseries"),
                type="circle", color="firebrick"
            ),
            
            html.Div(className="selection d-flex justify-content-center mt-2", children=[
                dmc.ChipGroup(value="weekly_mean_line", id="period-type", children=[
                    dmc.Chip(x, value=y, size="sm", color="red")
                    for x, y in zip(
                        ["Daily trends (Raw data)", "Weekly mean (line)", "Weekly mean (area)"],
                        ["daily", "weekly_mean_line", "weekly_mean_area"]
                    )
                ])
            ])
        ]),
        
        html.Div(className="col-md-2", children=[
            dcc.Markdown(
                """
                ###### Dans l'ensemble, le nombre d'attaques terroristes dans
                
                monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs.
                
                ###### Dans l'ensemble, le nombre d'attaques terroristes dans
                
                monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée"
                """,

                className="small_comments",
            ),
        ]),

        html.Div(className="col-md-4", children=[
            
            html.Div(className="selection d-flex justify-content-center", children=[
                dmc.ChipGroup(value="all", id="area", children=[
                    dmc.Chip(x, value=y, size="sm", color="red")
                    for x, y in zip(
                        ["All countries", "excluding Ukraine and Russia"],
                        ["all", "ue"]
                    )
                ])
            ]),
            
            dcc.Graph(config=dict(displayModeBar=False), id="rate_deaths"),
        ]),


        html.Div(className="col-12", children=[
            dcc.Markdown(
                """
                The vast majority of deaths resulting from armed conflicts in Europe are concentrated in Ukraine, with the country contributing to nearly 99% of the total death rate. In contrast, the combined contribution of the other 30 countries is relatively low, making up only about 1.39% of the overall death toll
                """,

                className="comments",
            )
        ])
    ]),
    
    
    html.Div(className="row justify-content-center align-items-center mt-4", children=[
        
        html.Div(className="col-md-4", children=[
            dcc.Graph(config=dict(displayModeBar=False), figure=distribution_conflict_ue()),
        ]),
        
        html.Div(className="col-md-6", children=[

            dcc.Loading(
                dcc.Graph(config=dict(displayModeBar=False), id="uk_vs_ue"),
                type="circle", color="firebrick"
            ),

            html.Div(className="selection d-flex justify-content-center mt-2", children=[
                dmc.ChipGroup(value="weekly_mean_event", id="type-period", children=[
                    dmc.Chip(x, value=y, size="sm", color="red")
                    for x, y in zip(
                        ["Weekly mean event", "Weekly mean fatalities"],
                        ["weekly_mean_event", "weekly_mean_fatalities"]
                    )
                ])
            ])
        ]),
        
        html.Div(className="col-md-2", children=[
            dcc.Markdown(
                """
                ###### The vast majority of deaths resulting
                
                The vast majority of deaths resulting from armed conflicts in Europe are concentrated in Ukraine, with the country  is relatively low, making up only about 1.39% of the overall death toll.
                """,

                className="small_comments",
            )
        ]),
        
        
        html.Div(className="col-12 mt-3", children=[
            dcc.Markdown(
                """
                The vast majority of deaths resulting from armed conflicts in Europe are concentrated in Ukraine, with the country contributing to nearly 99% of the total death rate. In contrast, the combined contribution of the other 30 countries is relatively low, making up only about 1.39% of the overall death tollThe vast majority of deaths resulting from armed conflicts in Europe are concentrated in Ukraine, with the country contributing to nearly 99% of the total death rate. In contrast, the combined contribution of the other 30 countries is relatively low, making up only about 1.39% of the overall death toll.
                """,

                className="comments",
            )
        ]),
        
        
        
    ]),
    
    # ----------------------------------------------------------------------------------------------------------------------
    
    
    html.Div(className="row justify-content-center mt-4", children=[
        
        html.Div(className="col-md-2", children=[
            dcc.Markdown(
                """
                ###### The vast majority of deaths resulting
                
                The vast majority of deaths resulting from armed conflicts in Europe are concentrated in Ukraine, with the country  is relatively low, making up only about 1.39% of the overall death toll.
                
                ###### The vast majority of deaths resulting
                
                The vast majority of deaths resulting from armed conflicts in Europe are concentrated in Ukraine, with the country  is relatively low, making up only about 1.39% of the overall death toll.
                """,

                className="small_comments",
            )
        ]),
        
        html.Div(className="col-md-5", children=[
            dcc.Graph(config=dict(displayModeBar=False), figure=mapbox_ue()),
        ]),
        
        html.Div(className="col-md-5", children=[
            dcc.Graph(config=dict(displayModeBar=False), figure=mapbox_ukraine()),
        ]),
    ]),
    
    
    # ----------------------------------------------------------------------------------------------------------------------
    
    
    html.Div(className="mt-5", children=[
        dcc.Markdown(
            """ 
                It is evident that Russia and Ukraine dominate the rankings when it comes to armed conflicts in Europe. To gain a better understanding of the situation, we turn our attention to other countries. This year, France and Germany are the most affected nations, with over 7,654 conflicts in France, accounting for 5% of armed conflicts in Europe (excluding Russia and Ukraine), even surpassing the number of conflicts in Russia, which stands at 765. Germany has the highest number of casualties, totaling 567,888 armed conflicts, of which only 765 occur in the month of March.
            """,
            className="comments",
        ),

    ]),

    # ---------------------------------------------------------------------------------------------------------------------
    
    
    html.Div(className="row", children=[
        
        dcc.Markdown(
            """                
                *We adopted this approach to prevent bias in the analysis due to the high number of conflicts and deaths in Ukraine. Additionally, Russia's extensive geographical span, bordering both Europe and Asia, is often excluded when considering European countries.*
            """,
            className="comments",
        )
        
    ]),



    # --------------------------------------------------------------------------------------------------------------------

    

    html.Div(className="row align-items-center mt-5", children=[
        
        html.Div(className="col", children=[
            dbc.Tabs(class_name="tabular", children=[
                dbc.Tab(
                    label="Repartition en pourcentage", 
                    tab_style=tab_style,
                    active_tab_style=active_tab_style,
                    children=[
                        
                        html.Div(className="row align-items-center mt-5", children=[

                            html.Div(className="col-md-2", children=[
                                dcc.Markdown(
                                    """
                                    ###### Dans l'ensemble, le nombre d'attaques terroristes dans
                                    
                                    monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupesterroristes, laj facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflits égionaux et des cellules terroristes dans de nombreux pays.""",

                                    className="small_comments",
                                ),
                            ]),

                            html.Div(className="col-md-4", children=[
                                dcc.Graph(config=dict(displayModeBar=False), figure=heatmap_month_all_countries()),
                            ]),

                            html.Div(className="col-md-2", children=[
                                dcc.Markdown(
                                    """
                                    ###### Dans l'ensemble, le nombre d'attaques terroristes dans
                                    
                                    monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupesterroristes, laj facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflits égionaux et des cellules terroristes dans de nombreux pays.""",

                                    className="small_comments",
                                ),
                            ]),

                            html.Div(className="col-md-4", children=[
                                dcc.Graph(id="bar-period",
                                          config=dict(displayModeBar=False)),

                                html.Div(className="selection d-flex justify-content-center", children=[
                                    dmc.ChipGroup(value="month", id="select-period", children=[
                                        dmc.Chip(
                                            x, value=y, size="sm", color="red")
                                        for x, y in zip(
                                            ["Month of year", "Days of week","Days of month"],
                                            ["month", "day_name", "day"]
                                        )
                                    ])
                                ])
                            ]),

                        ]),

                        html.Div(className="row align-items-center", children=[
                            html.Div(className="col-md-7", children=[
                                dcc.Graph(config=dict(displayModeBar=False), figure=choropleth_europe_globale()),
                            ]),

                            html.Div(className="col-md-5", children=[
                                
                                html.Div(className="col-md-12", children=[
                                    dcc.Graph(config=dict(displayModeBar=False), figure=ranking_country()),
                                ]),
                                
                                html.Div(className="col-md-12", children=[
                                    dcc.Graph(config=dict(displayModeBar=False), figure=ranking_city()),
                                ]),

                            ]),
                        ])
                    ]
                ),
                
                dbc.Tab(
                    label="Evolution temporelle absolue/relative",
                    active_tab_style=active_tab_style,
                    class_name="bg-danger",
                    children=[
                        
                        html.Div(className="row align-items-center mt-5", children=[

                            html.Div(className="col-md-2", children=[
                                dcc.Markdown(
                                    """
                                    ###### Dans l'ensemble, le nombre d'attaques terroristes dans
                                    
                                    monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupesterroristes, laj facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflits égionaux et des cellules terroristes dans de nombreux pays.""",

                                    className="small_comments",
                                ),
                            ]),

                            html.Div(className="col-md-4", children=[
                                dcc.Graph(config=dict(displayModeBar=False), figure=heatmap_month_without_uk_and_rus()),
                            ]),

                            html.Div(className="col-md-2", children=[
                                dcc.Markdown(
                                    """
                                    ###### Dans l'ensemble, le nombre d'attaques terroristes dans
                                    
                                    monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupesterroristes, laj facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflits égionaux et des cellules terroristes dans de nombreux pays.""",

                                    className="small_comments",
                                ),
                            ]),

                            html.Div(className="col-md-4", children=[
                                dcc.Graph(id="bar-period-wur", config=dict(displayModeBar=False)),

                                html.Div(className="selection d-flex justify-content-center", children=[
                                    dmc.ChipGroup(value="month", id="select-period-wur", children=[
                                        dmc.Chip(
                                            x, value=y, size="sm", color="red")
                                        for x, y in zip(
                                            ["Month of year", "Days of week","Days of month"],
                                            ["month", "day_name", "day"]
                                        )
                                    ])
                                ])
                            ]),

                        ]),
        
                        
                        html.Div(className="row align-items-center", children=[

                            html.Div(className="col-md-7", children=[
                                dcc.Graph(config=dict(displayModeBar=False), figure=choropleth_europe_ue()),
                            ]),

                            html.Div(className="col-md-5", children=[

                                html.Div(className="row align-items-center", children=[

                                    html.Div(className="col-md-12", children=[
                                        dcc.Graph(config=dict(displayModeBar=False), figure=ranking_city_ue()),
                                    ]),

                                    html.Div(className="col-md-12", children=[
                                        dcc.Graph(config=dict(displayModeBar=False), figure=ranking_country_ue()),
                                    ])

                                ])

                            ])

                        ])
                    ]
                ),
            ])
        ]),
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        
        
        
    ]),


    # --------------------------------------------------------------------------------------------------------------------

    html.H3("More than half of conflicts are politically motivated",
            className="mt-5 mb-3"),
    html.Div(className="", children=[
        dcc.Markdown(
            """
                Dans l'ensemble, le nombre d'attaques terroristes dans le 
                monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupesterroristes, laj facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflits égionaux et des cellules terroristes dans de nombreux pays.""",

            className="comments",
        ),
    ]),

    html.Div(className="row align-items-center mt-3", children=[
        html.Div(className="col-lg-5", children=[
            dcc.Graph(config=dict(displayModeBar=False), figure=disorder_type()),
        ]),

        html.Div(className="col-md-2", children=[
            dcc.Markdown(
                """
                ###### Dans l'ensemble, le nombre d'attaques terroristes
                
                monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée
                
                ###### Dans l'ensemble, le nombre d'attaques terroristes
                
                monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée
                """,

                className="small_comments",
            ),
        ]),

        html.Div(className="col-md-5", children=[
            dcc.Graph(config=dict(displayModeBar=False), id="disorder-type-time-series"),
            html.Div(className="selection d-flex justify-content-center", children=[
                dmc.ChipGroup(value="line", id="disorder-graph", children=[
                    dmc.Chip(x, value=y, size="sm", color="red")
                    for x, y in zip(["Line chart", "Bar chart"], ["line", "bar"])
                ])
            ])
        ]),

    ]),


    # --------------------------------------------------------------------------------------------------------------


    html.H3("Armed Conflits in Europe: By Events Type", className="mt"),

    html.Div(className="row align-items-center", children=[

        html.Div(className="col-md-2", children=[
            dcc.Markdown(
                """
                ###### Dans l'ensemble, le nombre d'attaques terroristes dans le 
                
                monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée.""",

                className="small_comments",
            ),
        ]),

        html.Div(className="col-md-5", children=[
            dcc.Graph(config=dict(displayModeBar=False),id="event-type-time-series"),
            html.Div(className="selection d-flex justify-content-center", children=[
                dmc.ChipGroup(value="line", id="event-graph", children=[
                    dmc.Chip(x, value=y, size="sm", color="red")
                    for x, y in zip(["Line chart", "Bar chart"], ["line", "bar"])
                ])
            ])
        ]),

        html.Div(className="col-md-5", children=[
            dcc.Graph(config=dict(displayModeBar=False), figure=events_type()),
        ]),

    ]),


    # -----------------------------------------------------------------------------------------------------------


    html.Div(className="row mt-4", children=[
        
        html.H5("From a geospatial perspective", className="mb-4"),

        html.Div(className="col-md-3", children=[
            html.Small("Analysis by event type"),
            html.Div(className="mb-3", children=[
                dcc.Dropdown(
                    id="select-event",
                    options=[{"label": x, "value": x}
                             for x in df.event_type.unique()],
                    value="Protests",
                    placeholder="Choose an event type",
                )
            ]),
            
            dcc.Markdown(
                """
                ###### Dans l'ensemble, le nombre d'attaques terroristes dans le 
                
                monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupesterroristes, laj facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflits égionaux et des cellules terroristes dans de nombreux pays.""",

                className="small_comments",
            ),
        ]),

        html.Div(className="col-md-5", children=[
            dcc.Graph(id="event-type-mapbox", config=dict(displayModeBar=False)),
        ]),

        html.Div(className="col-md-4", children=[
            dcc.Graph(config=dict(displayModeBar=False), id="distribution-event-type"),
        ]),

    ]),

    html.Div(className="row align-items-center mt", children=[

        html.Div(className="col-md-7", children=[
            dcc.Graph(config=dict(displayModeBar=False),
                      id="event-type-choropleth"),
        ]),

        html.Div(className="col-md-5", children=[
            html.Div(className="row align-items-center", children=[

                html.Div(className="col-md-12", children=[
                    dcc.Graph(config=dict(
                        displayModeBar=False), figure=ranking_city_ue()),
                ]),

                html.Div(className="col-md-12", children=[
                    dcc.Graph(config=dict(
                        displayModeBar=False), figure=ranking_country_ue()),
                ])

            ])
        ]),
    ]),

    
    # ----------------------------------------------------------------------------------------------------------------

    
    html.H3("The Calendar of Armed Conflicts in Europe", className="my-5 pt-3"),
    
    html.Div(className="row align-items-center mt-3", children=[
        html.Div(className="col-md-6", children=[
            
            html.Div(className="mt-3", children=[
                dcc.Graph(config=dict(displayModeBar=False), figure=calendar(), id="calendar"),
            ]),
            
            html.Div(className="my-2", children=[
                dcc.Graph(config=dict(displayModeBar=False), figure=calendar_fatalities(), id="calendar_fatalities"),
            ]),
            
            dcc.Markdown(
                """
                ###### Conflicts and fatalities every day 
                
                monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupesterroristes, laj facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflits égionaux et des cellules terroristes dans de nombreux pays.""",

                className="small_comments",
            ),
        ]),
        
        html.Div(className="col-md-6 justify-content-end", children=[

            html.Div(className="md-inline text-end", children=[
                html.Span("Europe on", className="text-end d-block"),
                dcc.DatePickerSingle(
                    id='select-date',
                    min_date_allowed=df["event_date"].min(),
                    max_date_allowed=df["event_date"].max(),
                    initial_visible_month=df["event_date"].min(),
                    date=df["event_date"].min(),
                    className=""
                ),

                DashIconify(icon="game-icons:click", width=20),
            ]),

            dcc.Markdown(
                """
                monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupesterroristes, laj facilité dans de nombreux pays.""",

                className="small_comments text-end",
            ),

            dcc.Graph(config=dict(displayModeBar=False), id="map-calendar"),
        ]),
        
        
    ]),


    # ----------------------------------------------------------------------------------------------------------------
    
    html.Hr(className="my-5 pt-5"),
    html.H3("Summary of Key Figures", className="pt-3"),

    html.Div(className="row align-items-center mt-3", children=[
        html.Div(className="col-12", children=[
            grid
        ])
    ]),
    
    
    # ----------------------------------------------------------------------------------------------------------------    
    
    
    html.Div(className="separate my-5"),
    

    html.Div(className="row align-items-center text-center", children=[
        
        html.H1(className="display-1 fw-bold", children=[
            html.Span("Analytics", className="text-white"),
            html.Span("Paper", className="text-red", style={'color': 'red'})
        ]),
        
        html.Span("By Chris Baudelaire .K", className="text-white fw-bold mb-3"),
        
        # html.Div(className="div-img", children=[
        #     html.Img(
        #         src=dash.get_asset_url('profile_picture.png'),
        #         className="div-img img-responsive rounded-square mb-4",
        #         style={"height": "160px", "width": "180px"}
        #     ),
        # ]),
        
        html.Span("Powered by Plotly/Dash", className=""),
        
    ]),
])
