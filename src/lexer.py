from utils import *
from multitry import *

def lex(string):
	node = []

	isstr = 0
	s = ""

	num = 0

	tok = ""
	for i, c in enumerate(string):
		if c not in idChars and c != ".":
			if tok != "" and tok != " " and tok != "\t" and tok != "\n":
				try:
					node.append({"number": test('str(int("' + tok + '"))', 'str(float("' + tok + '"))')})
					num = 0
				except:
					node.append({"id": tok})
			tok = ""

		tok += c

		if num == 1 and c not in list(map(str, range(0,9))) and c != ".":
			num = 0
			node.append({"number": tok[:-1]})
			tok = c

		if tok == '"':
			if isstr == 0:
				isstr = 1
			elif string[i-1] != "\\":
				isstr = 0
				node.append({"string": s})
				s = ""
			tok = ""

		elif isstr == 1:
			s += tok
			tok = ""

		elif tok == ",":
			node.append("comma")
			tok = ""

		elif tok in opers:
			node.append({"operator": tok})
			tok = ""

		elif tok == "(":
			node.append("lpar")
			tok = ""

		elif tok == ")":
			node.append("rpar")
			tok = ""

		elif tok == "[":
			node.append("lsq")
			tok = ""

		elif tok == "]":
			node.append("rsq")
			tok = ""

		elif tok in list(map(str, range(0,9))):
			num = 1

		elif tok == " " and isstr == 0:
			tok = ""

		elif tok == "\n" and isstr == 0:
			isstr = 0
			s = ""
			tok = ""
	if tok != "":
		h = True
		for c in tok:
			if c not in idChars and c != ".":
				node.append(lex(tok)[0])
				h = False
		if h and tok != " " and tok != "\t" and tok != "\n":
			try:
				node.append({"number": test('str(int("' + tok + '"))', 'str(float("' + tok + '"))')})
			except:
				node.append({"id": tok})
	#print(node)
	return node