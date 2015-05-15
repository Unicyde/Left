import sys, os, traceback
from multitry import *
import string

# Colors
pink = '\033[95m'
blue = '\033[94m'
green = '\033[92m'
yellow = '\033[93m'
red = '\033[91m'
endc = '\033[0m'
bold = '\033[1m'
underline = '\033[4m'

# Presets
warn = yellow + bold
fail = bold + red

# Traceback printer
def getError():
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	t, f, n =  exc_type.__name__, str(fname), str(exc_tb.tb_lineno)

	if n[-1] == "1" and (int(n) < 10 or int(n) > 19):
		print(fail + "Got `%s` in file `%s` at %sst line!" % (t, f, n) + endc)
	elif n[-1] == "2" and (int(n) < 10 or int(n) > 19):
		print(fail + "Got `%s` in file `%s` at %snd line!" % (t, f, n) + endc)
	elif n[-1] == "3" and (int(n) < 10 or int(n) > 19):
		print(fail + "Got `%s` in file `%s` at %srd line!" % (t, f, n) + endc)
	else:
		print(fail + "Got `%s` in file `%s` at %sth line!" % (t, f, n) + endc)

	if input(underline + "Do you want to see the error? (y/n)" + endc + "  ") in ["y","Y","yes","Yes","YES"]:
		raise exc_obj


idChars = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(map(str, range(0,10))) + ["_"]
opers = ["+","-","*","/","^","=","!","~","?"]

def contains(a1, a2):
	return len([x for x in a1 if x in a2]) > 0

def genType(value):
	if type(value) is dict:
		return value
	elif type(value) is list:
		return {"list": [genType(x) for x in value]}
	elif type(value) is int or type(value) is float:
		return {"number": str(value)}
	else:
		try:
			value = {"number": test('str(int("' + value + '"))', 'str(float("' + value + '"))')}
		except:
			#print(value, type(value))
			value = {"string": value}
		finally:
			return value

def toStr(node):
	if type(node) is not dict:
		return node
	if "list" in node:
		return "[" + ", ".join([toStr(x) for x in node["list"]]) + "]"
	else:
		return list(node.values())[0]