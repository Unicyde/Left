from utils import *

def diveToLast(lst):
	try:
		if type(list(list(lst.values())[0][0].values())[0]) is list:
			return diveToLast(list(lst.values())[0][0])
		elif type(list(list(lst.values())[0][1].values())[0]) is list:
			return diveToLast(list(lst.values())[0][1])
		else:
			return lst
	except:
		raise SyntaxError(fail + "Invalid AST format!" + endc)


if __name__ == '__main__':
	print(diveToLast({"+": [{"number": "3"}, {"number": "17"}]}))
	print(diveToLast({"-": [{"*": [{"number": "5"}, {"id": "pi"}]}, {"/": [{"number": "3"}, {"number": "2"}]}]}))
	print(diveToLast({"=": [{"id": "pi"}, {"-": [{"*": [{"number": "5"}, {"id": "pi"}]}, {"/": [{"number": "3"}, {"number": "2"}]}]}]}))