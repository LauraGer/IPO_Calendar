import os

#load environment variables
HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("APP_DB")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")

DATABASE_URL ={f"postgresql://{USER}:{PASSWORD}@{HOST}:5432/{DATABASE}"}
ALPHA_MONTHLY_URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=##SYMBOL##&apikey={ALPHA_VANTAGE_KEY}"


json = {
    "Meta Data": {
        "1. Information": "Monthly Prices (open, high, low, close) and Volumes",
        "2. Symbol": "GBS",
        "3. Last Refreshed": "2024-01-05",
        "4. Time Zone": "US/Eastern"
    },
    "Monthly Time Series": {
        "2024-01-05": {
            "1. open": "0.3274",
            "2. high": "0.3500",
            "3. low": "0.2945",
            "4. close": "0.3166",
            "5. volume": "2376316"
        },
        "2023-12-29": {
            "1. open": "0.3710",
            "2. high": "0.5290",
            "3. low": "0.2288",
            "4. close": "0.3379",
            "5. volume": "115303332"
        },
        "2023-11-30": {
            "1. open": "0.2191",
            "2. high": "0.7806",
            "3. low": "0.2011",
            "4. close": "0.4200",
            "5. volume": "372406929"
        },
        "2023-10-31": {
            "1. open": "0.4300",
            "2. high": "0.5300",
            "3. low": "0.2001",
            "4. close": "0.2163",
            "5. volume": "23652589"
        },
        "2023-09-29": {
            "1. open": "1.8400",
            "2. high": "1.9122",
            "3. low": "1.0200",
            "4. close": "1.0300",
            "5. volume": "651506"
        },
        "2023-08-31": {
            "1. open": "1.8900",
            "2. high": "2.0000",
            "3. low": "1.3800",
            "4. close": "1.7600",
            "5. volume": "988122"
        },
        "2023-07-31": {
            "1. open": "2.7650",
            "2. high": "3.2900",
            "3. low": "1.7600",
            "4. close": "1.8000",
            "5. volume": "1312159"
        },
        "2023-06-30": {
            "1. open": "2.7200",
            "2. high": "3.7400",
            "3. low": "2.6591",
            "4. close": "2.7800",
            "5. volume": "1321986"
        },
        "2023-05-31": {
            "1. open": "2.4594",
            "2. high": "4.1000",
            "3. low": "2.0900",
            "4. close": "2.7300",
            "5. volume": "5301643"
        },
        "2023-04-28": {
            "1. open": "2.7800",
            "2. high": "3.2400",
            "3. low": "2.3600",
            "4. close": "2.4001",
            "5. volume": "865785"
        },
        "2023-03-31": {
            "1. open": "6.0900",
            "2. high": "6.5300",
            "3. low": "2.6263",
            "4. close": "2.9000",
            "5. volume": "1135136"
        },
        "2023-02-28": {
            "1. open": "0.8200",
            "2. high": "11.2900",
            "3. low": "0.5700",
            "4. close": "6.1000",
            "5. volume": "6558532"
        },
        "2023-01-31": {
            "1. open": "0.1850",
            "2. high": "1.6000",
            "3. low": "0.1800",
            "4. close": "0.8493",
            "5. volume": "193680224"
        },
        "2022-12-30": {
            "1. open": "0.3100",
            "2. high": "0.4435",
            "3. low": "0.1700",
            "4. close": "0.1999",
            "5. volume": "1587934"
        },
        "2022-11-30": {
            "1. open": "0.4400",
            "2. high": "0.4789",
            "3. low": "0.3010",
            "4. close": "0.3555",
            "5. volume": "631414"
        },
        "2022-10-31": {
            "1. open": "0.4440",
            "2. high": "0.7100",
            "3. low": "0.4103",
            "4. close": "0.4403",
            "5. volume": "1449610"
        },
        "2022-09-30": {
            "1. open": "0.6020",
            "2. high": "0.6159",
            "3. low": "0.3600",
            "4. close": "0.4200",
            "5. volume": "1174086"
        },
        "2022-08-31": {
            "1. open": "0.7600",
            "2. high": "0.7868",
            "3. low": "0.5600",
            "4. close": "0.6350",
            "5. volume": "1033823"
        },
        "2022-07-29": {
            "1. open": "0.7071",
            "2. high": "0.8000",
            "3. low": "0.6230",
            "4. close": "0.7174",
            "5. volume": "994400"
        },
        "2022-06-30": {
            "1. open": "0.5880",
            "2. high": "0.8200",
            "3. low": "0.5320",
            "4. close": "0.6620",
            "5. volume": "1872108"
        },
        "2022-05-31": {
            "1. open": "0.6128",
            "2. high": "0.7600",
            "3. low": "0.5300",
            "4. close": "0.5800",
            "5. volume": "2662150"
        },
        "2022-04-29": {
            "1. open": "0.7999",
            "2. high": "1.5400",
            "3. low": "0.6000",
            "4. close": "0.6128",
            "5. volume": "34539313"
        },
        "2022-03-31": {
            "1. open": "0.6661",
            "2. high": "1.2500",
            "3. low": "0.5608",
            "4. close": "0.7823",
            "5. volume": "131467162"
        },
        "2022-02-28": {
            "1. open": "0.9209",
            "2. high": "1.0800",
            "3. low": "0.3805",
            "4. close": "0.4600",
            "5. volume": "8417416"
        },
        "2022-01-31": {
            "1. open": "1.5500",
            "2. high": "1.9800",
            "3. low": "0.8801",
            "4. close": "0.9299",
            "5. volume": "12922741"
        },
        "2021-12-31": {
            "1. open": "1.6900",
            "2. high": "1.9300",
            "3. low": "1.2600",
            "4. close": "1.4350",
            "5. volume": "10645522"
        },
        "2021-11-30": {
            "1. open": "2.0900",
            "2. high": "2.8900",
            "3. low": "1.5500",
            "4. close": "1.9800",
            "5. volume": "38557525"
        },
        "2021-10-29": {
            "1. open": "2.5200",
            "2. high": "2.5500",
            "3. low": "1.9400",
            "4. close": "2.0400",
            "5. volume": "5866024"
        },
        "2021-09-30": {
            "1. open": "4.7700",
            "2. high": "4.8700",
            "3. low": "2.2000",
            "4. close": "2.5200",
            "5. volume": "36664390"
        },
        "2021-08-31": {
            "1. open": "3.2000",
            "2. high": "3.5200",
            "3. low": "2.6600",
            "4. close": "3.2400",
            "5. volume": "4377892"
        },
        "2021-07-30": {
            "1. open": "3.9600",
            "2. high": "5.1100",
            "3. low": "2.9000",
            "4. close": "3.2400",
            "5. volume": "20087638"
        },
        "2021-06-30": {
            "1. open": "3.0200",
            "2. high": "5.0000",
            "3. low": "2.4410",
            "4. close": "3.9400",
            "5. volume": "27732442"
        },
        "2021-05-28": {
            "1. open": "3.9400",
            "2. high": "4.9900",
            "3. low": "2.9347",
            "4. close": "3.0100",
            "5. volume": "6802402"
        },
        "2021-04-30": {
            "1. open": "5.6300",
            "2. high": "5.7800",
            "3. low": "3.8550",
            "4. close": "3.9500",
            "5. volume": "1697551"
        },
        "2021-03-31": {
            "1. open": "6.1100",
            "2. high": "8.5000",
            "3. low": "5.0101",
            "4. close": "5.6500",
            "5. volume": "7024339"
        },
        "2021-02-26": {
            "1. open": "7.6100",
            "2. high": "9.6300",
            "3. low": "5.7120",
            "4. close": "5.9800",
            "5. volume": "11022737"
        },
        "2021-01-29": {
            "1. open": "7.5400",
            "2. high": "8.5900",
            "3. low": "7.0400",
            "4. close": "7.5500",
            "5. volume": "5176094"
        }
    }
}