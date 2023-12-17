import finnhub
import pandas as pd
from datetime import date, timedelta

#import requests

# id = "ckim1nhr01qlj9q73cvgckim1nhr01qlj9q73d00"
# r = requests.get("https://finnhub.io/api/v1/calendar/ipo?from=2020-01-01&to=2020-04-30&token=ckim1nhr01qlj9q73cvgckim1nhr01qlj9q73d00")
# print(r.content)
today = date.today()
start=today - timedelta(days=30)
end=today + timedelta(days=30)

def getIPOData(start, end):
    finnhub_client = finnhub.Client(api_key="ckim1nhr01qlj9q73cvgckim1nhr01qlj9q73d00")

    ipo_data = finnhub_client.ipo_calendar(_from=start, to=end)

    df = pd.json_normalize(ipo_data, "ipoCalendar")

    return df

ipo_data=getIPOData(start,end)

df = pd.DataFrame(ipo_data)
df = df.set_index("name")
print(df)
print(df.columns())