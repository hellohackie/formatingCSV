import csv

data = []
header = ['Date','Transaction Description','Debit','Credit','Currency','CardName','Transaction','Location']
currType = ['Domestic Transactions', 'International Transactions','Transaction Description', 'Credit']
_currCurrency = ""
_user = ""

def domesticUsage(iteratorLoc):
	global data
	global _user
	global _currCurrency
	fl = True
	next(iteratorLoc, -1)
	user = next(iteratorLoc, -1)
	if user == -1:
		return None
	_user = user[2]
	if _user=='International Transactions':
		internationalUsage(iteratorLoc)
		return None
	next(iteratorLoc, -1)
	while fl == True:
		row = next(iteratorLoc, -1)
		if row==-1:
			return None
		if row[0]=='' and row[1]=='' and row[2]=='':
			fl = False
			break
		trow = []
		trow.append(row[0])
		formated = row[3].split()
		location = formated[-1]
		trow.append(" ".join(formated))
		debit = 0
		credit = 0
		if row[2]!='':
			credit = row[2]
		if row[1]!='':
			debit = row[1]
		trow.append(debit)
		trow.append(credit)
		trow.append("INR")
		trow.append(_user)
		trow.append("Domestic")
		trow.append(location)

		data.append(trow)
	if fl == False:
		domesticUsage(iteratorLoc)

def internationalUsage(iteratorLoc):
	global data
	global _user
	global _currCurrency
	fl = True
	next(iteratorLoc, -1)
	user = next(iteratorLoc, -1)
	if user == -1:
		return None
	_user = user[2]
	if _user=='Domestic Transactions':
		domesticUsage(iteratorLoc)
		return None
	next(iteratorLoc, -1)
	while fl == True:
		row = next(iteratorLoc, -1)
		if row==-1:
			return None
		if row[0]=='' and row[1]=='' and row[2]=='':
			fl = False
			break
		trow = []
		trow.append(row[0])
		formated = row[3].split()
		location = formated[-2]
		typeCurr = formated[-1]
		trow.append(" ".join(formated[:-1]))
		debit = 0
		credit = 0
		if row[2]!='':
			credit = row[2]
		if row[1]!='':
			debit = row[1]
		trow.append(debit)
		trow.append(credit)
		trow.append(typeCurr)
		trow.append(_user)
		trow.append("International")
		trow.append(location)

		data.append(trow)
	if fl == False:
		internationalUsage(iteratorLoc)

def standardizeAxis(input_file, output_file):
	global data
	with open(input_file) as csvFile:
		myCsvReader = csv.reader(csvFile)
		firstRow = next(myCsvReader, -1)
		if firstRow==-1:
			print("File is empty!")
			return None
		with open(output_file, 'w') as f:
			writer = csv.writer(f)
			writer.writerow(header)
		f.close()
		_currCurrency = firstRow[2]
		if _currCurrency == 'Domestic Transactions':
			domesticUsage(myCsvReader)
		else:
			internationalUsage(myCsvReader)
		data = sorted(data, key = lambda x: (x[0].split('-')[::-1]))
		for line in data:
			with open(output_file, 'a') as f:
				writer = csv.writer(f)
				writer.writerow(line)
			f.close()
