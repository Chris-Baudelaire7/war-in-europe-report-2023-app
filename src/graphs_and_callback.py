import datetime as dt
import plotly.figure_factory as ff
from plotly_calplot import calplot
from dash import Input, Output, callback, html
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib.pyplot as plt
from data_preparation import *
from utils import *


# --------------------------------------------------- Pydeck ---------------------------------------------------------

def total_events_Deck():
    # data
    data_sum = df.groupby(["longitude", "latitude", "location"], as_index=False)[
        ["fatalities"]].sum()
    data_occurence = df.groupby(
        ["longitude", "latitude", "location"], as_index=False).size()
    data = pd.merge(data_sum, data_occurence, on=[
                    "longitude", "latitude", "location"])
    data["metric"] = data["fatalities"] + data["size"]

    # Setting the viewport location
    initial_view_state = pdk.data_utils.compute_view(
        data[["longitude", "latitude"]])
    initial_view_state.zoom = 3
    initial_view_state.pitch = 50
    initial_view_state.bearing = 20

    # Define the layer to display on a map
    hexagonlayer = pdk.Layer(
        "HexagonLayer",
        data=data,
        get_position=["longitude", "latitude"],
        get_elevation="metric",
        elevation_scale=1,
        elevation_range=[40000, 1590000],
        pickable=True,
        radius=6000,
        extruded=True,
        auto_highlight=True,
    )

    heatmapLayer = pdk.Layer(
        "HeatmapLayer",
        data=data,
        opacity=1,
        get_position=["longitude", "latitude"],
        # aggregation="MEAN",
        threshold=1,
        get_weight="metric",
        radius_pixels=150,
    )

    tooltip = {
        "html": "<b>Location: {location}</b> <br> <b>Armed Conficts: {size}</b> <br> <b>Fatalities: {fatalities}</b>",
        "style": {
            "background": "white",
            "color": "black",
            "font-family": 'serif, Arial',
            "z-index": "10000"
        },
    }

    maps = pdk.Deck(
        layers=[hexagonlayer, heatmapLayer],
        tooltip=tooltip,
        initial_view_state=initial_view_state,
        **map_config("mapbox://styles/mapbox/satellite-streets-v11")
    )

    return maps, tooltip


# ------------------------------------------------ Choropleth ----------------------------------------------------------

def choropleth_europe_globale():

    d = df.groupby(["country"], as_index=False).size()
    input_countries = d["country"].unique()
    d = render_codes_and_flag(d, input_countries)

    fig = choropleth_europe(d, "size", d['size'].min(
    ), d['size'].max()/4, px.colors.sequential.Reds)

    return fig


def choropleth_europe_ue():

    d = df_ue.groupby(["country"], as_index=False).size()
    input_countries = d["country"].unique()
    d = render_codes_and_flag(d, input_countries)

    fig = choropleth_europe(d, "size", d['size'].min(
    ), d['size'].max(), px.colors.sequential.Reds)

    return fig


@callback(
    Output("event-type-choropleth", "figure"),
    Input("select-event", "value")
)
def choropleth_europe_by_event_type(event_type):

    d = df[df["event_type"] == event_type]
    d = d.groupby(["country"], as_index=False).size()
    input_countries = d["country"].unique()
    d = render_codes_and_flag(d, input_countries)

    fig = choropleth_europe(d, "size", d['size'].min(
    ), d['size'].max(), px.colors.sequential.YlOrRd)

    return fig


