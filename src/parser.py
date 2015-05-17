from utils import *

vars = {}

def parseExpression(nodes):
	print(nodes)

	if len(nodes) == 0:
		return None
	elif (len(nodes) == 1 and not contains(["+","-","*","/","^"], nodes)) or type(nodes) is list:
		if type(nodes) is list:
			return [parse(x) for x in nodes]
		else:
			if type(nodes[list(nodes.keys())[0]]) is not str and not contains(["list","tuple"], nodes):
				raise Exception
			k = nodes
			if "id" in k:
				if k["id"] not in vars:
					raise NameError(fail + "Invalid pointer `%s`!" % (k["id"]) + endc)
				else:
					k = vars[k["id"]]
			if contains(["number","string"], k):
				k = k[list(k.keys())[0]]
			if "list" in k:
				k = [parse(x) for x in k["list"]]
			elif "tuple" in k:
				k = tuple(parse(x) for x in k["tuple"])
			return k

	operator = list(nodes.keys())[0]
	left = nodes[operator][0]
	right = nodes[operator][1]

	# print(left)
	# print(right)
	# print(operator)
	# print()

	if type(left) is list and len(left) == 1:
		left = left[0]
	if type(right) is list and len(right) == 1:
		right = right[0]

	if "id" in left:
		if left["id"] not in vars:
			raise NameError(fail + "Invalid pointer `%s`!" % (left["id"]) + endc)
		else:
			left = vars[left["id"]]
	if "id" in right:
		if right["id"] not in vars:
			raise NameError(fail + "Invalid pointer `%s`!" % (right["id"]) + endc)
		else:
			right = vars[right["id"]]

	if not contains(["number","string"], left):
		left = parse(left)
		left = genType(left)

	if not contains(["number","string"], right):
		right = parse(right)
		right = genType(right)

	# print(left)
	# print(right)
	# print(operator)
	# print()

	if "number" in left and "number" in right:
		left = left["number"]
		right = right["number"]
		if operator == "+":
			try:
				return int(left) + int(right)
			except:
				return float(left) + float(right)
		elif operator == "-":
			try:
				return int(left) - int(right)
			except:
				return float(left) - float(right)
		elif operator == "*":
			try:
				return int(left) * int(right)
			except:
				return float(left) * float(right)
		elif operator == "/":
			try:
				return int(left) / int(right)
			except:
				return float(left) / float(right)
		elif operator == "^":
			try:
				assert round(float(left)) < 10**100 and round(float(right)) < 10**100
			except:
				print(warn + underline + "Googol found!" + endc)
				if round(float(left)) + round(float(right)) > 10**100:
					raise IOError(fail + underline + "Googolplex can't be computed!" + endc)
			try:
				return int(left) ** int(right)
			except:
				return float(left) ** float(right)

	elif "list" in left and "list" in right:
		left = left["list"]
		right = right["list"]
		if operator == "+":
			return {"list": left + right}
		elif operator == "-":
			return {"list": [x for x in left if x not in right]}
		elif operator == "*":
			return {"list": [x for x in left if x in right]}
		else:
			raise ArithmeticError(fail + "Can't apply `%s` to `list` and `list`!" % (operator) + endc)

	elif "list" in left:
		left = left["list"]
		if operator == "+":
			left.append(right)
			return {"list": left}
		elif operator == "-":
			return {"list": [x for x in left if x != right]}
		elif operator == "*":
			return {"list": [x for x in left if x == right]}
		else:
			raise ArithmeticError(fail + "Can't apply `%s` to `list` and `%s`!" % (operator, list(right.keys())[0]) + endc)

	elif "tuple" in left and "tuple" in right:
		left = left["tuple"]
		right = right["tuple"]
		if operator in ["+","-","*","/","^"]:
			return {"tuple": [parse({operator: [x, y]}) for x, y in zip(left, right)]}

	elif "tuple" in left and "number" in right:
		left = left["tuple"]
		if operator in ["+","-","*","/","^"]:
			return {"tuple": [parse({operator: [x, right]}) for x in left]}

	elif "number" in left:
		left = left["number"]
		right = right["string"]
		if operator == "+":
			print(warn + "WARNING::Converting `int` to `string` implicitly!" + endc)
			return left + right
		elif operator == "*":
			return round(float(left)) * right
		else:
			raise ArithmeticError(fail + "Can't apply `%s` to `int` and `string`!" % (operator) + endc)

	elif "number" in right:
		left = left["string"]
		right = right["number"]
		if operator == "+":
			print(warn + "WARNING::Converting `int` to `string` implicitly!" + endc)
			return left + right
		elif operator == "*":
			return left * round(float(right))
		elif operator == "-":
			try:
				return left[:-round(float(right))]
			except:
				raise IndexError(fail + "String index out of range!" + endc)
		else:
			raise ArithmeticError(fail + "Can't apply `%s` to `int` and `string`!" % (operator) + endc)

	else:
		left = left["string"]
		right = right["string"]
		if operator == "+":
			return left + right
		elif operator == "-":
			return left.replace(right, "")
		else:
			raise ArithmeticError(fail + "Can't apply `%s` to `string` and `string`!" % (operator) + endc)

def assignParse(nodes):
	#print(nodes)
	operator = list(nodes.keys())[0]
	if operator[-1] != "=":
		raise SyntaxError(fail + "Invalid assignment operator `%s`!" % (operator) + endc)

	name = nodes[operator][0]
	value = nodes[operator][1]

	if type(name) is list:
		if "list" in value:
			value = value["list"]
			vals = list(value)

			bak = {}
			for n, v in zip(name, vals):
				if "id" not in n:
					raise Exception(fail + "Invalid identifier type `%s`!" % (n) + endc)
				if "id" in v:
					if v["id"] not in vars:
						raise NameError(fail + "Invalid pointer `%s!`" % (v["id"]) + endc)
					else:
						v = vars[v["id"]]
				bak[n["id"]] = v
				del value[0]
			for x in bak:
				vars[x] = bak[x]
			if len(value) > 0:
				vars[name[-1]["id"]] = {"list": vals[-len(value)-1:-len(value)] + value}
			return
		else:
			for n in name:
				if "id" not in n:
					raise Exception(fail + "Invalid identifier type `%s`!" % (n) + endc)
				vars[n["id"]] = value
			return
	
	if "id" not in name:
		raise Exception(fail + "Invalid identifier type `%s`!" % (list(name.keys())[0]) + endc)
	else:
		name = name["id"]
	if "id" in value:
		if value["id"] not in vars:
			raise NameError(fail + "Invalid pointer `%s`!" % (value["id"]) + endc)
		else:
			value = vars[value["id"]]

	if operator == "=":
		vars[name] = genType(parse(value))

def parse(nodes):
	#print(vars) if len(vars) > 0 else None
	try:
		#print(nodes)
		return parseExpression(nodes)
	except IOError:
		raise
	except:
		assignParse(nodes)