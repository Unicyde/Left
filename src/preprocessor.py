from utils import *
from multiplace import *
from diver import *
from parser import parse

def process(nodes, tupSize=False):
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
			raise SyntaxError(fail + "Closing brackets without openings!" + endc)

		depth = 0
		i = 0
		while nodes[i] != "rpar":
			if nodes[i] == "lpar":
				depth += 1
			i += 1

		depth -= 1

		piece = []
		bak = i

		i -= 1
		while nodes[i] != "lpar":
			piece.append(nodes[i])
			i -= 1
		piece.reverse()

		# if "comma" in piece:
		# 	d = []
		# 	code = []
		# 	j = 0
		# 	for x in piece:
		# 		if x == "comma":
		# 			m = parse(process(code)[0])

		# 			if m:
		# 				d.append(genType(m[0]))
		# 			code = []
		# 		else:
		# 			code.append(x)
		# 			j += 1
		# 	m = parse(process(code)[0])

		# 	if m:
		# 		d.append(genType(m[0]))

		# 	node.append({"tuple": d})

		# 	j = 0
		# 	if nodes[i-1] == "comma":
		# 		j = 1

		# 	del nodes[i-j:bak+1]

		# 	n = len([x for k, x in enumerate(nodes) if len(nodes) > k + 1 and nodes[k+1] == "comma" and k < i-j])
			
		# 	if len(nodes) > 0:
		# 		try:
		# 			right = process(nodes, True)[0]

		# 			node = insertToTuple(right, node, depth-1, n)
		# 		except Exception as e:
		# 			raise SyntaxError(fail + "Error while parsing tuple!\n`%s`" % (e) + endc)

		# 	if type(list(node)[0]) is not dict:
		# 		node = [node]

		# 	return list(node), skip
		# else:
		if "comma" not in piece:
			node += process(piece)[0]
			#print(node, "L")
			del nodes[i:bak+1]
			nodes.insert(i, genType(parse(node[0])))
			node = process(nodes)[0]
			return node

	#print(nodes)
	for i, n in enumerate(nodes):
		if skip > 0:
			skip -= 1
			continue
		if "operator" in n:
			if (n["operator"] == "^" and contains(["+","-","*","/"],node[-1])) or (len(node)>0 and "=" in node[-1]):
				if nodes[i+1] in ["lsq","lpar"]:
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
				if nodes[i+1] in ["lsq","lpar"]:
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
						value, skip = process(nodes[i+1:])
						if type(value[0]) is list:
							value = value[0]
					else:
						print("O")
						value, skip = process(["lsq"] + nodes[i+1:] + ["rsq"])

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

			piece = process(piece[:-1])[0]
			node.append({"list": piece})

		elif n == "lpar":
			piece = []
			o = 1
			ii = i + 1
			while ii < len(nodes) and o != 0:
				if nodes[ii] == "lpar":
					o += 1
				elif nodes[ii] == "rpar":
					o -= 1
				piece.append(nodes[ii])
				ii += 1
			skip = ii - (i+1)

			piece = process(piece[:-1])[0]
			node.append({"tuple": piece})

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