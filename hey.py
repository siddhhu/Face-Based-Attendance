import sqlite3
from datetime import date
import pandas as pd
today=date.today()
print(today)
conn = sqlite3.connect('information.db')
print ("Opened database successfully");
cursor = conn.execute("SELECT DISTINCT NAME,Time, Date from Attendance where Date=?",(today,))
for line in cursor:
    data1=list(line)
    print(data1)
print ("Operation done successfully");
conn.close()
