from random import randint#
print 'In this game, you can guess a random number'

i=1
n=0
y=randint(0,100)
while i:
	x=int(raw_input("Please insert a number between 0 and 100: "))
	
	if x==y:
		print 'You are right!'
		print 'You tried {} times' .format(n)
		i=int(raw_input("Again, 1 yes 0 no: "))
	elif x<0 or x>100:
		print 'The input was not valueable. Please try again!'
	else:
		print 'The input was not correct. Please try again!'
		n=n+1
