def parse_csv_data(csv_filename):
    return open(csv_filename, "r").readlines()


def process_covid_csv_data(covid_csv_data):
    covid_data_england = parse_csv_data(covid_csv_data)

    last7days_cases = 0
    for i in range(3, 10):
        row = covid_data_england[i]
        row_list = list(row.split(","))
        new_cases = row_list[6]
        new_cases_list = list(map(list, new_cases))
        del new_cases_list[len(new_cases) - 1]
        new_cases = int("".join(new_cases))
        last7days_cases += new_cases

    first_entry = covid_data_england[1]
    first_entry_list = list(first_entry.split(","))
    current_hospital_cases = first_entry_list[5]

    latest_total_deaths_entry = covid_data_england[14]
    latest_total_deaths_entry_list = list(latest_total_deaths_entry.split(","))
    total_deaths = latest_total_deaths_entry_list[4]

    return last7days_cases, current_hospital_cases, total_deaths


