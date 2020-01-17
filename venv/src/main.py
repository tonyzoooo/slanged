word = "hello"
nb_letters = 0
letters = set()
hidden_word = list()
counter = 0


def verify(letter, letters):
    return letter in letters

def hasBlank(hidden_word):
    return '_' in hidden_word

def update(letter, letters, word, hidden_word):
    if verify(letter, letters):
        for k in range(len(word)):
            if word[k] == letter:
                hidden_word[k] = letter


for letter in word:
    letters.add(letter)
    nb_letters += 1
    hidden_word.append('_')

while counter <= nb_letters and hasBlank(hidden_word):
    print(hidden_word)
    letter = input("Type in a letter:")
    counter += 1
    update(letter, letters, word, hidden_word)
