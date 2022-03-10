import re
import csv
import os

def reader(filename):
	with open(filename, "r", encoding="utf-8") as f:
		m = []
		ass = ""
		for row in csv.reader(f):
			if any(field.strip() for field in row):
				for item in row:
					ass += "," + str(item)
				m.append(ass)
	return m

def output_csv():
	thisFile = "tmp-patron_import.csv"
	with open(thisFile, "w", encoding="utf-8") as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		header = ["cardnumber", "surname", "firstname", "address", "country", "email", "phone", "dateofbirth", "branchcode", "categorycode", "dateenrolled", "dateexpiry", "borrowernotes", "password", "userid"]
		writer.writerow(header)
		for item in pars_objects:
			row = [item.cardnumber, item.surname, item.firstname, item.address, item.country, item.email, item.phone, item.dateofbirth, item.branchcode, item.categorycode, item.dateenrolled, item.dateexpiry, item.borrowernotes, item.password, item.userid]
			writer.writerow(row)

class pars_object:
	def __init__(self, name, text):
		self.name = name
		self.text = text
		self.cardnumber = " "
		self.surname = " "
		self.firstname = " "
		self.address = " "
		self.country = " "
		self.email = " "
		self.phone = " "
		self.dateofbirth = " "
		self.branchcode = "TPU"
		self.categorycode = " "
		self.dateenrolled = " "
		self.dateexpiry = " "
		self.borrowernotes = " "
		self.password = " "
		self.userid = " "
		self.objects_fields()
	
	def objects_fields(self):
		m = self.text.split("@")
		for item in m:
			a = item.split(",",1)
			if a[0] == "100":
				self.cardnumber = item.split("=")[1].split(",",1)[0]
			if a[0] == "101":
				self.surname = '"' + item.split("=")[1] + '"'
			if a[0] == "102":
				self.firstname = '"' + item.split("=")[1]
			if a[0] == "103":
				self.firstname += " " + item.split("=")[1] + '"' 
			if a[0] == "130":
				self.address = '"' + item.split("=")[1] + '"'
			if a[0] == "108":
				self.country = '"' + item.split("=")[1] + '"'
			if a[0] == "122":
				self.email = item.split("=")[1]
			if not "=" in item and "." in item:
				self.email += "@" + item
			if a[0] == "120":
				self.phone = item.split("=")[1]
			if a[0] == "234":
				b = item.split("=")[1]
				self.dateofbirth = b[0] + b[1] + b[2] + b[3] + "-" + b[4] + b[5] + "-" + b[6] + b[7]
			if a[0] == "107":
				b = item.split("=")[1]
				if b == "Студент":
					self.categorycode = "ST"
				else:
					self.categorycode = "PT"
			if a[0] == "246":
				b = item.split("=")[1]
				self.dateenrolled = b[0] + b[1] + b[2] + b[3] + "-" + b[4] + b[5] + "-" + b[6] + b[7]
			if a[0] == "106":
				b = item.split("=")[1]
				self.dateexpiry = b[0] + b[1] + b[2] + b[3] + "-" + b[4] + b[5] + "-" + b[6] + b[7]
			if a[0] == "115":
				self.password = item.split("=")[1]
			if a[0] == "100":
				self.userid = item.split("=")[1].split(",",1)[0] 

dirname = './'
files = os.listdir(dirname)
mass = reader("users.dat")
pars_objects = [pars_object(f"name_object_{i}", mass[i]) for i in range(len(mass))]
output_csv()