@callback(
    Output("ranking-bar-country", "figure"),
    Output("ranking-bar-city", "figure"),
    Input("select-event", "value")
)
def update_bar_chart_rank(event):

    def graph(area):
        data = (df[df["event_type"] == event]).groupby(
            [area], as_index=False).size().nlargest(columns="size", n=10)
        fig = px.bar(data, x=area, y="size", color="size",
                     color_continuous_scale="reds", text="size")
        fig.update_coloraxes(showscale=False)
        fig.update_traces(textposition="outside", textfont=dict(size=10))

        fig.update_layout(
            template="plotly_dark",
            height=265,
            hovermode="x",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=0, b=0, r=0, l=0),
            yaxis=dict(showgrid=False, visible=False),
            xaxis=dict(nticks=30, title=None),
            font=dict(size=12, family="serif"),
            title={
                "text": (
                    f"<b>Top 10 most {area} affected</b><br />"
                ),
                "font": {"family": "serif", "size": 14, "color": "white"},
                "x": 0.98,
                "y": 0.9,
                "xanchor": "right",
                "yanchor": "top",
            }
        )

        return fig

    country_graph, city_graph = graph("country"), graph("location")

    return country_graph, city_graph

# -------------------------------------------------- Mapbox ---------------------------------------------------------


@callback(
    Output("event-type-mapbox", "figure"),
    Input("select-event", "value")
)
def mapbox(event_type):
    dframe = df[df["event_type"] == event_type].groupby(
        ["latitude", "longitude"], as_index=False).size()

    initial_view_state = pdk.data_utils.compute_view(
        dframe[["longitude", "latitude"]])

    fig = go.Figure(
        go.Densitymapbox(
            lat=dframe.latitude, lon=dframe.longitude, z=dframe["size"],
            colorscale="rainbow", showscale=False, zmin=-2000, radius=30
        ),
    )

    if event_type in ["Battles"]:
        zoom, pitch = 5.5, 50
    elif event_type in ["Explosions/Remote violence"]:
        zoom, pitch = 5, 50
    else:
        zoom, pitch = 3, 30

    fig.update_layout(
        autosize=True,
        height=300,
        hovermode='closest',
        margin=dict(autoexpand=True, l=0, r=0, b=0, t=0),
        mapbox=dict(
            center={"lat": initial_view_state.latitude,
                    "lon": initial_view_state.longitude},
            accesstoken="YOUR_MAPBOX_ACCESS_TOKEN",
            style="mapbox://styles/mapbox/satellite-streets-v11",
            zoom=zoom,
            pitch=pitch
        ),
    )

    return fig


def mapbox_ue():
    dframe = df_ue.groupby(["latitude", "longitude"], as_index=False).size()

    initial_view_state = pdk.data_utils.compute_view(
        dframe[["longitude", "latitude"]])

    fig = go.Figure(
        go.Densitymapbox(
            lat=dframe.latitude, lon=dframe.longitude, z=dframe["size"],
            colorscale="rainbow", showscale=False, zmin=-2000, radius=30
        ),
    )

    fig.update_layout(
        autosize=True,
        height=310,
        hovermode='closest',
        margin=dict(autoexpand=True, l=0, r=0, b=0, t=0),
        mapbox=dict(
            center={"lat": initial_view_state.latitude,
                    "lon": initial_view_state.longitude},
            accesstoken="YOUR_MAPBOX_ACCESS_TOKEN",
            style="mapbox://styles/mapbox/satellite-streets-v11",
            zoom=2.5,
            pitch=40
        ),
    )

    return fig


def mapbox_ukraine():
    dframe = df[df["country"] == "Ukraine"].groupby(
        ["latitude", "longitude"], as_index=False).size()

    initial_view_state = pdk.data_utils.compute_view(
        dframe[["longitude", "latitude"]])

    fig = go.Figure(
        go.Densitymapbox(
            lat=dframe.latitude, lon=dframe.longitude, z=dframe["size"],
            colorscale="rainbow", showscale=False, zmin=-2000, radius=30
        ),
    )

    fig.update_layout(
        autosize=True,
        height=310,
        hovermode='closest',
        margin=dict(autoexpand=True, l=0, r=0, b=0, t=0),
        mapbox=dict(
            center={"lat": initial_view_state.latitude,
                    "lon": initial_view_state.longitude},
            accesstoken="YOUR_MAPBOX_ACCESS_TOKEN",
            style="mapbox://styles/mapbox/satellite-streets-v11",
            zoom=4.6,
            pitch=40
        ),
    )

    return fig


