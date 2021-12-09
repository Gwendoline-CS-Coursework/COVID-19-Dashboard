import pytest
from covid_data_handler import parse_csv_data, process_covid_csv_data
from main import hours_to_seconds, minutes_to_seconds, hhmm_to_seconds


def test_process_covid_csv_data():
    assert process_covid_csv_data("nation_2021-10-28") == (240299, 7019, 141544)


def test_hhmm_to_seconds():
    assert hhmm_to_seconds("01:01") == 3660
