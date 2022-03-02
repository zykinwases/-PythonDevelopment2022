import textdistance
import random
import urllib.request
import sys

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

argv = sys.argv[1:]

if argv[0].startswith("http"):
    vocabulary = [line.decode("utf-8").strip() for line in urllib.request.urlopen(argv[0])]
else:
    f = open(path, "r")
    vocabulary = [line.strip() for line in f.readlines()]

length = 5
if len(argv) == 2:
    length = int(argv[1])
truncated = [word for word in vocabulary if len(word) == length]
vocabulary = truncated

print("Количество попыток: ", gameplay(ask, inform, vocabulary))
