# CRUD Operation using sqlite3
import sqlite3
dataBaseName = "sample.db"
tableName = "SAMPLE_TABLE"
menuFileName = "menu.cfg"

connection = sqlite3.connect(dataBaseName) 
cursor = connection.cursor()
fields = []

def getFields():

	metadata = cursor.execute("PRAGMA TABLE_INFO({})".format(tableName))
	for field in metadata:
		fields.append(field[1])
	

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
			print("Error while Insertion.")

		print("\n{} Number of row(s) affected".format(cursor.rowcount))

	except Exception as e:
		print("Error ", e)

def readRecords():

	records = cursor.execute("SELECT * FROM {}".format(tableName))

	for data in records:

		if data[-1] == '0':
			pass 
		else:
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
		cursor.execute("UPDATE {} SET {} = '{}' WHERE {} = '{}' ".format(tableName, fields[choice], updateData, fields[0], dataToBeUpdated))
		connection.commit()
		if cursor.rowcount >= 1:
			print("Updation successful.")
		else:
			print("Error while Updation.")

		print("\n{} Number of row(s) affected".format(cursor.rowcount))

	except Exception as e:
		print("Error ", e)
	
def deleteRecord():
	dataToBeDeleted = input("Enter " + fields[0].lower() + " to be deleted: ")

	try:
		cursor.execute("UPDATE {} SET {} = '0' WHERE {} = '{}' ".format(tableName, fields[-1], fields[0], dataToBeDeleted))
		connection.commit()
		if cursor.rowcount == 1:
			print("\nDeletion successful.")
		else:
			print("Error while Deletion.")

		print("\n{} Number of row(s) affected".format(cursor.rowcount))


	except Exception as e:
		print("Error ", e)


def exitMenu():
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