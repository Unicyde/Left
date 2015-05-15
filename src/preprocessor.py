from utils import *
from multiplace import *
from diver import *
from parser import parse

def process(nodes):
	skip = 0
	for i, n in enumerate(nodes):
		if "operator" in n and n["operator"] in ["+","-","*","/","^"]:
			if len(nodes) > i+1 and nodes[i+1] == {"operator": "="}:
				if "id" in nodes[i-1]:
					nodes.insert(i+2, "lpar")
					nodes.append("rpar")
					nodes.insert(i+2, nodes[i-1])
					nodes.insert(i+3, n)
					del nodes[i]
					#print(nodes)
	node = []
	if "rpar" in nodes:
		if not "lpar" in nodes:
			raise SyntaxError("Closing brackets without openings!")

		i = 0
		while nodes[i] != "rpar":
			i += 1
		piece = []
		bak = i
		i -= 1
		while nodes[i] != "lpar":
			piece.append(nodes[i])
			i -= 1
		piece.reverse()
		node += process(piece)[0]
		#print(node, "L")
		del nodes[i:bak+1]
		nodes.insert(i, genType(parse(node[0])))
		node = process(nodes)[0]
	else:
		#print(nodes)
		for i, n in enumerate(nodes):
			if skip > 0:
				skip -= 1
				continue
			if "operator" in n:
				if (n["operator"] == "^" and contains(["+","-","*","/"],node[-1])) or (len(node)>0 and "=" in node[-1]):
					if nodes[i+1] == "lsq":
						value, skip = process(nodes[i+1:])
						value = value[0]
					else:
						value = nodes[i+1]
						skip = 1

					if "=" in node[-1]:
						list(diveToLast(node[-1]).values())[0][1] = {n["operator"]: [list(diveToLast(node[-1]).values())[0][1], value]}
					else:
						list(node[-1].values())[0][1] = {n["operator"]: [list(node[-1].values())[0][1], value]}

				elif (n["operator"] in ["*","/"] and contains(["+","-"],node[-1])) or (len(node)>0 and "=" in node[-1]):
					if nodes[i+1] == "lsq":
						value, skip = process(nodes[i+1:])
						value = value[0]
					else:
						value = nodes[i+1]
						skip = 1

					if "=" in node[-1]:
						node[-1]["="][1] = {n["operator"]: [node[-1]["="][1], value]}
					else:
						list(node[-1].values())[0][1] = {n["operator"]: [list(node[-1].values())[0][1], value]}

				else:
					if nodes[i+1] == "lsq" or "comma" in nodes[i+1:]:
						if "comma" in nodes[i+1:]:
							#print(nodes[i+1:])
							value, skip = process(nodes[i+1:])
							if type(value[0]) is list:
								value = value[0]
						else:
							print("O")
							value, skip = process(["lsq"] + nodes[i+1:] + ["rsq"])
						value = {"list": value}
						#print(value)
					else:
						value = nodes[i+1]
						skip = 1
					if n["operator"] == "-" and len(node) == 0:
						first = {"number": "0"}
					else:
						first = node[-1]
					node.append({n["operator"]: [first, value]})
					if first != {"number": "0"}:
						del node[-2]

			elif n == "lsq":
				piece = []
				o = 1
				ii = i + 1
				while ii < len(nodes) and o != 0:
					if nodes[ii] == "lsq":
						o += 1
					elif nodes[ii] == "rsq":
						o -= 1
					piece.append(nodes[ii])
					ii += 1
				skip = ii - (i+1)
				# print(piece, "K")
				piece = process(piece[:-1])[0]
				node.append({"list": piece})
				# print(node)
				# print(piece)
				# print(nodes)
				# print(skip)
				# print()

			elif n == "comma":
				pass

			elif "id" in n:
				if len(nodes) > i+1 and nodes[i+1] == "comma":
					ids = []
					step = 0
					ii = i
					for x in nodes[i:]:
						if step == 1:
							if x != "comma" and len(nodes) > ii+1 or len(nodes) <= ii+1:
								break
							else:
								step = 0
								ii += 1
								continue
						if "id" not in x:
							break
						ids.append(x)
						step = 1
						ii += 1
					skip = ii - i - 1
					node.append(ids)
				else:
					node.append(n)

			else:
				node.append(n)

	#print(node)
	return node, skip