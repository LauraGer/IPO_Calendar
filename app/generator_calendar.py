import calendar
import numpy as np
import os
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
from app.config import font_path, static_path
from app.dba.db_helper import get_entries
from PIL import Image, ImageDraw, ImageFont

# Function to add entries to the calendar image
def add_entries_to_calendar(year, month):
    base_image = os.path.join(static_path, "calendar_empty.png")
    img = Image.open(base_image)
    draw = ImageDraw.Draw(img)

    # Get the calendar data for the specified year and month
    cal = calendar.monthcalendar(year, month)

    # Define calendar cell dimensions based on the base image size
    width, height = img.size
    cell_width = width // 7
    cell_height = height // (len(cal) + 1)
    font_size = 24
    font_24 = ImageFont.truetype(font_path, font_size)
    font_18 = ImageFont.truetype(font_path, 18)
    font_small = ImageFont.truetype(font_path, 13)

    # Draw the calendar entries onto the image
    for week_num, week in enumerate(cal, start=1):
        for day_num, day in enumerate(week, start=1):
            if day != 0:
                x0 = (day_num - 1) * cell_width
                y0 = (week_num - 1) * cell_height

                # Get date (year, month, day)
                date = (year, month, day)
                draw.text((x0 + 2, y0 + 2), str(day), fill="black", font=font_24)
                # Check if date has an entry

                entries = get_entries(year,month)
                if date in entries:
                    entry_text = entries[date]
                    entry_text_with_line_breaks = "\n".join(entry_text[i:i+15] for i in range(0, len(entry_text), 15))  # Insert line break every 15 characters
                    draw.text((x0 + 2, y0 + 25), entry_text_with_line_breaks, fill="red", font=font_18)

    # Save the modified image
    img.save(os.path.join(static_path, "calendar_with_entries.png"))
