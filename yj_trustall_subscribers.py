#!/usr/bin/env python3
# script to trusts all numbers in the SQLite db file (again).
# 2020 Yves Jeanrenaud for PocketPC.ch 

import sqlite3
from pprint import pprint
import sys,os
dbFilename= os.path.abspath(os.path.dirname(sys.argv[0]))+'/signal.db' 
import arrow
#connect to sqlite db
conn = sqlite3.connect(dbFilename, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
#set db cursor
cursor = conn.execute("PRAGMA table_info(subscribers);")
results = cursor.fetchall()
print(dbFilename+"\n=============================================")
pprint(results)
cursor =conn.execute("SELECT phone FROM subscribers;")
results = cursor.fetchall()	
print("---------------------------------------------")
pprint(results)
print("---------------------------------------------\nn="+str(len(results)))

#stop the dbus service for a moment
import os
stopService = 'systemctl stop signal.service'
print("systemctl stop signal.service");
print(os.popen(stopService).read()+" \n")
try:
	connection = sqlite3.connect(dbFilename, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
except Error as e:
	print(e)

sql = "SELECT phone FROM subscribers"
cursor = connection.execute(sql)
results = cursor.fetchall()


counter=1
if len(results)>1:
	for subscriber in results:
		trustCmd = "signal-cli --config /var/lib/signal-cli -u +YOURNUMBER trust "+str(subscriber[0]) +" -a"
		print("#"+str(counter))
		counter+=1
		print("trust to "+str(subscriber[0]))
		print(os.popen(trustCmd).read()+" \n--------------------------------\n")
		
else: #only one subscriber
	trustCmd = "signal-cli --config /var/lib/signal-cli -u +YOURNUMBER trust "+str(subscriber[0][0]) +" -a"
	print("trust to "+str(subscriber[0][0]))
	print(os.popen(trustCmd).read()+" \n--------------------------------\n")
	
print("all signals trusted")
# restart service
startService = 'systemctl start signal.service'
print('systemctl start signal.service');
print(os.popen(startService).read()+" \n")
