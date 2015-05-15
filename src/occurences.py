def lrep(old, new, string, number=1):
	li = str(string).lsplit(old, number)
	return new.join(li)

def rrep(old, new, string, number=1):
	li = str(string).rsplit(old, number)
	return new.join(li)