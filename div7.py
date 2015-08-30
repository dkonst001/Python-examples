import math
import random

for i in range(1,101):
	iIsDividedBy7 = ((i % 7) == 0)
	iIncludesDigit7 = (str(i).find('7') > -1)
	if iIsDividedBy7 and iIncludesDigit7:
		print "hackita!"
	elif iIsDividedBy7:
		print  "!boom!"
	elif iIncludesDigit7:
		print "!bang"
	else:
		print i
	