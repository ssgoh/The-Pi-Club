import datetime
time_now = datetime.datetime.now()
later = time_now + datetime.timedelta(seconds=30)
print(time_now, later)
print(later.year, later.month,later.day,later.hour,later.minute,later.second)



"""
import datetime
YEAR        = datetime.date.today().year
MONTH       = datetime.date.today().month
DATE        = datetime.date.today().day
HOUR        = datetime.datetime.now().hour
MINUTE      = datetime.datetime.now().minute
SECONDS     = datetime.datetime.now().second
print(YEAR, MONTH, DATE, HOUR, MINUTE, SECONDS)
"""