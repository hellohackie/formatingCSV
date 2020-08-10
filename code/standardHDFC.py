import csv

data = []
header = ['Date','Transaction Description','Debit','Credit','Currency','CardName','Transaction','Location']
currType = ['Domestic Transactions', 'International Transactions','Transaction Description']
_currCurrency = ""
_user = ""
first = 0
second = 0

def domesticUsage(iteratorLoc):
	global data
	global first
	if first==0:
		first=1
		next(iteratorLoc, -1)
	global _user
	fl = True
	user = next(iteratorLoc, -1)
	if user==-1:
		return None
	temp = user[1]
	if temp not in currType and temp!='':
		_user = temp
		_currCurrency = 'Domestic Transactions'
	else:
		_currCurrency = temp
		if _currCurrency != 'Domestic Transactions':
			internationalUsage(iteratorLoc)
	
	while fl==True:
		row = next(iteratorLoc, -1)
		if row == -1:
			break
		if first==1 and row[0]=='':
			first+=1
			continue
		if row[0]=='':
			fl = False
			break
		trow = []
		trow.append(row[0])
		formated = row[1].split()
		trow.append(" ".join(formated))
		debit = 0
		credit = 0
		if row[2][len(str(row[2]))-1]=='r':
			credit = row[2][:len(row[2])-3]
		else:
			debit = row[2]
		trow.append(debit)
		trow.append(credit)
		trow.append("INR")
		trow.append(_user)
		trow.append("Domestic")
		location = str(row[1]).split()
		trow.append(location[-1].lower())
		# print(trow)
		data.append(trow)
	if fl==False:
		domesticUsage(iteratorLoc)

def internationalUsage(iteratorLoc):
	global data
	fl = True
	global second
	second = 0
	global _user
	if second==0:
		next(iteratorLoc, -1)
		second = 1
	user = next(iteratorLoc, -1)
	if user == -1:
		return None
	temp = user[1]
	if temp not in currType and temp!='':
		_user = temp
		_currCurrency = 'International Transactions'
	else:
		_currCurrency = temp
		if _currCurrency != 'International Transactions':
			first = 0
			domesticUsage(iteratorLoc)

	while fl==True:
		row = next(iteratorLoc, -1)
		if row == -1:
			break
		if second==1 and row[0]=='':
			second+=1
			continue
		if row[0]=='':
			fl = False
			break
		trow = []
		trow.append(row[0])
		formated = row[1].split()
		nFormated = formated[:-1]
		trow.append(" ".join(nFormated))
		debit = 0
		credit = 0
		if row[2][len(str(row[2]))-1]=='r':
			credit = row[2][:len(row[2])-3]
		else:
			debit = row[2]
		trow.append(debit)
		trow.append(credit)
		trow.append(formated[-1])
		trow.append(_user)
		trow.append("International")
		location = str(row[1]).split()
		trow.append(location[-2].lower())
		# print(trow)
		data.append(trow)
	if fl==False:
		internationalUsage(iteratorLoc)

def standardizeHDFC(input_file, output_file):
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
		_currCurrency = firstRow[1]
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