@callback(
    Output("map-calendar", "figure"),
    Input("select-date", "date")
)
def mapbox_calendar(date):
    data = df[df["event_date"] == date]
    data = data.groupby(["latitude", "longitude"], as_index=False).size()
    initial_view_state = pdk.data_utils.compute_view(
        data[["longitude", "latitude"]])

    fig = go.Figure(
        go.Densitymapbox(
            lat=data.latitude, lon=data.longitude, z=data["size"],
            colorscale="rainbow", showscale=False, zmin=-2000, radius=30
        ),
    )

    fig.update_layout(
        autosize=True,
        height=310,
        hovermode='closest',
        margin=dict(autoexpand=True, l=0, r=0, b=0, t=0),
        mapbox=dict(
            center={"lat": initial_view_state.latitude,
                    "lon": initial_view_state.longitude},
            accesstoken="YOUR_MAPBOX_ACCESS_TOKEN",
            style="mapbox://styles/mapbox/satellite-streets-v11",
            zoom=2.8,
            pitch=40
        ),
    )

    return fig


# ------------------------------------------------- Bar Charts --------------------------------------------------------

@callback(
    Output("bar-period", "figure"),
    Input("select-period", "value")
)
def conflict_by_month(value):
    return conflict_by_month_utils(df, value, "Total conflicts and fatalities by month")


@callback(
    Output("bar-period-wur", "figure"),
    Input("select-period-wur", "value")
)
def trends_month_day(value):
    return conflict_by_month_utils(df_ue, value, "Total conflicts and fatalities by month", True)


def conflict_by_month_in_ue():
    return conflict_by_month_utils(df_ue, "month", "Total conflicts and fatalities by month", True)


def ranking_country():
    return ranking(df, "country")


def ranking_country_ue():
    return ranking(df_ue, "country")


def ranking_city():
    return ranking(df, "location")


def ranking_city_ue():
    return ranking(df_ue, "location")

# fig.update_xaxes(categoryorder='array', categoryarray=days_orderd)


# -------------------------------------------------- Timesries ----------------------------------------------------------

