import dash_deck as ddk
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from dash import html, dcc
from components import *
from data_preparation import *
from graphs_and_callback import *

import dash


access_api_token = "pk.eyJ1IjoiY2hyaXMtYmF1ZGVsYWlyZSIsImEiOiJjbHB6dWYxb2wxOWdmMnJvOGtzaDVyb3Y2In0.pXQ81pAk9gRoUHXDnNsjJg"

r, tooltip = total_events_Deck()

layout = html.Div(className="layout mx-0 mx-md-3 mx-lg-5", children=[

    # px-0 px-lg-3 px-xl-5 pb-5 mx-0 mx-xl-3 mx-auto

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

            html.Span(f"{df['fatalities'].sum()}",
                      className="text-danger fs-3"),
            html.Span(" deaths recorded"),

            html.Br(),

            html.Span(f"59%", className="text-primary fs-3"),
            html.Span(" of the wars in Ukraine")
        ])
    ]),

    html.Div(className="row", children=[
        html.Div(className="col-lg-8", children=[
            html.Div(className="", children=[
                ddk.DeckGL(r.to_json(), id="deck-gl",
                           mapboxKey=access_api_token),
            ])
        ]),

        html.Div(className="col-lg-4 mt-3 mt-xl-0", children=[

            html.Div(className="row", children=[
                html.Div(className="col-md-6 col-lg-12", children=[
                    daq_comp("daq-slider-events"),
                    dcc.Graph(config=dict(displayModeBar=False),
                              id="distribution_events"),
                ]),

                html.Div(className="col-md-6 col-lg-12 mt-3 mt-md-0 mt-xl-3", children=[
                    daq_comp("daq-slider-fatalities"),
                    dcc.Graph(config=dict(displayModeBar=False),
                              id="distribution_fatalities"),
                ]),
            ])

        ]),
    ]),



    # --------------------------------------------------------------------------------------------------------------------



    html.H3("Trend over the course of the year", className="my-5"),

    html.Div(className="row align-items-center mt-3", children=[

        html.Div(className="col-12 col-md-8 col-lg-6 order-first", children=[
            dcc.Loading(
                dcc.Graph(config=dict(displayModeBar=False), id="timeseries"),
                type="circle", color="firebrick"
            ),
            html.Div(className="selection d-flex justify-content-center mt-2", children=[
                dmc.ChipGroup(value="weekly_mean_line", id="period-type", children=[
                    dmc.Chip(x, value=y, size="sm", color="red")
                    for x, y in zip(
                        ["Daily trends (Raw data)", "Weekly mean (line)",
                         "Weekly mean (area)"],
                        ["daily", "weekly_mean_line", "weekly_mean_area"]
                    )
                ])
            ])
        ]),

        html.Div(className="col-12 col-lg-2 order-md-3 order-lg-2 mt-3 mt-lg", children=[
            html.Div(className="row", children=[
                html.Div(className="col-12", children=[
                    dcc.Markdown(
                        """
                        ###### More conflicts in the first quarter of the year
                        
                        The first quarter of the year was the most eventful, recording over **23,147** conflicts in Europe. In contrast, we observe a decline in wars in the months of April, July, and August.
                        """,

                        className="small_comments",
                    )
                ]),

                html.Div(className="col-12", children=[
                    dcc.Markdown(
                        """
                        ###### *Ukraine* and *Greece* make the difference
                        
                        **Greece** and **Ukraine** are the two countries with the highest number of casualties recorded this year. **145** casualties for Greece compared to **29,350** for Ukraine.
                        """,

                        className="small_comments",
                    ),
                ])
            ])
        ]),

        html.Div(className="col-12 col-md-4 col-lg-4 order-md-2 order-lg-3", children=[

            dcc.Graph(config=dict(displayModeBar=False), id="rate_deaths"),

            html.Div(className="selection d-flex justify-content-center", children=[
                dmc.ChipGroup(value="ue", id="area", children=[
                    dmc.Chip(x, value=y, size="sm", color="red")
                    for x, y in zip(
                        ["All countries", "No Ukraine and Russia"],
                        ["all", "ue"]
                    )
                ])
            ]),

        ]),

        html.Div(className="col-12 order-last mt-3", children=[
            dcc.Markdown(
                """
                The vast majority of deaths resulting from armed conflicts in Europe are concentrated in **Ukraine**, with the country contributing to nearly **99%** of the total death rate. In contrast, the combined contribution of the other **46 countries** is relatively low, making up only about **1.39%** of the overall death toll
                """,

                className="comments",
            )
        ])
    ]),



    # -------------------------------------------------------------------------------------------------------------------------




    html.Div(className="row justify-content-center align-items-center mt-4", children=[

        html.Div(className="col-12 col-lg-4 col-md-4", children=[
            dcc.Graph(config=dict(displayModeBar=False),
                      figure=distribution_conflict_ue()),
        ]),

        html.Div(className="col-12 mt-4 mt-md col-md-8 col-lg-6", children=[
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

        html.Div(className="col-12 col-xl-2 mt-3 mt-xl-0", children=[
            dcc.Markdown(
                """
                ###### Ukraine overwhelmingly dominates the rankings
                
                The number of conflicts in Ukraine remains high and consistent throughout the year, surpassing the rest of Europe for almost the entire year. In contrast, we observe significant variations in the rest of Europe.
                """,

                className="small_comments",
            )
        ]),


        html.Div(className="col-12 mt-3", children=[
            dcc.Markdown(
                """
                This can be naturally explained by **Russia's** invasion of **Ukraine** since **February 24, 2022**, which has led to a bloody war. This ongoing conflict is very intense and continues to claim victims.
                """,

                className="comments",
            )
        ]),



    ]),



    # ----------------------------------------------------------------------------------------------------------------------




    html.Div(className="row justify-content-center mt-4", children=[

        html.Div(className="col-12 col-xl-2", children=[
            html.Div(className="row", children=[
                html.Div(className="col-6 col-xl-12", children=[
                    dcc.Markdown(
                        """
                        ###### France overwhelmingly dominates the rankings in Europe
                        
                        In Europe (excluding Ukraine and Russia), France alone has recorded more than **8336** armed conflicts, accounting for approximately 28% of the total conflicts.
                        """,

                        className="small_comments",
                    )
                ]),

                html.Div(className="col-6 col-xl-12", children=[
                    dcc.Markdown(
                        """
                        ###### The War: More Intense at the Ukraine Border
                        
                        Occupation (Invasion) and War Zone between Russia and Ukraine"
                        """,

                        className="small_comments",
                    ),
                ])
            ])
        ]),

        html.Div(className="col-md-6 col-xl-5", children=[
            dcc.Graph(config=dict(displayModeBar=False), figure=mapbox_ue()),
        ]),

        html.Div(className="col-md-6 col-xl-5 mt-4 mt-md", children=[
            dcc.Graph(config=dict(displayModeBar=False),
                      figure=mapbox_ukraine()),
        ]),
    ]),


    # ---------------------------------------------------------------------------------------------------------------------


    html.Div(className="row mt-3", children=[

        dcc.Markdown(
            """                
                *Note: We have separated Ukraine from Europe and excluded Russia for a better understanding of the situation. We adopted this approach to prevent bias in the analysis due to the high number of conflicts and deaths in Ukraine. Additionally, Russia's extensive geographical span, bordering both Europe and Asia, is often excluded when considering European countries.*
            """,
            className="comments",
        )

    ]),


    # --------------------------------------------------------------------------------------------------------------------



    html.Div(className="row align-items-center mt-5", children=[

        html.Div(className="col", children=[
            dbc.Tabs(class_name="tabular", children=[
                dbc.Tab(
                    label="All European countries",
                    tab_style=tab_style,
                    active_tab_style=active_tab_style,
                    children=[

                        html.Div(className="row align-items-center mt-5", children=[

                            html.Div(className="col-12 col-md-6 col-lg-6 col-xl-2 order-1", children=[
                                dcc.Markdown(
                                    """
                                    ###### High level trend per day by month
                                    
                                    Wednesday and Thursday have the highest number of conflicts per day by month in all of Europe, with 1767 and 1775 conflicts respectively
                                    .""",

                                    className="small_comments",
                                ),
                            ]),

                            html.Div(className="col-12 col-md-6 col-lg-6 col-xl-4 order-3 order-xl-2", children=[
                                dcc.Graph(config=dict(displayModeBar=False),
                                          figure=heatmap_month_all_countries()),
                            ]),

                            html.Div(className="col-12 col-md-6 col-lg-6 col-xl-2 order-3 order-md-2 order-xl-3 mt-4 mt-md-0", children=[
                                dcc.Markdown(
                                    """
                                    ###### High level trend in event and fatalities by month and day
                                    
                                    In March and May, there are respectively the highest number of armed conflicts and fatalities in the year, while Saturday and Wednesday are respectively the highest number of armed conflicts and fatalities in the week
                                    """,

                                    className="small_comments",
                                ),
                            ]),

                            html.Div(className="col-12 col-md-6 col-lg-6 col-xl-4 order-4", children=[
                                dcc.Graph(id="bar-period",
                                          config=dict(displayModeBar=False)),

                                html.Div(className="selection d-flex justify-content-center", children=[
                                    dmc.ChipGroup(value="month", id="select-period", children=[
                                        dmc.Chip(
                                            x, value=y, size="sm", color="red")
                                        for x, y in zip(
                                            ["Month of year", "Days of week",
                                                "Days of month"],
                                            ["month", "day_name", "day"]
                                        )
                                    ])
                                ])
                            ]),

                        ]),

                        html.Div(className="row align-items-center", children=[
                            html.Div(className="col-md-7", children=[
                                dcc.Graph(config=dict(displayModeBar=False),
                                          figure=choropleth_europe_globale()),
                            ]),

                            html.Div(className="col-md-5", children=[

                                html.Div(className="col-md-12", children=[
                                    dcc.Graph(config=dict(
                                        displayModeBar=False), figure=ranking_country()),
                                ]),

                                html.Div(className="col-md-12", children=[
                                    dcc.Graph(config=dict(
                                        displayModeBar=False), figure=ranking_city()),
                                ]),

                            ]),
                        ])
                    ]
                ),

                dbc.Tab(
                    label="Europe without Ukraine and Russia",
                    active_tab_style=active_tab_style,
                    class_name="bg-danger",
                    children=[

                        html.Div(className="row align-items-center mt-5", children=[

                            html.Div(className="col-12 col-md-6 col-lg-6 col-xl-2 order-1", children=[
                                dcc.Markdown(
                                    """
                                    ###### High level trend per day by month
                                    
                                    Wednesday and Thursday have the highest number of conflicts per day by month in all of Europe, with 894 and 933 conflicts respectively.
                                    """,

                                    className="small_comments",
                                ),
                            ]),

                            html.Div(className="col-12 col-md-6 col-lg-6 col-xl-4 order-3 order-xl-2", children=[
                                dcc.Graph(config=dict(displayModeBar=False),
                                          figure=heatmap_month_without_uk_and_rus()),
                            ]),

                            html.Div(className="col-12 col-md-6 col-lg-6 col-xl-2 order-3 order-md-2 order-xl-3 mt-4 mt-md-0", children=[
                                dcc.Markdown(
                                    """
                                    ###### High level trend in event and fatalities by month and day
                                    
                                    In March and May, there are respectively the highest number of armed conflicts and fatalities in the year, while Saturday and Wednesday are respectively the highest number of armed conflicts and fatalities in the week.
                                    """,

                                    className="small_comments",
                                ),
                            ]),

                            html.Div(className="col-12 col-md-6 col-lg-6 col-xl-4 order-4", children=[
                                dcc.Graph(id="bar-period-wur",
                                          config=dict(displayModeBar=False)),

                                html.Div(className="selection d-flex justify-content-center", children=[
                                    dmc.ChipGroup(value="month", id="select-period-wur", children=[
                                        dmc.Chip(
                                            x, value=y, size="sm", color="red")
                                        for x, y in zip(
                                            ["Month of year", "Days of week",
                                                "Days of month"],
                                            ["month", "day_name", "day"]
                                        )
                                    ])
                                ])
                            ]),

                        ]),


                        html.Div(className="row align-items-center", children=[

                            html.Div(className="col-md-7", children=[
                                dcc.Graph(config=dict(displayModeBar=False),
                                          figure=choropleth_europe_ue()),
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

                            ])

                        ])
                    ]
                ),
            ])
        ])

    ]),


    # -------------------------------------------   DISORDER TYPE   ----------------------------------------------------------------

    html.H3("Armed Conflits in Europe: By Disorder Type", className="mt-5 mb-3"),

    html.Div(className="", children=[
        dmc.Blockquote(
            "After months of military buildup along the Ukrainian border, Russian forces launched a large-scale invasion of Ukraine on February 24, 2022. The escalation of the ensuing armed conflict led to the highest level of political violence recorded in a European country. The surge in violence in Ukraine was accompanied by a staggering human cost, with Ukraine also ranking as the country with the highest number of reported fatalities",
            cite="- Source: Acled", color="white"
        )
    ]),

    html.Div(className="row align-items-center mt-3", children=[

        html.Div(className="col-12 col-md-6 col-xl-5 order-first", children=[
            dcc.Graph(config=dict(displayModeBar=False),
                      figure=disorder_type()),
        ]),

        html.Div(className="col-12 col-xl-2 order-last order-xl-2", children=[
            html.Div(className="row", children=[
                html.Div(className="col-6 col-xl-12 mt-3 mt-xl", children=[
                    dcc.Markdown(
                        """
                        ###### - More than half of conflicts are politically motivated
                        """,

                        className="small_comments",
                    )
                ]),

                html.Div(className="col-6 col-xl-12", children=[
                    dcc.Markdown(
                        """
                        ###### - Dans l'ensemble, le nombre d'attaques terroristes dans
                        
                        Demonstration wars have surpassed political violence in the month of March, considered the most tumultuous month of the year with over 54,677 conflicts, as seen previously.
                        Political violence reached its peak in the month of June, rising to 6,765 conflicts this month"
                        """,

                        className="small_comments",
                    ),
                ])
            ])
        ]),

        html.Div(className="col-12 col-md-6 col-xl-5 order-2 order-xl-3", children=[
            dcc.Graph(config=dict(displayModeBar=False),
                      id="disorder-type-time-series"),
            html.Div(className="selection d-flex justify-content-center", children=[
                dmc.ChipGroup(value="line", id="disorder-graph", children=[
                    dmc.Chip(x, value=y, size="sm", color="red")
                    for x, y in zip(["Line chart", "Bar chart"], ["line", "bar"])
                ])
            ])
        ]),

    ]),


    # ---------------------------------------------  EVENT TYPE  -----------------------------------------------------------------


    html.H3("Armed Conflits in Europe: By Events Type", className="mt-5"),

    html.Div(className="row align-items-center", children=[

        html.Div(className="col-12 col-xl-2 order-last order-xl-first", children=[
            dcc.Markdown(
                """
                Prominent during armed conflicts in Europe are events categorized as Explosions/Remote violence and Protests, showcasing their high frequency.""",

                className="small_comments",
            ),
        ]),

        html.Div(className="col-12 col-md-6 col-xl-5 order-first order-xl-2", children=[
            dcc.Graph(config=dict(displayModeBar=False),
                      id="event-type-time-series"),
            html.Div(className="selection d-flex justify-content-center", children=[
                dmc.ChipGroup(value="line", id="event-graph", children=[
                    dmc.Chip(x, value=y, size="sm", color="red")
                    for x, y in zip(["Line chart", "Bar chart"], ["line", "bar"])
                ])
            ])
        ]),

        html.Div(className="col-12 col-md-6 col-xl-5 order-2 order-xl-last", children=[
            dcc.Graph(config=dict(displayModeBar=False), figure=events_type()),
        ]),

    ]),


    # ------------------------------------   FROM A GEOSPATIAL PERSPECTIVE   -----------------------------------------------------



    html.Div(className="row mt-4 mx-auto", children=[

        html.H5("From a geospatial perspective", className="mb-4"),

        html.Div(className="col-12 col-xl-3 text-center text-xl", children=[
            html.Small("Event Type"),
            html.Div(className="mb-3", children=[
                dcc.Dropdown(
                    id="select-event",
                    options=[{"label": x, "value": x}
                             for x in df.event_type.unique()],
                    value="Protests",
                    placeholder="Choose an event type",
                )
            ])
        ]),

        html.Div(className="col-12 col-md-8 col-xl-5", children=[
            dcc.Graph(id="event-type-mapbox",
                      config=dict(displayModeBar=False)),
        ]),

        html.Div(className="col-12 col-md-4 col-xl-4 mt-3 mt-md", children=[
            dcc.Graph(config=dict(displayModeBar=False),
                      id="distribution-event-type"),
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
                    dcc.Graph(config=dict(displayModeBar=False),
                              id="ranking-bar-country"),
                ]),

                html.Div(className="col-md-12", children=[
                    dcc.Graph(config=dict(displayModeBar=False),
                              id="ranking-bar-city"),
                ])

            ])
        ]),
    ]),


    # ----------------------------------------------------------------------------------------------------------------


    html.H3("The Calendar of Armed Conflicts in Europe", className="my-5 pt-3"),

    html.Div(className="row align-items-center mt-3 mb-5", children=[
        html.Div(className="col-md-6", children=[

            html.Div(className="mt-3", children=[
                dcc.Graph(config=dict(displayModeBar=False),
                          figure=calendar(), id="calendar"),
            ]),

            html.Div(className="my-2", children=[
                dcc.Graph(config=dict(displayModeBar=False),
                          figure=calendar_fatalities(), id="calendar_fatalities"),
            ]),

            dcc.Markdown(
                """
                ###### Conflicts and fatalities every day 
                
                """,

                className="small_comments",
            ),
        ]),

        html.Div(className="col-md-6 justify-content-center mt-4 mt-md", children=[

            html.Div(className="md-inline text-start text-md-center mb-3", children=[
                html.Span(
                    "Europe on", className="text-start text-md-center d-block europe"),
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

            dcc.Graph(config=dict(displayModeBar=False), id="map-calendar"),
        ]),


    ]),


    # ----------------------------------------------------------------------------------------------------------------

    html.Hr(className="my-5"),

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

        html.Span("By Chris Baudelaire .K",
                  className="text-white fw-bold mb-3"),

    ]),
])
