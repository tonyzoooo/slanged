import requests 
import turtle
from random import randint
import re


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
# Drawing during Hangman
# =============================================================================
def drawHead():
    turtle.seth(90)
    turtle.goto(0,100)
    turtle.down()
    turtle.right(90)
    turtle.circle(20)
    turtle.up()
    
def drawTronc():
    turtle.pensize(10)
    turtle.seth(90)
    turtle.hideturtle()
    turtle.down()
    turtle.forward(100)
    turtle.up()
    
def drawLeftLeg():
    turtle.goto(0,0)
    turtle.seth(-115)
    turtle.down()
    turtle.forward(50)
    turtle.up()
    
def drawRightLeg():
    turtle.goto(0,0)
    turtle.seth(-65)
    turtle.down()
    turtle.forward(50)
    turtle.up()
    
def drawLeftArm():
    turtle.goto(0,100)
    turtle.seth(-115)
    turtle.down()
    turtle.forward(50)
    turtle.up()
    
def drawRightArm():
    turtle.goto(0,100)
    turtle.seth(-65)
    turtle.down()
    turtle.forward(50)
    turtle.up()
    
def œœœ():
    turtle.goto(0,140)
    turtle.seth(90)
    turtle.down()
    turtle.forward(40)
    turtle.up()
    
def bite():
    turtle.goto(0,0)
    turtle.pensize(5)
    turtle.color("red")
    turtle.seth(-90)
    turtle.down()
    turtle.circle(10)
    turtle.left(180)
    turtle.circle(10)
    turtle.pensize(10)
    turtle.forward(20)
    turtle.up()
    
a = input()
drawTronc()
a = input()
drawLeftLeg()
a = input()
drawRightLeg()
a = input()
drawLeftArm()
a = input()
drawRightArm()
a = input()
drawHead()
a = input()
œœœ()
a = input()
bite()
# =============================================================================
# UrbanDictionary API
# =============================================================================

def findWordDefinition(word="lurker"):
    url = "https://api.urbandictionary.com/v0/define?term="+word
    content=requests.get(url)
    data=content.json()
    #classer par score
    return data["list"][0]["definition"]



def findRandomWord():
    url = "https://api.urbandictionary.com/v0/random"
    content=requests.get(url)
    data=content.json()["list"]
    size = len(data)
    word = data[randint(0, size - 1 )]
    name = word["word"]
    while (re.search("\W", name) or 15 < len(name)<=3) :
        word = data[randint(0, size - 1 )]
        name = word["word"]
    #print(json.dumps(data[randint(0,size - 1)], sort_keys=True, indent=4))
    return word



# =============================================================================
# Crosswords
# =============================================================================

def createWordsList():
    words= list()
    words_veri = list()
    while len(words_veri)!= 15:
        word = findRandomWord()
        words.append(word)
        name = word["word"]
        if (name not in words_veri):
            words.append(word)
            words_veri.append(name)
    return sorted(words_veri, key=len).reverse(), words


def createGrid():
    return list(15* [15*['_']])

def compatible(char, word):
    return (char in word)

def compatibleLen(index, mot):
    return (0 <= index <15 and len(mot)<index+1)

def isAvailable(cell):
    return cell=='_'


def putWords(grid, words):
    for word in words:
        index1 = randint(0, 15)
        index2 = randint(0, 15)
        
        
    

# =============================================================================
# Guess the word?
# =============================================================================

def guessTheWord(word):
    print("Try to guess what the word is!")
    print("Here's the definition:")
    print(word["definition"])
    myword = ""
    tries = 3
    while (word["word"].lower()!=myword.lower() and tries !=0 ):
        myword= input("Type in a word:")
        tries-=1
        print("Tries left:" + str(tries))
    if (tries !=0):
        print("Good job! You found it!")
    else:
        print("Boo! You s*ck!")
        print("The word was: " + word["word"] + ".")

guessTheWord(findRandomWord())