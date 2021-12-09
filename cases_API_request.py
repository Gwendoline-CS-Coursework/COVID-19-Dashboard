import requests
import logging
from uk_covid19 import Cov19API

logging.basicConfig(filename="test.log", level=logging.DEBUG,
                    format="%(levelname)s: %(asctime)s %(message)s")


def covid_API_request(location="Exeter", location_type="ltla"):
    """Queries Public Health England's COVID-19 API, returning data about COVID-19 cases in Exeter and the amount
       of hospitalisations caused by it.
    """
    england_only = [
        'areaType=' + location_type,
        'areaName=' + location
    ]
    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesBySpecimenDate": "newCasesBySpecimenDate"
    }
    api = Cov19API(filters=england_only, structure=cases_and_deaths)
    data = api.get_json()
    data_list = data["data"]
    local_7day_infection_rate = 0
    for i in range(7):
        daily_data_dict = data_list[i]
        daily_infection_rate = daily_data_dict["newCasesBySpecimenDate"]
        local_7day_infection_rate += daily_infection_rate
    return local_7day_infection_rate


