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
from app.config import font_path, static_path
from app.dba.db_helper import get_history_by_symbol
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

    # Create the figure
    fig = go.Figure(data=[trace], layout=layout)

    # Generate HTML content for the Plotly graph
    graph_html = pyo.plot(fig, include_plotlyjs=False, output_type="div")

    return graph_html
