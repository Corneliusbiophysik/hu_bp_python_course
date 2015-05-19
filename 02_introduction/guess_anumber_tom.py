from random import randint

def main():
	zahl=randint(1,100)
	n=5

	while True:
		try: 
			geraten=int(raw_input('Du hast ' + n + ' Verusche.' 'Rate eine Zahl zwischen 1 und 100:'))
			if geraten < 1 or geraten > 99:
				continue
		except: 
			print 'Gib bitte eine ganze Zahl zwischen 1 und 100 ein!'
			continue
		if geraten < zahl:
			print u'Du hast zu klein geschaetzt.'
		elif geraten > zahl:
			print u'Das ist leider zu hoch!'
		elif geraten == zahl:
			print "Richtig!"
			break
	print geraten


if __name__ == '__main__':
	main()

