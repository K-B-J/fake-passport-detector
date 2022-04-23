import datetime
import time


def dashboard_data(data):
    final_dict = {}
    airp_dict = {}
    years_set = set()
    cases = {}
    data = sorted(data, key=lambda k: k.time)
    last_occurance = data[len(data) - 1]
    occurance_airport = last_occurance.airport.airport
    occurance_day = datetime.datetime.fromtimestamp(int(last_occurance.time)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    for i in data:
        airport = i.airport.airport
        dateofcase = datetime.datetime.fromtimestamp(int(i.time))
        year = dateofcase.year
        years_set.add(year)

        # setting up airp_dict
        if airport not in airp_dict:
            airp_dict[airport] = {}
        if year in airp_dict[airport]:
            airp_dict[airport][year] += 1
        else:
            airp_dict[airport][year] = 1

        # setting up cases dict
        if year not in cases:
            cases[year] = []
        dt = dateofcase.strftime("%Y-%m-%d")
        if len(cases[year]) != 0:
            flag = False
            for j in cases[year]:
                if j[0] == dt:
                    j[1] += 1
                    Flag = True
                    break
            if flag == False:
                cases[year].append([dt, 1])
        else:
            cases[year].append([dt, 1])

    # logic for airport-cases bar charts
    for airport in airp_dict:
        for year in years_set:
            if year not in airp_dict[airport]:
                airp_dict[airport][year] = 0
        airp_dict[airport] = dict(sorted(airp_dict[airport].items()))

    series_data = []
    for i in airp_dict:
        obj = {
            "name": i,
            "data": list(airp_dict[i].values()),
        }
        series_data.append(obj)

    years = list(years_set)
    years = [str(year) for year in years]

    # logic for time-cases line chart
    final_arr = []
    for i in cases:
        for j in cases[i]:
            dt_format = datetime.datetime.strptime(j[0], "%Y-%m-%d")
            unix_time = time.mktime(dt_format.timetuple())
            final_arr.append([int(unix_time), j[1]])

    return years, series_data, final_arr, occurance_airport, occurance_day
