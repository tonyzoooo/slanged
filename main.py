import json
import requests 
from random import randint


# =============================================================================
# Hangman
# =============================================================================

def verify(letter, letters):
    return letter in letters

def hasBlank(hidden_word):
    return '_' in hidden_word

def update(letter, letters, word, hidden_word):
    if verify(letter, letters):
        for k in range(len(word)):
            if word[k] == letter:
                hidden_word[k] = letter

def hangman(word = "hello"):
    nb_letters = 0
    letters = set()
    hidden_word = list()
    counter = 0

    for letter in word:
        letters.add(letter)
        nb_letters += 1
        hidden_word.append('_')
    
    while counter <= nb_letters and hasBlank(hidden_word):
        print(hidden_word)
        letter = input("Type in a letter:")
        counter += 1
        update(letter, letters, word, hidden_word)


# =============================================================================
# UrbanDictionary API
# =============================================================================

def findWordDefinition(word="lurker"):
    url = "https://api.urbandictionary.com/v0/define?term="+word
    content=requests.get(url)
    data=content.json()
    return data["list"][0]["definition"]

def findRandomWord():
    url = "https://api.urbandictionary.com/v0/random"
    content=requests.get(url)
    data=content.json()["list"]
    size = len(data)
    print(json.dumps(data[randint(0,size - 1)], sort_keys=True, indent=4))
    return data[randint(0, size - 1 )]
