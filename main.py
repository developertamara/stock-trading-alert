import requests
from twilio.rest import Client

STOCK_NAME = "ACRS"
COMPANY_NAME = "Aclaris Therapeutics"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

ALPHA_API_KEY = "api_key"
NEWS_API_KEY = "news_api_key"

account_sid = "account_sid"
auth_token = "auth_token"

FROM_NUMBER = "+1231231234"
MY_NUMBER = "+123456789"

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
alpha_parameters = {
    "function": "TIME_SERIES_DAILY",
    "apikey": ALPHA_API_KEY,
    "symbol": STOCK_NAME,
}
response = requests.get(STOCK_ENDPOINT, params=alpha_parameters)
response.raise_for_status()
stock_data = response.json()
print(stock_data)

time_series_data = stock_data["Time Series (Daily)"]
time_data_list = [value for (key, value) in time_series_data.items()]
yesterday_data = time_data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

#TODO 2. - Get the day before yesterday's closing stock price

day_before_yesterday_data = time_data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
positive_difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
print(positive_difference)

actual_difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
if actual_difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.

percentage_difference = round((positive_difference/float(yesterday_closing_price)) * 100)
print(percentage_difference)

#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if percentage_difference >= 2:
    print("Get News!")

#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
    news_parameters = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    articles = news_response.json()["articles"]
    print(articles)

#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation

    first_three_articles = articles[:3]
    print(first_three_articles)
    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number.

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [(f"{STOCK_NAME}: {up_down} {percentage_difference}% \nHeadline: {article['title']}. \n"
                           f"Brief: {article['description']}")
                          for article in first_three_articles]

#TODO 9. - Send each article as a separate message via Twilio.
    client = Client(account_sid, auth_token)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_= FROM_NUMBER,
            to= MY_NUMBER,
        )

