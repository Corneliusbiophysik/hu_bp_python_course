from random import randint

def main():
	zahl=randint(1,100)
	VERSUCHE = 5 
	n = VERSUCHE + 1 

	while True:
		n = n - 1
		if n == 0:
			try: 
				entscheidung = str(raw_input('Du hast leider keinen Versuch mehr! Willst du nochmal Spielen? y/n: ')) 
				if entscheidung == 'y':
					n = VERSUCHE + 1 
					continue
				elif entscheidung == 'n':
					break
			except: 
				print 'Gib bitte y oder n ein!'
				n = 1
		try: 
			geraten=int(raw_input('Du hast noch ' + str(n) + ' Versuche. Rate eine Zahl zwischen 1 und 100: '))
			if geraten < 1 or geraten > 99:
				continue
		except: 
			print 'Gib bitte eine ganze Zahl zwischen 1 und 100 ein!'
			n = n + 1 
			continue
		if geraten < zahl:
			print u'Du hast zu klein geschaetzt.'
		elif geraten > zahl:
			print u'Das ist leider zu hoch!'
		elif geraten == zahl:
			print "Richtig!"
			print geraten
			break
	


if __name__ == '__main__':
	main()

