from sys import *
from utils import *
from lexer import lex
from parser import parse
from preprocessor import process

def cli(name="left",version="0.1",prompt="| %s v%s |>  "):
	try:
		while True:
			code = input(warn + prompt % (name, version) + endc)
			if len(code) == 0:
				continue

			out = parse(process(lex(code))[0][0])
			if out:
				print(bold + green + str(toStr(out)) + endc)
	except (KeyboardInterrupt, EOFError):
		print(warn + "\n\nProcess finished!\n" + endc)
	except IOError:
		raise
	except Exception as e:
		getError()

def main():
	parse(process(lex("pi = 3.14"))[0])
	for i, a in enumerate(argv[1:]):
		try:
			parse(process(lex(a))[0])
		except:
			k = ""
			if str(i)[-1] == "1":
				k = "st"
			elif str(i)[-1] == "2":
				k = "nd"
			elif str(i)[-1] == "3":
				k = "rd"
			else:
				k = "th"
			print("%s%s argument is invalid!" % (i, k))
	cli()


if __name__ == "__main__":
	main()