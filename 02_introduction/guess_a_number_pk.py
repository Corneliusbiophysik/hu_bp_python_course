from random import randint

def guess():
    n=randint(0, 100)
    print 'Guess a number between 0 and 100!'
    x = int(raw_input('Whats your guess? '))
    count_guess = 1
    while x != n:
        if x < n:
            print 'Keep guessing, the right number is bigger than yours!'
            x = int(raw_input('Whats your new guess? '))
            count_guess = count_guess + 1
        else:
            print 'Keep guessing, the right number is smaler than yours!'
            x = int(raw_input('Whats your new guess? '))
            count_guess = count_guess + 1
    if x == n:
        print 'Awesome! You are right!'
        print 'Your needed counts:'
        print count_guess
        y = raw_input('Do you want to play again? ')
        if y == 'yes':
            guess()
        else:
            print 'Goodbye!'

guess()