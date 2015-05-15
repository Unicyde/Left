def replace(sequence, replacement, lst, expand=False):
	out = list(lst)
	for i, e in enumerate(lst):
		if e == sequence[0]:
			i1 = i
			f = 1
			for e1, e2 in zip(sequence, lst[i:]):
				if e1 != e2:
					f = 0
					break
				i1 += 1
			if f == 1:
				del out[i:i1]
				if expand:
					for x in list(replacement):
						out.insert(i, x)
				else:
					out.insert(i, replacement)
	return out

if __name__ == "__main__":
	print(replace([1,2,3], 123, [3,2,1,5,6,3,9,0,6,5,1,5,1,2,3,]))
	print(replace(["+", "="], "+=", [3, "blah", "+", "foo", "=", "+", "="]))
	print(replace([1,2,3], {3,2,1}, [3,2,1,5,6,3,9,0,6,5,1,5,1,2,3,]))