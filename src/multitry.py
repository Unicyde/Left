from occurences import *

def test(*args):
	for a in args:
		try:
			try:
				return eval(str(a))
			except:
				if "\n" in a:
					for x in a.split("\n"):
						try:
							return eval(str(a))
						except:
							exec(str(a))
		except:
			pass

	raise IndexError("All tries failed!")