@callback(
    Output("timeseries", "figure"),
    Input("period-type", "value")
)
def timeseries(period):
    year = 2023
    data = df.groupby(["dayofyear"], as_index=False).size()
    data["fatalities"] = (df.groupby("dayofyear", as_index=False)[
                          "fatalities"].sum())["fatalities"]
    data["date"] = data["dayofyear"].apply(
        lambda x: dt.datetime(year, 1, 1) + dt.timedelta(days=x - 1))
    data["moving_average"] = data["size"].rolling(window=7).mean()
    data["moving_average_fatalities"] = data["fatalities"].rolling(
        window=7).mean()

    fig = go.Figure()

    if period == "daily":

        subtitle = "Conflicts and fatalities day per day in 2023"

        fig.add_scatter(
            x=data["date"], y=data["size"],
            line=dict(color="orangered", width=1),
            name="Armed conflict (Raw data)"
        )

        fig.add_scatter(
            x=data["date"], y=data["fatalities"],
            line=dict(color="firebrick", width=1.86),
            name="Fatalities (Raw data)"
        )

    elif period == "weekly_mean_line":
        fig.add_scatter(
            x=data["date"], y=data["moving_average"],
            line=dict(color="orangered", width=1.86),
            name="Armed conflict (Weekly mean)"
        )

        fig.add_scatter(
            x=data["date"], y=data["moving_average_fatalities"],
            line=dict(color="firebrick", width=1.86),
            name="Fatalities (Weekly mean)",
        )
        subtitle = "Weekly average of conflicts and casualties"
    else:
        fig = px.area(data, x="date", y=[
                      "moving_average_fatalities", "moving_average"])
        for trace, color in zip(fig.data, ["orangered", "firebrick"]):
            trace.update(line=dict(color=color))
        subtitle = "Weekly average of conflicts and fatalities"

    months_with_days = {
        month: (
            dt.datetime(year, month, 1),
            dt.datetime(
                year, month, 28 if month == 2 else 30 if month in [
                    4, 6, 9, 11] else 31
            ),
        )
        for month in range(1, 13)
    }

    # Loop over months and add a shape for each month
    for month, days in months_with_days.items():
        # Define background color
        bg_color = "rgba(0, 0, 0, 0)" if (month % 2) == 0 else "#111"

        fig.add_shape(
            type="rect", yref="paper",
            x0=days[0], x1=days[1],
            y0=0, y1=1,
            fillcolor=bg_color,
            layer="below",
            line_width=0,
        )

    fig.update_layout(
        **update_layout_t50_b30,
        height=350,
        font=dict(size=11, family="serif"),
        legend=dict(x=.58, y=1, title=None),
        xaxis=dict(
            showgrid=False,
            dtick="M1",
            tickformat="%B",
            hoverformat="%e %B",
            ticklabelmode="period",
            tickfont=dict(size=11, family="serif")
        ),
        yaxis=dict(showgrid=False),
        title={
            "text": (
                f"<b>Daily trends of events and fatalities</b><br />"
                f"<sup style='color:silver'>{subtitle}"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": .93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    return fig


@callback(
    Output("uk_vs_ue", "figure"),
    Input("type-period", "value")
)
def world_vs_ukraine(metric):
    year = 2023
    df_ukraine = df[df["country"] == "Ukraine"]

    if metric == "weekly_mean_event":
        df_ukraine = (df_ukraine.groupby(["dayofyear"], as_index=False).size()).rename(
            columns={"size": "ukraine"})
        df_rest_of_europe = (df_ue.groupby(
            ["dayofyear"], as_index=False).size()).rename(columns={"size": "ue"})
    else:
        df_ukraine = (df_ukraine.groupby(["dayofyear"], as_index=False)[
            ["fatalities"]].sum()).rename(columns={"fatalities": "ukraine"})
        df_rest_of_europe = (df_ue.groupby(["dayofyear"], as_index=False)[
            "fatalities"].sum()).rename(columns={"fatalities": "ue"})

    data = pd.merge(df_ukraine, df_rest_of_europe, on="dayofyear")

    data["date"] = data["dayofyear"].apply(
        lambda x: dt.datetime(year, 1, 1) + dt.timedelta(days=x - 1))

    data["moving_average_ukraine"] = data["ukraine"].rolling(window=7).mean()
    data["moving_average_ue"] = data["ue"].rolling(window=7).mean()

    fig = go.Figure()

    fig.add_scatter(
        x=data["date"], y=data["moving_average_ue"],
        line=dict(color="orangered", width=1.86),
        name="Rest of Europe"
    )

    fig.add_scatter(
        x=data["date"], y=data["moving_average_ukraine"],
        line=dict(color="firebrick", width=1.86),
        name="Ukraine"
    )

    months_with_days = {
        month: (
            dt.datetime(year, month, 1),
            dt.datetime(
                year, month, 28 if month == 2 else 30 if month in [
                    4, 6, 9, 11] else 31
            ),
        )
        for month in range(1, 13)
    }

    # Loop over months and add a shape for each month
    for month, days in months_with_days.items():
        # Define background color
        bg_color = "rgba(0, 0, 0, 0)" if (month % 2) == 0 else "#111"

        fig.add_shape(
            type="rect", yref="paper",
            x0=days[0], x1=days[1],
            y0=0, y1=1,
            fillcolor=bg_color,
            layer="below",
            line_width=0,
        )

    fig.update_layout(
        **update_layout_t50_b30,
        height=350,
        font=dict(size=11, family="serif"),
        legend=dict(x=.58, y=1, title=None),
        xaxis=dict(
            showgrid=False,
            dtick="M1",
            tickformat="%B",
            hoverformat="%e %B",
            ticklabelmode="period",
            tickfont=dict(size=11, family="serif")
        ),
        yaxis=dict(showgrid=False),
        title={
            "text": (
                f"<b>Weekly Trend of events and fatalities</b><br />"
                f"<sup style='color:silver'>Ukraine vs The rest of Europe"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": .93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    return fig


# -------------------------------------------------- Distribution -------------------------------------------------------

@callback(
    Output('distribution_events', 'figure'),
    Output('distribution_fatalities', 'figure'),
    Input('daq-slider-events', 'value'),
    Input('daq-slider-fatalities', 'value')
)
def distribution_ev_fat(bin_ev, bin_fat):
    cause, period = "size", "dayofyear"

    data1 = df.groupby([period], as_index=False).size()
    data2 = df.groupby([period], as_index=False)["fatalities"].sum()

    x = data1[cause].values
    y = data2["fatalities"].values

    def dist(val, bin_size, name, color, title, subtitle):
        hist_data = [val]
        group_labels = [name]
        fig = ff.create_distplot(hist_data, group_labels, bin_size=bin_size, histnorm="", show_curve=False,
                                 show_rug=False, curve_type="normal", colors=[color])

        fig.update_layout(
            **update_layout_simple,
            bargap=.1,
            font={"family": "serif", "size": 14},
            height=290,
            showlegend=False,
            yaxis=dict(title="Frequence", showgrid=False),
            xaxis=dict(title="Nombre d'attaque par jour"),
            title={
                "text": (
                    f"<b>{title}</b><br />"
                    f"<sup style='color:silver'>{subtitle}"
                ),
                "font": {"family": "serif", "size": 20, "color": "white"},
                "x": 0.98,
                "y": 0.9,
                "xanchor": "right",
                "yanchor": "top",
            },
            dragmode="select"
        )

        return fig

    fig_event = dist(x, bin_ev, "Events", "orangered",
                     "Frequency of Conflicts<br>in Europe", "All wars from January 1st to December 8th")
    fig_fatalities = dist(y, bin_fat, "Fatalities", "firebrick",
                          "Frequency of Fatalities<br>in Europe", "All fatalities from January 1st to December 8th")

    return fig_event, fig_fatalities


@callback(
    Output("distribution-event-type", "figure"),
    Input("select-event", "value")
)
def distribution_events_type(event_type):
    cause, period = "size", "dayofyear"

    data = df[df["event_type"] == event_type].groupby(
        [period], as_index=False).size()

    x = data[cause].values
    hist_data = [x]
    group_labels = ['distplot']

    bin_size = 10 if event_type == "Protests" else 1

    fig = ff.create_distplot(hist_data, group_labels, bin_size=bin_size, histnorm="", show_curve=False,
                             show_rug=False, curve_type="normal", colors=["firebrick"])

    fig.update_layout(
        **update_layout_simple,
        bargap=.1,
        font={"family": "serif", "size": 14},
        height=280,
        showlegend=False,
        yaxis=dict(title="Frequence", showgrid=False),
        xaxis=dict(title="Nombre d'attaque par jour"),
        title={
            "text": (
                f"<b>Frequency of Conflicts</b><br />"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    return fig


def distribution_conflict_ue():
    cause, period = "size", "dayofyear"

    data_ue = df_ue.groupby([period], as_index=False).size()
    data_ukraine = df[df["country"] == "Ukraine"].groupby(
        [period], as_index=False).size()

    x = data_ue[cause].values
    y = data_ukraine[cause].values
    hist_data = [x, y]
    group_labels = ['Other countries', 'Ukraine']

    fig = ff.create_distplot(hist_data, group_labels, bin_size=10, histnorm="", show_curve=False,
                             show_rug=False, curve_type="normal", colors=["firebrick", "orangered"])

    fig.update_layout(
        **update_layout_simple,
        bargap=.1,
        font={"family": "serif", "size": 14},
        height=280,
        showlegend=False,
        yaxis=dict(title=None, showgrid=False),
        xaxis=dict(title="Nombre d'attaque par jour"),
        title={
            "text": (
                f"<b>Frequency of conflicts<br>in Euope</b><br />"
                f"<sup style='color:silver'>Ukraine vs Rest of Europe"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    return fig


# ------------------------------------------------------ Heatmap --------------------------------------------------------


def heatmap_month_all_countries():
    return heatmap_month(df)


def heatmap_month_without_uk_and_rus():
    return heatmap_month(df_ue)


# ------------------------------------------------ Pie Charts -------------------------------------------------------------


def disorder_type():
    labels, values = "disorder_type", "count"
    data = df[labels].value_counts().to_frame().reset_index()
    return pie_chart(data, labels, values, "Distribution of Disorder Types")


def events_type():
    labels, values = "event_type", "count"
    data = df[labels].value_counts().to_frame().reset_index()
    return pie_chart(data, labels, values, "Distribution of Event Types")


@callback(
    Output("rate_deaths", "figure"),
    Input("area", "value")
)
def rate_deaths(value):
    dframe = df.copy() if value == "all" else df_ue.copy()
    labels, values, n = "country", "fatalities", 1
    data = dframe.groupby([labels], as_index=False)[
        values].sum().sort_values(by=values, ascending=False)
    other = data.iloc[n:][values].sum()
    new_row = pd.DataFrame(
        {"country": ['Other<br>countries'], values: [other]})
    data = pd.concat([data.iloc[:n], new_row], ignore_index=True)

    return pie_chart(data, labels, values, "Death rate")


# ---------------------------------------------- Line (+ scatter) Charts ---------------------------------------------------

@callback(
    Output("disorder-type-time-series", "figure"),
    Input("disorder-graph", "value")
)
def disorder_type_time_series(graph):
    title = "Evolution of disorder types per month"
    colors = ['rgb(252,187,161)', 'rgb(251,106,74)',
              'rgb(203,24,29)', 'rgb(103,0,13)'][::-1]
    return timeseries_by_categories(title, "disorder_type", "size", colors, [2, 1, 3, 0], graph)


@callback(
    Output("event-type-time-series", "figure"),
    Input("event-graph", "value")
)
def event_type_time_series(graph):
    title = "Evolution of event types per month"
    colors = ['rgb(255,245,240)', 'rgb(254,224,210)', 'rgb(252,187,161)',
              'rgb(251,106,74)', 'rgb(203,24,29)', 'rgb(103,0,13)'][::-1]

    return timeseries_by_categories(title, "event_type", "size", colors, [1, 2, 0, 4, 3, 5], graph)


# ------------------------------------------------------- Calendar -----------------------------------------------------------

def calendar():
    data = df.groupby("event_date", as_index=False).size()
    data["event_date"] = pd.to_datetime(data["event_date"])

    fig = calplot(data, x="event_date", y="size", dark_theme=True, colorscale="reds",
                  month_lines_color="black", month_lines_width=3, total_height=250)
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, b=0, r=0, l=0),

        title={
            "text": (
                f"<b>2023 Wars Calendar</b><br />"
                f"<sup style='color:silver'>All wars perpetrated in Europe"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        }
    )

    return fig


def calendar_fatalities():
    data = df.groupby("event_date", as_index=False)["fatalities"].sum()
    data["event_date"] = pd.to_datetime(data["event_date"])

    fig = calplot(data, x="event_date", y="fatalities", dark_theme=True, colorscale="ylorrd",
                  month_lines_color="black", month_lines_width=3, total_height=250)
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, b=0, r=0, l=0),

        title={
            "text": (
                f"<b>2023 Fatalities Calendar</b><br />"
                f"<sup style='color:silver'>All fatalities due to conflict in Europe"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    return fig


@callback(
    Output("select-date", "date"),
    Input("calendar", "clickData"),
    prevent_initial_call=True
)
def update_date(clickData):
    date = clickData["points"][0]["customdata"][0] if clickData else None
    return date
