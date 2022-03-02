import textdistance

def bullscows(guess, secret):
    bulls = textdistance.hamming.similarity(guess, secret)
    cows = textdistance.bag.similarity(guess, secret) - bulls
    return((bulls, cows))

print(bullscows("12345", "12345"))
print(bullscows("12345", "12456"))
print(bullscows("12345", "67890"))
