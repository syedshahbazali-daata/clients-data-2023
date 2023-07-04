from datetime import datetime, timedelta
current_datetime_x = datetime.now().utcnow().strftime("%d-%m-%Y %H:%M") # add 5 hours 30 minutes to convert to india time
current_datetime_x = (datetime.strptime(current_datetime_x, "%d-%m-%Y %H:%M") + timedelta(hours=5, minutes=30)).strftime("%d-%m-%Y %H:%M")

print(current_datetime_x)