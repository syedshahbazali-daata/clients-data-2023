from datetime import datetime, timedelta

# make a function takes two dates 2023-10-20,2023-10-30 and returns a list of dates in between
def range_of_dates(starting_date, ending_date):
    starting_date = datetime.strptime(starting_date, "%Y-%m-%d")
    ending_date = datetime.strptime(ending_date, "%Y-%m-%d")
    dates = []
    while starting_date <= ending_date:
        dates.append(starting_date.strftime("%Y-%m-%d"))
        starting_date += timedelta(days=1)
    return dates

