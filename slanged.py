#!/usr/bin/env python3
# -*- coding: utf-8 -*-



# =============================================================================
# Imports
# =============================================================================

import tkinter as tk
import requests
import re
from random import randint
#from tkinter import font  as tkfont 
#from itertools import count


# =============================================================================
# Useful functions
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
# Main classes (MVC pattern)
# =============================================================================

#main frame which will contain about everything
class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg = 'blue')
        self.master.title('Slanged!')
        controller1 = HangmanViewController()
        controller2 = GuessWordViewController()
        self.pages = [MainView("Homepage"), controller1.view, controller2.view, 
                        GameView("Crosswords"), GameView("Guess the Word")]
        for page in self.pages:
           page.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
           page.genButtons(page.header, self.pages)
        self.pages[0].show()
    
#basic view which every other other view will inherit from
class View(tk.Frame):
    def __init__(self, name, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.name = name
        self.container = tk.Frame(self)
        self.header = tk.Frame(self)
        self.header.pack(side="top", fill="x", expand=True)
        self.container.pack(side="top", fill = 'x', expand=True)
    
    def show(self):
        self.lift()
       
        
#view for games, specific header        
class GameView(View):
    def __init__(self, name, *args, **kwargs):
        super().__init__(self, bg ='yellow')
        
        
    def genButtons(self, master, pages):
        buttons = list()
        buttonframe = tk.Frame(master)
        buttonframe.pack(side="top", fill="both", expand=True)
        for page in pages:
            if not isinstance(page, HangmanView):
                newBtn = tk.Button(buttonframe, text = page.name, command=page.show)
                buttons.append(newBtn)
                newBtn.pack(side="left")
        newBtn = tk.Button(buttonframe, text = "Leaderboard", command=page.show)
        buttons.append(newBtn)
        newBtn.pack(side="right")
        buttonframe.pack()


#basic game model        
class Game(object):
    def __init__(self, *args, **kwargs):
        self.score = tk.IntVar()
        self.lives = tk.IntVar()   
        self.won = False
        self.guess = False
    
    def updateScore(self):
        lives = self.lives.get()
        score = self.score.get()
        if self.won and lives!=0:
            self.score.set(score +lives)
            self.reset()
        elif not self.won and lives == 1 and score >=5 and not self.guess:
            self.score.set(score-5)
            self.reset()
        elif self.guess and lives != 0:
            self.guess = False
        elif lives == 1 and not self.guess:
            self.reset()
        else:
            self.lives.set(lives-1)
    
        def reset(self):
            self.guess = False
            self.won = False
        

  
#basic controller
class Controller(object):
    def __init__(self, view, game, *args, **kwargs):
        self.view = view
        self.game = game

# =============================================================================
# Homepage
# =============================================================================
        
class MainView(View):
    def __init__(self, name, *args, **kwargs):
        super().__init__(self, bg ='red')

    def genButtons(self, master, pages):
        buttons = list()
        nbGames = 0
        buttonframe = tk.Frame(master)
        buttonframe.place(relx=0.5, rely=0.5, anchor='center')
        for page in pages:
            if isinstance(page, GameView):
                newBtn = tk.Button(buttonframe, text = page.name, command=page.show)
                buttons.append(newBtn)
                binary = "{0:02b}".format(nbGames)
                newBtn.grid(row = int(binary[0]), column= int(binary[1]))
                nbGames+=1
        buttonframe.pack()
      
       
# =============================================================================
# Hangman
# =============================================================================
            
class HangmanView(GameView):
    def __init__(self, name, *args, **kwargs):
        super().__init__(self)
        self.score = tk.StringVar()
        self.letters = tk.StringVar()
        self.lives = tk.StringVar()
        
        playground = tk.Frame(self.container)
        keyboard = tk.Frame(self.container)
        scoreboard = tk.Frame(self.container)
        self.buttons = self.genKeyboard(keyboard)
        self.genScoreboard(scoreboard)
        self.word = self.genPlayground(playground)
        keyboard.pack(side='right')
        scoreboard.pack(side = 'right')
        playground.pack(side='left')
        

    def genScoreboard(self, master):
        labels = []
        score_lbl = tk.Label(master, textvariable= self.score)
        labels.append(score_lbl)
        tries_lbl = tk.Label(master, textvariable = self.letters)
        labels.append(tries_lbl)
        lives_lbl = tk.Label(master, textvariable =self.lives)
        labels.append(lives_lbl)
        score_lbl.pack(side = 'top')
        tries_lbl.pack(side = 'top')
        lives_lbl.pack(side = 'top')
        return labels
        
    def genKeyboard(self, master):
        buttons = []
        value = 65
        for i in range(6):
            for j in range(5):
                letter = chr(value)
                l = tk.Button(master, text = letter)
                l.grid(row = i, column = j)
                value +=1
                buttons.append(l)
                if value > 90 :
                    break
        return buttons
    
    def genPlayground(self, master):
        greet_lbl = tk.Label(master, text='Try to find the word!')
        greet_lbl.pack()
        word_lbl = tk.Label(master)
        word_lbl.pack()
        return word_lbl


class Hangman(Game):
    def __init__(self):    
        super().__init__(self)
        self.score.set(0)
        self.word = findRandomWord()['word']
        self.lives.set(len(self.word))
        self.hword=list(len(self.word)*'_')
        self.letters = []
        
    
    def reset(self):
        self.guess = False
        self.word = findRandomWord()['word']
        self.lives.set(len(self.word))
        self.hword=list(len(self.word)*'_')
        self.letters = []

class HangmanViewController:
    def __init__(self):
        super().__init__()
        self.view = HangmanView("Hangman")
        self.game = Hangman()
        self.bindButtons()
        self.initGame()

    def bindButtons(self):
        for button in self.view.buttons :
            letter = button['text']
            button['command']= lambda x = letter: self.addLetter(x)
        
    def initGame(self):
        hw = tk.StringVar(value = ' '.join(self.game.hword))
        self.view.score.set("Current score: "+ str(self.game.score.get()))
        self.view.letters.set("Input letters:\n"+ str(self.game.letters))
        self.view.lives.set("Remaining attempts: "+ str(self.game.lives.get()))
        self.view.word['textvariable'] = hw


    def addLetter(self, letter):
        hw = tk.StringVar()
        if letter not in self.game.letters :
            self.game.letters.append(letter)
            for i in range(len(self.game.word)):
                if self.game.word[i].upper() == letter :
                    self.game.guess = True
                    self.game.hword[i] = letter
            self.game.won = not '_' in self.game.hword
            self.game.updateScore()
        hw.set(' '.join(self.game.hword))
        self.view.word['textvariable'] = hw
        self.view.letters.set("Input letters:\n"+ ', '.join(self.game.letters))
        self.view.lives.set("Remaining attempts: "+ str(self.game.lives.get()))

# =============================================================================
# Guess the word        
# =============================================================================
    
class GuessWordView(GameView):
    def __init__(self, name, *args, **kwargs):
        super().__init__(self)
        self.score = tk.StringVar()
        self.attempts = tk.StringVar()
        self.lives = tk.StringVar()
        
        playground = tk.Frame(self.container)
        scoreboard = tk.Frame(self.container)
        workzone = tk.Frame(self.container)
        self.genScoreboard(scoreboard)
        self.definition = self.genPlayground(playground)
        self.word = self.genEntry(workzone)
        self.submit = tk.Button(workzone, text = 'Submit')
        scoreboard.pack(side = 'right')
        playground.pack(side='left')
        self.submit.pack()
        workzone.pack(side='left')
        
    def genScoreboard(self, master):
        labels = []
        score_lbl = tk.Label(master, textvariable= self.score)
        labels.append(score_lbl)
        tries_lbl = tk.Label(master, textvariable = self.attempts)
        labels.append(tries_lbl)
        lives_lbl = tk.Label(master, textvariable =self.lives)
        labels.append(lives_lbl)
        score_lbl.pack(side = 'top')
        tries_lbl.pack(side = 'top')
        lives_lbl.pack(side = 'top')
        return labels
    
    def genPlayground(self, master):
        greet_lbl = tk.Label(master, text='Try to guess the word!')
        greet_lbl.pack()
        def_lbl = tk.Label(master)
        def_lbl.pack()
        return def_lbl

    def genEntry(self, master):
        word = tk.Entry(master)
        word.pack()
        return word


class GuessWord(Game):
    def __init__(self):    
        super().__init__(self)
        self.score.set(0)
        self.word = findRandomWord()
        self.lives.set(5)
        self.attempts = []
        
    def reset(self):
        self.guess = False
        self.word = findRandomWord()
        self.lives.set(5)
        self.attempts = []
        
          
class GuessWordViewController:
    def __init__(self):
        super().__init__()
        self.view = GuessWordView("GuessWord")
        self.game = GuessWord()
        self.view.submit['command'] = lambda : self.submit()
        self.initGame()
    
    def initGame(self):
        definition = tk.StringVar(value = "Here's its' definition:\n"+self.game.word['definition'])
        self.view.score.set("Current score: "+ str(self.game.score.get()))
        self.view.attempts.set("Input words:\n"+ str(self.game.attempts))
        self.view.lives.set("Remaining attempts: "+ str(self.game.lives.get()))
        self.view.definition.config(textvariable=definition, width=20)
        
    def submit(self):
        word = self.view.word.get()
        if word.lower() == self.game.word['word'].lower():
            self.game.won = True
        else:
            self.game.attempts.append(word)
        self.game.updateScore()
        self.view.attempts.set("Input words:\n"+ str(self.game.attempts))
        self.view.lives.set("Remaining attempts: "+ str(self.game.lives.get()))
        definition = tk.StringVar(value = "Here's its' definition:\n"+self.game.word['definition'])
        self.view.definition.config(textvariable=definition, width=20)

# =============================================================================
# To be executed...
# =============================================================================
    
if __name__ == "__main__":
    root = tk.Tk()
    main = App(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x600")
    root.mainloop()
