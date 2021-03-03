# CRUD Operation using sqlite3
import sqlite3
dataBaseName = "sample.db"
tableName = "SAMPLE_TABLE"
menuFileName = "menu.cfg"

connection = sqlite3.connect(dataBaseName) 
cursor = connection.cursor()
fields = []

def getFields():

	cursor.execute("SELECT count(name) FROM sqlite_master WHERE type = 'table' and name = '{}' ".format(tableName))
	if (cursor.fetchone()[0] == 1):
		metadata = cursor.execute("PRAGMA TABLE_INFO({})".format(tableName))
		for field in metadata:
			fields.append(field[1])

	else:
		print("\nNo Table Named {} in database {}".format(tableName, dataBaseName))
		exit()

def addRecord():

	values = ""
	for field in fields:
		storeData = input("\nEnter the " + field + ": ")
		if field == fields[-1]:
			values += "\'" + storeData + "\' "
		else:
			values += "\'" + storeData + "\', "
	try:
		cursor.execute("INSERT INTO {} VALUES ({})".format(tableName, values))
		connection.commit()
		if cursor.rowcount >= 1:
			print("Insertion successful.")
		else:
			print("Insertion unsuccessful.")

		print("\n{} Number of row(s) affected".format(cursor.rowcount))

	except Exception as e:
		print("Error ", e)
		connection.rollback()
		

def readRecords():

	records = cursor.execute("SELECT * FROM {}".format(tableName))
	deletedRecords = []

	for data in records:

		if data[-1] == '0':
			deletedRecords.append(data) 
		else:
			print("\n")
			for item in data:
				print(item + " ", end = " ")
	print("\n\nDeleted Records are: ")
	for data in deletedRecords:
		print("\n")
		for item in data:
			print(item + " ", end = " ")


def updateRecord():

	dataToBeUpdated = input("Enter " + fields[0].lower() + " to be updated: ")
	counter = 1
	for field in fields:
		if field == fields[0]:
			pass
		elif field == fields[-1]:
			pass
		else:
			print(counter - 1, ".", field)
		counter += 1
	choice = int(input("Enter choice: "))

	try:
		updateData = input("Enter {} to update: ".format(fields[choice]))
		cursor.execute("UPDATE {} SET {} = '{}' WHERE {} = '{}' AND STATUS = 1".format(tableName, fields[choice], updateData, fields[0], dataToBeUpdated))
		connection.commit()
		if cursor.rowcount >= 1:
			print("Updation successful.")
		else:
			print(dataToBeUpdated + " not found.")

		print("\n{} Number of row(s) affected".format(cursor.rowcount))

	except Exception as e:
		print("Error ", e)
		connection.rollback()
		peinr("Updation failed.")
	
def deleteRecord():
	dataToBeDeleted = input("Enter " + fields[0].lower() + " to be deleted: ")

	try:
		cursor.execute("UPDATE {} SET {} = '0' WHERE {} = '{}' ".format(tableName, fields[-1], fields[0], dataToBeDeleted))
		connection.commit()
		if cursor.rowcount == 1:
			print("\nDeletion successful.")
		else:
			print(dataToBeDeleted + " is not found")

		print("\n{} Number of row(s) affected".format(cursor.rowcount))

	except Exception as e:
		print("Error ", e)
		connection.rollback()
		print("Deletion failed.")


def exitMenu():
	connection.commit()
	connection.close()
	print("\nThank You.")
	exit()


getFields()
while True:
	print("\n")
	with open(menuFileName) as f:
		menu = f.read()
		print(menu)
	[addRecord, readRecords, updateRecord, deleteRecord, exitMenu][int(input("Enter your choice: ")) - 1]()