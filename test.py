# Testing purposes
from datetime import datetime

today = datetime.now()

today_date = today.strftime("%d")
today_month = today.strftime("%B")
today_year = today.strftime("%Y")

format_str = f"{today_date} {today_month}, {today_year}"

print(format_str)
