from utils import *

def diveToLast(lst):
	try:
		if type(list(list(lst.values())[0][0].values())[0]) is list:
			return diveToLast(list(lst.values())[0][0])
		elif type(list(list(lst.values())[0][1].values())[0]) is list:
			return diveToLast(list(lst.values())[0][1])
		else:
			return lst
	except Exception as e:
		raise SyntaxError(fail + "Invalid AST format! (`%s`)" % (e) + endc)

def insertToTuple(tup, value, depth, index):
	if type(tup) is dict:
		tup = [tup]
	else:
		tup = list(tup)

	if depth > 0:
		if type(tup) is list:
			success = False
			for i, x in enumerate(tup):
				if "tuple" in x:
					success = True

					tup = [insertToTuple(tup[i]["tuple"], value, depth-1, index)]
					break

			if not success:
				raise SyntaxError(fail + "Invalid tuple format (maybe depth overflow) `%s`!" % (tup) + endc)

		elif type(tup) is dict and contains({"tuple"}, tup["tuple"]):
			tup = [insertToTuple(tup["tuple"], value, depth-1, index)]

	else:
		for i, x in enumerate(tup):
			if "tuple" in x:
				if type(value) is list and len(value) == 1:
					value = value[0]
				if index < 0:
					if index == -1:
						tup[i]["tuple"].append(value)
					else:
						tup[i]["tuple"].insert(index+1, value)
				else:
					tup[i]["tuple"].insert(index, value)
				break

	if type(tup) is list:
		if len(tup) > 1:
			tup = {"tuple": list(tup)}
		else:
			tup = tup[0]

	return tup


if __name__ == '__main__':
	print(diveToLast({"+": [{"number": "3"}, {"number": "17"}]}))
	print(diveToLast({"-": [{"*": [{"number": "5"}, {"id": "pi"}]}, {"/": [{"number": "3"}, {"number": "2"}]}]}))
	print(diveToLast({"=": [{"id": "pi"}, {"-": [{"*": [{"number": "5"}, {"id": "pi"}]}, {"/": [{"number": "3"}, {"number": "2"}]}]}]}))

	print(insertToTuple({"tuple": [{"tuple": [{"tuple": [{"number": "3"}, {"number": "4"}]}]}]}, {"tuple": [{"number": "1"}, {"number": "2"}]}, 2, 0))