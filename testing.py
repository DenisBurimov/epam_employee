import datetime

deadline = datetime.date(2021, 12, 31)
today = datetime.date.today()

print(deadline, today, (deadline - today).days)