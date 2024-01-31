"""
Copyright 2023 Laura Gerlach

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import numpy as np
import os
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
import plotly.io as pio
from app.config import font_path, static_path
from dba.db_helper import get_history_by_symbol, get_symbol_details
from datetime import datetime


def build_graph(symbol):

    data = get_history_by_symbol(symbol)

    values = [item[1] for item in data]
    dates = [item[0].strftime("%Y-%m-%d") for item in data]

    # # Create a Plotly trace with hoverinfo
    trace = go.Scatter(
        x=dates,
        y=values,
        mode="lines+markers",
        name="Values over Time",
        hoverinfo="x+y",  # Show both x (date) and y (value) on hover
        text=[f"Date: {date}<br>Value: {value}" for date, value in zip(dates, values)]  # Tooltip text
    )

    # Create the layout
    layout = go.Layout(
        xaxis=dict(title="Date"),
        yaxis=dict(title="Values")
    )

    details = get_symbol_details(symbol)
    if details:
        title_text = f"Details: {details}"
    else:
        title_text = "No details about this stock available."
    # define x axe ticker text for every 6. month
    x_ticker_text = [f"{date.split('-')[1]}<br>{date.split('-')[0]}" for date in dates if date.split('-')[1] in ['01', '06']]

    # Create the figure
    layout = go.Layout(
        title=title_text,
        #xaxis=dict(title="Date", showgrid=True),
        xaxis=dict(
            #title="January-June<br>Year",
            showgrid=False,
            tickmode='array',
            tickvals=dates[::6],  # Set tick values every quarter
            ticktext=x_ticker_text,
        ),
        yaxis=dict(title="CURRENCY???", showgrid=True),
      #  margin=dict(l=0, r=0, b=50, t=30),
        plot_bgcolor="white",  # Set the plot background color
    )

    dotted_lines = []
    for date in dates:
        dotted_lines.append({
            'type': 'line',
            'x0': date,
            'x1': date,
            'y0': min(values),
            'y1': max(values),
            'line': {
                'color': 'rgba(0, 0, 0, 0.2)',
                'dash': 'dot',
            },
        })
    layout['shapes'] = dotted_lines
    # Create the figure
    fig = go.Figure(data=[trace], layout=layout)

    # Update the figure style
    # mint: https://www.colorhexa.com/aaf0d1
    fig.update_traces(marker=dict(size=8, color='#46de9b', symbol="circle"), line=dict(width=8))

    # Update the layout style with the custom font
    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=12, color="black"),
    )
    # Update the layout style
    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=12, color="black"),
        paper_bgcolor="rgba(0,0,0,0)",  # Set the paper background color to transparent
        hoverlabel=dict(bgcolor="white", font=dict(family="Arial, sans-serif", size=24, color="black")),
    )


    # Generate HTML content for the Plotly graph
    #graph_html = pyo.plot(fig, include_plotlyjs=False, output_type="div")
    graph_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

    return graph_html
