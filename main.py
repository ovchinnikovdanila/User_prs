import re
import csv
import os

def reader(filename):
		with open(filename, "r", encoding="utf-8") as f:
			text = ""
			etc = 0
			global a
			for row in csv.reader(f, delimiter="@"):
				# print(etc)
				# if row[0]:
				# 	print("fuck")
				# 	if row[0][0] == "1" and row[0][1] ==",":
				# 		etc += 1
				# 	if row[0][0] == "1" and row[0][1] =="," and etc > 1:
				# 		a = pars_object(text)
				# 		add_row()
				# 		text = ""
				if any(field.strip() for field in row):
					for item in row:
						if item:
							if item[0] == "1" and item[1] ==",":
								etc += 1
							if item[0] == "1" and item[1] =="," and etc > 1:
								a = pars_object(text)
								add_row()
								text = ""
						if any(element == "=" for element in item):
							text += "@" + item
						else:
							text += "*^/&%" + item +"&#%!$"
			a = pars_object(text)
			add_row()
			text = ""

def add_row():
	thisFile = "tmp-patron_import.csv"
	if not os.path.exists(thisFile):
		with open(thisFile, "w", newline = "", encoding="utf-8") as csvfile:
			writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE, escapechar='', quotechar='',  delimiter='\t')
			header = ["cardnumber,surname,firstname,address,country,email,phone,dateofbirth,branchcode,categorycode,dateenrolled,dateexpiry,borrowernotes,password,userid"]
			writer.writerow(header)
			row = [a.cardnumber+","+a.surname+","+a.firstname+","+a.address+","+a.country+","+a.email+","+a.phone+","+a.dateofbirth+","+a.branchcode+","+a.categorycode+","+a.dateenrolled+","+a.dateexpiry+","+a.borrowernotes+","+a.password+","+a.userid]
			writer.writerow(row)
	
	else:
		with open(thisFile, "a", newline = "", encoding="utf-8") as csvfile:
			writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE, escapechar='', quotechar='',  delimiter='\t')
			row = [a.cardnumber+","+a.surname+","+a.firstname+","+a.address+","+a.country+","+a.email+","+a.phone+","+a.dateofbirth+","+a.branchcode+","+a.categorycode+","+a.dateenrolled+","+a.dateexpiry+","+a.borrowernotes+","+a.password+","+a.userid]
			writer.writerow(row)

class pars_object:
	def __init__(self, text):
		self.text = text
		self.cardnumber = ' '
		self.surname = ' '
		self.firstname = ' '
		self.address = ' '
		self.country = ' '
		self.email = ' '
		self.phone = ' '
		self.dateofbirth = ' '
		self.branchcode = 'TPU'
		self.categorycode = ' '
		self.dateenrolled = ' '
		self.dateexpiry = ' '
		self.borrowernotes = ' '
		self.password = ' '
		self.userid = ' '
		self.objects_fields()
	
	def objects_fields(self):
		# def nise_view(text):
		# 	a = text.replace("  ", " ")
		# 	a = a.replace("; ;",";")
		# 	a = a.replace(" ;","")
		# 	a = a.replace(";",",")
		# 	a = a.replace("*^/&%","")
		# 	while a[-1] == " " or a[-1] == ",":
		# 		a = a[:-1]
		# 	return(a)

		m = self.text.split("@")
		for item in m:
			a = item.split(",",1)
			if a[0] == "100":
				self.cardnumber = item.split("=")[1].split(",",1)[0].replace("&#%!$","").replace("*^/&%","")
			if a[0] == "101":
				self.surname = '"' + item.split("=")[1].replace("&#%!$","").replace("*^/&%","") + '"'
			if a[0] == "102":
				self.firstname = '"' + item.split("=")[1].replace("&#%!$","").replace("*^/&%","")
			if a[0] == "103":
				self.firstname += " " + item.split("=")[1].replace("&#%!$","").replace("*^/&%","") + '"'
			if a[0] == "130":
				self.address = '"' + item.split("=")[1].replace("&#%!$","").replace("*^/&%","") + '"'
			if a[0] == "108":
				self.country = '"' + item.split("=")[1].replace("&#%!$","").replace("*^/&%","") + '"'
			if a[0] == "122":
				self.email = item.split("=")[1].replace("&#%!$","").replace("*^/&%","@")
			if a[0] == "120":
				self.phone = item.split("=")[1].replace("&#%!$","").replace("*^/&%","")
			if a[0] == "234":
				b = item.split("=")[1].replace("&#%!$","").replace("*^/&%","")
				self.dateofbirth = b[0] + b[1] + b[2] + b[3] + "-" + b[4] + b[5] + "-" + b[6] + b[7]
			if a[0] == "107":
				b = item.split("=")[1].replace("&#%!$","").replace("*^/&%","")
				if b == "Студент":
					self.categorycode = "ST"
				else:
					self.categorycode = "PT"
			if a[0] == "246":
				b = item.split("=")[1].replace("&#%!$","").replace("*^/&%","")
				self.dateenrolled = b[0] + b[1] + b[2] + b[3] + "-" + b[4] + b[5] + "-" + b[6] + b[7]
			if a[0] == "106":
				b = item.split("=")[1].replace("&#%!$","").replace("*^/&%","")
				self.dateexpiry = b[0] + b[1] + b[2] + b[3] + "-" + b[4] + b[5] + "-" + b[6] + b[7]
			if a[0] == "119":
				if re.search('[а-яА-Я ,]', item.split("=")[1].replace("&#%!$","").replace("*^/&%","")):
					self.borrowernotes = '"' + item.split("=")[1].replace("&#%!$","").replace("*^/&%","") + '"'
				else:
					self.borrowernotes = item.split("=")[1].split(",",1)[0].replace("&#%!$","").replace("*^/&%","")
			if a[0] == "115":
				self.password = item.split("=")[1].replace("&#%!$","").replace("*^/&%","")
			if a[0] == "100":
				self.userid = item.split("=")[1].split(",",1)[0].replace("&#%!$","").replace("*^/&%","")

if os.path.exists("tmp-patron_import.csv"):
	os.remove("tmp-patron_import.csv")
reader("users.dat")