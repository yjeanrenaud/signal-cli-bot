#!/usr/bin/env python3
# the main script using a SQLite DB to store subscribers into a Signal Channel
# 2020 Yves Jeanrenaud for PocketPC.ch 

dbFilename= 'signal.db'
msg ="Unbekannter Befehl.\nDies ist der Channel von PocketPC.ch\n-----------------------------------------------\nSende START zum Anmelden, STOPP zum Abmelden."

def yjDbHandler (source,timestamp,command):
	global msg
	import sqlite3
	from pprint import pprint
	import arrow
	# db file is now existing
	# connect to db
	try:
	  connection = sqlite3.connect(dbFilename, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) 
	except Error as e:
	  pprint(e)
	
	# create db cursor
	cursor = connection.cursor()
	
	if command == "subscribe": 
		# create table data
		strFormatedDateTime=arrow.get(timestamp).format('YYYY-MM-DD HH:mm:ss ZZ')
		#check for exisiting number is done by sql
		sql = "INSERT INTO subscribers VALUES(\'"+str(source)+"\', "+str(timestamp)+",0 )"
		try:
			cursor.execute(sql)
		except sqlite3.IntegrityError:
			#already existing
			msg="bereits angemeldet"
		else:
			connection.commit()
			#now set the formated data right in an extra commit
			sql="UPDATE subscribers SET subsDateTime = \'"+strFormatedDateTime+"\' WHERE phone = \'"+str(source)+"\'"
			cursor.execute(sql)
			connection.commit()
			msg="erfolgreich angemeldet" 
	
	elif command == "unsubscribe":
	#check if there is one to unsubscribe goes by SQL
		sql = "DELETE FROM subscribers WHERE phone = \'"+str(source)+"\'"
		try: 
			cursor.execute(sql)
		except sqlite3.IntegrityError:
			#not there
			msg="nicht angemeldet?"
		
		else:
			cursor.execute(sql)
			msg="erfolgreich abgemeldet"
	
	connection.commit()
	connection.close()
	
	return

def msgRcv (timestamp, source, groupID, message, attachments):
	global msg
	print(str(message).lower()+" from " + str(source))
	if str(message).lower()=="start" or str(message).lower() == "anmelden" or str(message).lower() == "subscribe" or str(message).lower() == "start":
		print ("subscribe "+source +"!")
    #go and subcribe that number
		yjDbHandler(source,timestamp,"subscribe")

	elif str(message).lower()=="stop" or str(message).lower() == "stopp" or str(message).lower() == "abmelden" or str(message).lower() == "unsubscribe":
		print ("unsubscribe "+source +"!")
    #go and unsubscribe
		yjDbHandler(source,timestamp,"unsubscribe")

	else:
		#reply with help message
		msg="Unbekannter Befehl.\nDies ist der Channel von PocketPC.ch\n-----------------------------------------------\nSende START zum Anmelden, STOPP zum Abmelden."
	
	#send the message back!
	print (msg)
	signal.sendMessage(msg, [], [source])
	return

from pydbus import SystemBus
from gi.repository import GLib

bus = SystemBus()
loop = GLib.MainLoop()

signal = bus.get('org.asamk.Signal')

signal.onMessageReceived = msgRcv
import os, sys
if os.path.exists(dbFilename):
	print("Datenbank-Datei \""+dbFilename+"\" ist vorhanden")
else:
	print("Datenbank-Datei \""+dbFilename+"\" NICHT vorhanden")
	# connetion to SQlite
	connection = sqlite3.connect(dbFilename, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
	# Db cursor
	cursor = connection.cursor()
	# initially create db
	sql = "CREATE TABLE subscribers(" \
		"phone TEXT NOT NULL PRIMARY KEY, " \
		"subsDatestamp INTEGER, " \
		"subsDateTime TEXT )" 
	cursor.execute(sql)
	connection.commit()
	connection.close()
	print("Datenbank-Datei \""+dbFilename+"\" erstellt")
## now enter the loop
print ("Warte auf Nachrichten, schweigend...")
loop.run()
