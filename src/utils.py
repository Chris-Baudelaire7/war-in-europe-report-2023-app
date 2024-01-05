import pycountry
import pydeck as pdk
import plotly.express as px
import plotly.express as px
import plotly.graph_objects as go
from data_preparation import *


mapbox_access_token = "pk.eyJ1IjoiY2hyaXMtYmF1ZGVsYWlyZSIsImEiOiJjbHB6dWYxb2wxOWdmMnJvOGtzaDVyb3Y2In0.pXQ81pAk9gRoUHXDnNsjJg"


list_months = [
    "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December"
]


update_layout_geo = {
    "geo": dict(
        scope="europe",
        showcountries=False,
        bgcolor="rgba(0,0,0,0)",
        resolution=50,
        projection=dict(type='natural earth'),
    )
}

update_layout_simple = {
    "template": "plotly_dark",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "hovermode": "x",
    "margin": dict(l=0, r=0, t=0, b=30),
}


def render_codes_and_flag(df, input_countries):
    countries, flag = {}, {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_3
        flag[country.name] = country.flag
    codes = [countries.get(country, '') for country in input_countries]
    drapeau = [flag.get(country, '') for country in input_countries]
    df['code'] = codes
    df['flag'] = drapeau
    return df


# Trace choropleth map

def choropleth_europe(df, metric, zmin, zmax, colorscale):
    fig = go.Figure(
        go.Choropleth(
            z=df[metric],
            locations=df["code"],
            colorscale=colorscale,
            showscale=False,
            marker=dict(line=dict(width=.4, color="black")),
            customdata=df,
            zmin=zmin,
            zmax=zmax
        )
    )

    fig.update_layout(
        **update_layout_geo,
        dragmode="lasso",
        height=610,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(autoexpand=True, l=0, r=0, t=0, b=0),
        title={
            "text": (
                f"<b>Top Country most affected<br>by onflict this year</b><br />"
                f"<sup style='color:silver'>as of December 8, 2023"
            ),
            "font": {"family": "serif", "size": 30, "color": "white"},
            "x": 0.9,
            "y": 0.84,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    return fig


# Trace

def timeseries_by_categories(title, category, metric, colors, col_order, graph):
    period = "month"
    dframe = df.groupby([period, category], as_index=False).size()
    columns = list(dframe.groupby([category], as_index=False).size(
    ).sort_values(by=metric)[category].values)

    dframe = dframe.pivot_table(index="month", columns=category, values=metric)
    dframe = (dframe[columns].fillna(0)).sort_values(
        by="month", key=lambda x: pd.to_datetime(x, format='%B'))
    dframe = dframe.iloc[:, col_order]

    if graph == "line":
        fig = px.line(dframe, x=dframe.index, y=dframe.columns)

        for trace, color in zip(fig.data, colors):
            trace.update(mode='lines+markers',
                         line=dict(width=1.7, color=color))

        legend = dict(title=None, x=.6, y=.97)

    else:
        fig = go.Figure()
        for col, color in zip(list(dframe.columns), colors):
            fig.add_traces(
                go.Bar(
                    x=dframe.index, y=dframe[col],
                    marker_color=color, name=col
                )
            )
        legend = dict(title=None, x=0, y=.97)

    fig.update_layout(
        height=400,
        template="plotly_dark",
        legend=legend,
        hovermode="x",
        margin=dict(autoexpand=True, l=0, r=0, b=0, t=80),
        font=dict(size=11, family="serif"),
        xaxis=dict(title=None, showgrid=False),
        yaxis=dict(title=None, showgrid=False),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        title={
            "text": (
                f"<b>{title}</b><br />"
                f"<sup style='color:silver'>All natural disasters occurred: 1970 - 2023"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    return fig


# Trace pie chart

def pie_chart(data, labels, values, title):
    fig = go.Figure(go.Pie(
        labels=data[labels], values=data[values],
        textposition="outside", textinfo="label+percent",
        textfont=dict(size=13.6, family="Lato"),
        marker=dict(colors=px.colors.sequential.Reds_r),
        insidetextorientation='radial',
        pull=[.2]+[0] * 10,
    ))

    fig.update_layout(
        height=450,
        template="plotly_dark",
        showlegend=False,
        margin=dict(autoexpand=True, l=0, r=0, t=100),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        title={
            "text": (
                f"<b>{title}</b><br />"
                f"<sup style='color:silver'>All natural disasters occurred: 1970 - 2023"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    return fig


def conflict_by_month_utils(df, period, title, is_ue=False):
    day_order = ["Monday", "Tuesday", "Wednesday",
                 "Thursday", "Friday", "Saturday", "Sunday"]

    df_occurence = df.groupby([period], as_index=False).size()
    df_fatalities = df.groupby([period], as_index=False)["fatalities"].sum()
    data = pd.merge(df_occurence, df_fatalities, on=[period])
    if period == "month":
        data = data.sort_values(
            by=period, key=lambda x: pd.to_datetime(x, format="%B"))
    elif period == "day_name":
        data[period] = pd.Categorical(
            data[period], categories=day_order, ordered=True)
        data = data.sort_values(by=period)

    else:
        pass

    fig = px.bar(
        data, x=period, y="size", color="size", color_continuous_scale="reds",
        text="size" if period != "day" else None
    )
    fig.update_coloraxes(showscale=False)

    fig.update_traces(textposition="outside", textfont=dict(size=10))

    fig.add_scatter(
        x=data[period], y=data["fatalities"],
        text=data["fatalities"], textposition="top center",
        mode="lines+markers+text" if period != "day" else "lines",
        line=dict(color="white"),
        marker=dict(size=7),
        yaxis="y2" if is_ue else None
    )

    fig.update_layout(
        template="plotly_dark",
        height=300,
        hovermode="x",
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=30, r=0, l=0),
        yaxis=dict(visible=False) if period != "day" else dict(
            showgrid=False, title=None),
        yaxis2=dict(visible=False) if period != "day" else dict(
            showgrid=False, title=None),
        xaxis=dict(nticks=30, title=None),
        font=dict(size=12, family="serif"),
        title={
            "text": (
                f"<b>{title}</b><br />"
                f"<sup style='color:silver'>All natural disasters occurred: 1970 - 2023"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    return fig


def ranking(df, area):
    data = df.groupby([area], as_index=False).size().nlargest(
        columns="size", n=10)
    fig = px.bar(data, x=area, y="size", color="size",
                 color_continuous_scale="reds", text="size")
    fig.update_coloraxes(showscale=False)

    fig.update_traces(textposition="outside", textfont=dict(size=10))

    fig.update_layout(
        template="plotly_dark",
        height=200,
        hovermode="x",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=0, b=0, r=0, l=0),
        yaxis=dict(showgrid=False, visible=False),
        xaxis=dict(nticks=30, title=None),
        font=dict(size=12, family="serif"),
        title={
            "text": (
                f"<b>Top 10 most countries affected</b><br />"
                f"<sup style='color:silver'>War in 2023 to 8, November</sup>"
            ),
            "font": {"family": "serif", "size": 14, "color": "white"},
            "x": 0.98,
            "y": 0.8,
            "xanchor": "right",
            "yanchor": "top",
        }
    )

    return fig


def heatmap_month(df):
    data = df.groupby(["month", "day_name"], as_index=False).size()
    fig = go.Figure(
        go.Heatmap(
            z=data["size"],
            y=data["day_name"],
            x=data["month"],
            colorscale="reds",
            showscale=False,
            text=data["size"],
            texttemplate="%{text}",
        ),
    )

    list_months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    days_orderd = ['Monday', 'Tuesday', 'Wednesday',
                   'Thursday', 'Friday', 'Saturday', 'Sunday']

    fig.update_xaxes(categoryorder='array', categoryarray=list_months)
    fig.update_yaxes(categoryorder='array', categoryarray=days_orderd)

    fig.update_layout(
        update_layout_simple,
        margin=dict(autoexpand=True, l=0, r=0, t=60, b=45),
        height=350,
        xaxis=dict(
            showgrid=False,
            showticklabels=True,
            ticks="outside",
            tickfont=dict(
                color="white",
            )
        ),

        yaxis=dict(
            showticklabels=True,
            ticks="inside",
            ticklen=5,
            tickcolor="white"
        ),
        font=dict(family="serif", color="white", size=10),
        title={
            "text": (
                f"<b>Average Armed Conflicts Per Day in Europe</b><br />"
                f"<sup style='color:silver'>All natural disasters occurred: 1970 - 2023"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    return fig


def ranking_mapbox_utils(data):

    initial_view_state = pdk.data_utils.compute_view(
        df[["longitude", "latitude"]])

    a = set(state_id_map.keys())
    b = set(data["country"])
    states = list(a.intersection(b))

    data = data[data["country"].isin(states)]
    data["id"] = data["country"].apply(lambda x: state_id_map[x])
    data["events"] = data["size"].values

    fig = go.Figure(
        go.Choroplethmapbox(
            z=data["events"]/4,
            locations=data["id"],
            geojson=data_country_geojson,
            colorscale="reds",
            # marker_line_color='white',
            showscale=False
        )
    )

    fig.update_layout(
        height=400,
        margin=dict(autoexpand=True, l=0, r=0, t=0, b=0),
        mapbox=dict(
            center={"lat": initial_view_state.latitude,
                    "lon": initial_view_state.longitude},
            accesstoken=mapbox_access_token,
            style="mapbox://styles/mapbox/satellite-streets-v11",
            zoom=2,
            pitch=40
        ),
    )

    return fig
