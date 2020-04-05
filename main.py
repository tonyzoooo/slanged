import requests 
import turtle
from random import randint
import re
from games import Hangman
from ui import App

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
# Main program
# =============================================================================
def main():
    word = findRandomWord()['word']
    hangman = Hangman(word)
    hangman.initGame()
    print(hangman.word)
    print(findWordDefinition(word=word))

if __name__ == '__main__':
    main()


"""

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



def drawBase():
    turtle.right(90)
    turtle.forward(100)
    turtle.backward(5)
    turtle.left(90)

def drawVertical():
    turtle.forward(30)
    turtle.backward(5)


def drawHangMan():
    drawBase()
    drawVertical()
    turtle.done()






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
    return sorted(words_veri, key=len).reverse(), sorted(words, key=len)

def createGrid():
    return list(15* [15*['_']])

def compatibleWord(char, word):
    return (char in word)

def firstWord(index, word):
    return 15 - index < len(word) 

    

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


some useful links ??
https://stackoverflow.com/questions/55444898/can-i-stack-a-frame-on-top-of-a-canvas-tkinter
https://github.com/riverrun/genxword/blob/master/genxword/calculate.py
https://github.com/jameslinjl/Hangman/blob/master/hangmantext.py

"""