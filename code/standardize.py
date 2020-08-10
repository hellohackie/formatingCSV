# Main part of the program
if __name__ == '__main__':
	# First able to create and call required function
	print("Make sure your file is in same folder or place in which this program is stored!")
	input_file = input("Enter input file name: ")
	import re
	bankReg = re.compile(r'Axis|HDFC|ICICI|IDFC',re.I)
	bankType = bankReg.search(input_file)
	output_file = input_file.replace('Input', 'Output', 1)
	# print(output_file)
	# print(input_file)
	# print(bankType.group())

	# Calling required function
	if bankType.group()=='HDFC':
		from standardHDFC import standardizeHDFC
		standardizeHDFC(input_file, output_file)
		print("Successfully created!")

	elif bankType.group()=='Axis':
		from standardAxis import standardizeAxis
		standardizeAxis(input_file, output_file)
		print("Successfully created!")

	elif bankType.group()=='ICICI':
		from standardICICI import standardizeICICI
		standardizeICICI(input_file, output_file)
		print("Successfully created!")

	elif bankType.group()=='IDFC':
		from standardIDFC import standardizeIDFC
		standardizeIDFC(input_file, output_file)
		print("Successfully created!")
		
	else:
		print("Something wrong with Input File")