import requests
import json
import logging


logging.basicConfig(filename="test.log", level=logging.DEBUG,
                    format="%(levelname)s: %(asctime)s %(message)s")


def news_API_request(covid_terms="Covid COVID-19 coronavirus"):
    """Queries the News API for the latest articles about COVID-19, returning the headlines along with a
       description.
       The API key is found in the config.json file.
    """
    headlines = []
    base_url = "https://newsapi.org/v2/top-headlines?"
    config_object = open("config.json", "r")
    json_content = config_object.read()
    config_data = json.loads(json_content)
    api_key = config_data["API_key"]
    complete_url = base_url + "q=" + covid_terms + "&apiKey=" + api_key
    response = requests.get(complete_url).json()
    news = response["articles"]
    for article in news:
        article_add = {
            'title': article["title"],
            'content': article["description"]
        }
        headlines.append(article_add)
    logging.info("API request returned the following news: {}".format(headlines))
    return headlines
