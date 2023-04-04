import requests
import smtplib
import html

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = 'VR0RYXJMIQ6UTG2L'
NEWS_API_KEY = "220fdd24e3c1450c9e2f046f4d31d2be"

my_email = "glebtus94@gmail.com"
my_password = "ffrineqpplbnkowc"

stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]
day_before_yesterday_data_closing_price = day_before_yesterday_data["4. close"]

difference = float(yesterday_closing_price) - float(day_before_yesterday_data_closing_price)

up_down = None

if difference > 0:
    up_down = "+"
else:
    up_down = "-"

diff_percent = round((difference / float(yesterday_closing_price)) * 100)

if abs(diff_percent) > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,


    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    first_three_articles = articles[:3]

    first_three_articles_list = [f"Headline: {article['title']}. \nDescription: {article['description']}" for article in first_three_articles]
    for article in first_three_articles_list:
        article = article.encode('ascii', 'ignore').decode('ascii')

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(
                             from_addr=my_email,
                             to_addrs="ivascenko.gleb@gmail.com",
                             msg=f"Subject: {STOCK_NAME}: {up_down}{diff_percent}%\n\n{article}"
                         )
