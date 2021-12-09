from flask import Flask, render_template, request
import requests
import time
import sched
from cases_API_request import covid_API_request
from datetime import datetime
from news_API_data import news_API_request
from covid_data_handler import parse_csv_data, process_covid_csv_data
import logging

logging.basicConfig(filename="test.log", level=logging.DEBUG,
                    format="%(levelname)s: %(asctime)s %(message)s")
app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)

covid_spreadsheet_data = process_covid_csv_data("nation_2021-10-28.csv")
total_deaths = covid_spreadsheet_data[2]
hospital_cases_data = covid_spreadsheet_data[1]
headlines = news_API_request()
local_infections = covid_API_request()
national_infections = covid_API_request("United Kingdom", "overview")
delay = 0


def hours_to_seconds(hours):
    """Returns the amount of seconds in a given number of hours. (Input should be an integer)"""
    hours = int(hours)
    return hours * 60 * 60


def minutes_to_seconds(minutes):
    """Returns the amount of seconds in a given number of minutes. (Input should be an integer)"""
    minutes = int(minutes)
    return minutes * 60


def hhmm_to_seconds(hhmm):
    """Returns the amount of seconds in a given number of hours and minutes.
       (Input should be of the format hours:minutes)
    """
    hh = int(hhmm.split(":")[0])
    mm = int(hhmm.split(":")[1])
    time_in_seconds = hours_to_seconds(hh) + minutes_to_seconds(mm)
    logging.info("{} is {} seconds".format(hhmm, time_in_seconds))
    return time_in_seconds


def update_trigger(time_input):
    """Calculates the amount of time between the current time and the time when the user wants the data to be
       updated in seconds.
    """
    date_time = datetime.now()
    current_time = date_time.strftime("%H:%M")
    seconds_from_midnight = hhmm_to_seconds(current_time)
    time_input = hhmm_to_seconds(time_input)
    if time_input >= seconds_from_midnight:
        delay = time_input - seconds_from_midnight
        logging.info("The dashboard will be updated in {} seconds".format(delay))
        return delay
    else:
        delay = (24 * 60 * 60) - (seconds_from_midnight - time_input)
        logging.info("The dashboard will be updated in {} seconds".format(delay))
        return delay


def test():
    print("test")


@app.route("/index")
def home():
    """Renders the HTML on a webpage so the data can be read and the user can interact with the program."""
    update_time = request.args.get("update")
    covid_data_update = request.args.get("covid-data")
    update_news = request.args.get("news")
    repeat_updates = request.args.get("repeat")
    update_label = request.args.get("two")

    if update_time:
        update_trigger(update_time)
        if covid_data_update:
            s.enter(delay, 1, covid_API_request)
            s.enter(delay, 2, covid_API_request("United Kingdom", "overview"))
            s.run(blocking=False)
            if repeat_updates:
                while True:
                    s.enter(86400, 1, covid_API_request)
                    s.enter(86400, 2, covid_API_request("United Kingdom", "overview"))
                    s.run(blocking=False)
        if update_news:
            s.enter(delay, 3, news_API_request)
            s.run(blocking=False)
            if repeat_updates:
                while True:
                    s.enter(86400, 3, news_API_request)
                    s.run(blocking=False)

    return render_template("index.html",
                           title="COVID-19 Dashboard",
                           news_articles=headlines,
                           local_7day_infections=local_infections,
                           national_7day_infections=national_infections,
                           deaths_total="Total deaths: " + total_deaths,
                           hospital_cases="Hospital cases: " + hospital_cases_data,
                           location="Exeter",
                           nation_location="United Kingdom"
                           )


if __name__ == "__main__":
    app.run()
