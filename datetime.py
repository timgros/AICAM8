from datetime import datetime


now = datetime.now()
date_time = now.strftime("%m%d%Y%H%M%S")
print(date_time)