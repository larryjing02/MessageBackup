import datetime
timestamp = 689416188004000000
offset = 978336000
timestamp = timestamp // 1000000000 - offset
dt = datetime.datetime.fromtimestamp(offset)

# datetime(message.date/1000000000 + strftime("%s", "2001-01-01") ,"unixepoch","localtime") 


print(dt.strftime('%m/%d/%Y %I:%M:%S %p %Z')) 