from time import strftime
from pyfiglet import Figlet
import sys
import locale

def date(format="%Y %d %b, %A", font="graceful"):
	f = Figlet(font=font)
	locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
	date_text = strftime(format)
	return f.renderText(date_text)

if __name__ == "__main__":
	argv = sys.argv
	if (len(argv) == 1):
		print(date())
	elif (len(argv) == 2):
		print(date(argv[1]))
	elif (len(argv) == 3):
		print(date(argv[1], argv[2]))
