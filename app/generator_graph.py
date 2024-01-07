import numpy as np
import os
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
from app.config import font_path, static_path
from app.dba.db_helper import get_history_by_symbol
from datetime import datetime


def build_graph(symbol):

    data = get_history_by_symbol(symbol)

    values = [item[1] for item in data]
    dates = [item[0].strftime('%Y-%m-%d') for item in data]

    # # Create a Plotly trace with hoverinfo
    trace = go.Scatter(
        x=dates,
        y=values,
        mode='lines+markers',
        name='Values over Time',
        hoverinfo='x+y',  # Show both x (date) and y (value) on hover
        text=[f'Date: {date}<br>Value: {value}' for date, value in zip(dates, values)]  # Tooltip text
    )

    # Create the layout
    layout = go.Layout(
        xaxis=dict(title='Date'),
        yaxis=dict(title='Values')
    )

    # Create the figure
    fig = go.Figure(data=[trace], layout=layout)

    # Generate HTML content for the Plotly graph
    graph_html = pyo.plot(fig, include_plotlyjs=False, output_type='div')

    return graph_html
    # Render the HTML template with the graph content
    #return templates.TemplateResponse("stock_graph.html", {"request": request, "graph_html": graph_html})
