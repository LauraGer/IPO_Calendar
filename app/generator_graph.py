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
import plotly.graph_objs as go
import plotly.io as pio
from dba.db_helper import get_history_by_symbol, get_symbol_details
from datetime import datetime


def build_graph(symbol):
    try:
        data = get_history_by_symbol(symbol)
        dates = [item[1].strftime("%Y-%m-%d") for item in data]
        open = [item[2] for item in data]
        high = [item[3] for item in data]
        low = [item[4] for item in data]
        close = [item[5] for item in data]
        # # Create a Plotly trace with hoverinfo
        trace_low = go.Scatter(
            x=dates,
            y=open,
            mode="lines+markers",
            name="low over Time",
            hoverinfo="x+y",  # Show both x (date) and y (value) on hover
            text=[f"Date: {date}<br>Value: {value}" for date, value in zip(dates, low)],  # Tooltip text
            marker=dict(size=6, color='#FF5733'),
            line=dict(width=6)  # Set line width for trace 2
        )

        trace_high = go.Scatter(
            x=dates,
            y=high,
            mode="lines+markers",
            name="high over Time",
            hoverinfo="x+y",  # Show both x (date) and y (value) on hover
            text=[f"Date: {date}<br>Value: {value}" for date, value in zip(dates, high)],  # Tooltip text
            marker=dict(size=6, color='#46de9b', symbol="circle"),  # Set marker color for trace 2
            line=dict(width=6)
        )
        # Create the layout
        layout = go.Layout(
            xaxis=dict(title="Date"),
            yaxis=dict(title="Low & High")
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
            xaxis=dict(
                #title="January-June<br>Year",
                showgrid=False,
                tickmode='array',
                tickvals=dates[::6],  # Set tick values every quarter
                ticktext=x_ticker_text,
            ),
            yaxis=dict(title="CURRENCY???", showgrid=True),
            plot_bgcolor="white",  # Set the plot background color
        )
        dotted_lines = []
        for date in dates:
            dotted_lines.append({
                'type': 'line',
                'x0': date,
                'x1': date,
                'y0': min(open),
                'y1': max(open),
                'line': {
                    'color': 'rgba(0, 0, 0, 0.2)',
                    'dash': 'dot',
                },
            })
        layout['shapes'] = dotted_lines
        # Create the figure
        fig = go.Figure(data=[trace_high, trace_low], layout=layout)
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
        graph_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

        return graph_html

    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")
