import textdistance
import random

def bullscows(guess, secret):
    bulls = textdistance.hamming.similarity(guess, secret)
    cows = textdistance.bag.similarity(guess, secret) - bulls
    return (bulls, cows)

def ask(prompt, valid=None):
    word = input(prompt)
    if valid:
        while word not in valid:
            word = input("Invalid word, try again: ")
    return word

def inform(format_string, bulls, cows):
    print(format_string.format(bulls, cows))

def gameplay(ask, inform, words):
    secret = random.choice(words)
    attempts = 0
    result = (0,0)
    while result[0] < len(secret):
        guess = ask("Введите слово: ", words)
        result = bullscows(guess, secret)
        inform("Быки {}, Коровы {}", result[0], result[1])
        attempts += 1
    return attempts

numbers = [str(i) for i in range(10,100)]
print(gameplay(ask, inform, numbers))
