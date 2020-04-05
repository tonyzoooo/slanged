#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 16:42:31 2020

@author: tonyz
"""

# =============================================================================
# Imports
# =============================================================================

import tkinter as tk
from tkinter import font  as tkfont 
from itertools import count

# =============================================================================
# Classes
# =============================================================================

class App(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.master.title('Slanged!')
        p1 = MainView(self)
        p2 = HangmanView(self)
        
        #buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        #buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)


        #b1 = tk.Button(buttonframe, text="Homepage", command=p1.lift)
        #b2 = tk.Button(buttonframe, text="Hangman", command=p2.lift)


        #b1.pack(side="left")
        #b2.pack(side="right")
        #my_controller = HangmanController(ty, p2)
        #my_controller.initGame(ty, p2)
        
        p1.show()


# =============================================================================
# Views
# =============================================================================

class View(tk.Frame):
    def __init__(self, model=None, view=None):
        tk.Frame.__init__(self, model, view)
    def show(self):
        self.lift()

class GameView(View):
    _ids = count(0)
    ide = next(_ids)
    self.genHeader()
        
    def genHeader():
        buttons = list()
        buttonframe = tk.Frame()
        buttonframe.pack(side="top", fill="x", expand=False)
        for i in range(ide):
            newBtn = tk.Button(buttonframe, text = str(i))
            newBtn.append(buttons)
            newBtn.pack(side="left")
            buttonframe.pack()
        return buttons
    

class HangmanView(GameView):
    def __init__(self, *args, **kwargs):
       GameView.__init__(self, *args, **kwargs)
       self.container = tk.Frame(self)
       self.letter = tk.StringVar()
       
       self.kbFrame = tk.Frame(self.container)
       self.hmCanvas = tk.Canvas(self.container)
       self.scoreFrame = tk.Frame(self.container)
       
       self.genKeyboard(self.kbFrame)
       self.genCanvas(self.hmCanvas)
       self.used_letters = tk.Label(self.scoreFrame, text = "Hello")
       self.used_letters.pack()
       self.genScoreboard(self.scoreFrame)
       self.kbFrame.pack()
       self.hmCanvas.pack()
       self.scoreFrame.pack()
       self.container.pack()
       
    def getLetter(self):
        return self.letter.get()
        
    def setLetter(self, letter):
        self.letter.set(letter)
        self.used_letters.config(text = "Tried: " + self.getLetter())
       
    def genKeyboard(self, master = None):
        value = 65
        for i in range(6):
            for j in range(5):
                letter = chr(value)
                l = tk.Button(master, text = letter, command=lambda x = letter: self.setLetter(x))
                l.grid(row = i, column = j)
                value +=1
                if value > 90 :
                    break
        
        
                
    def genCanvas(self, master = None):
        label = tk.Label(master, text= "Hello bitches")
        label.pack()

    def genScoreboard(self, master = None):
        label = tk.Label(master, text= "Current score:")
        label.pack()

class MainView(View):
   def __init__(self, *args, **kwargs):
       View.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Homepage")
       label.pack(side="top", fill="both", expand=True) 





      


# =============================================================================
# Models
# =============================================================================

class Observable(object):
    def __init__(self, initialValue=None):
        self.data = initialValue
        self.callbacks = {}

    def addCallback(self, func):
        self.callbacks[func] = 1

    def delCallback(self, func):
        del self.callback[func]

    def _docallbacks(self):
        for func in self.callbacks:
             func(self.data)

    def set(self, data):
        self.data = data
        self._docallbacks()

    def get(self):
        return self.data

    def unset(self):
        self.data = None


class Game(object): #model
    def __init__(self):
        self.score =Observable(0)
    
    def addScore(self, value):
        self.score.set(self.score.get()+value)

        
"""class Leaderboard(object):
    def __init__():
"""


class Hangman(Game):
    def __init__(self, word):
        Game.__init__(self)
        self.__word = word # __ attribut privé
        self.__nb_letters = len(word)
        self.__hidden_word = list(self.__nb_letters * '_')

    @property #pattern decorateur
    def word(self): #getter de word
        return self.__word

    @word.setter
    def word(self, value): #setter de word
        self.__word = value

    def __hasBlank(self):
        return '_' in self.__hidden_word

    def __update(self, letter, letters, used_letters):
        used_letters.add(letter)
        if letter in letters:
            for k in range(self.__nb_letters):
                if self.__word[k] == letter:
                    self.__hidden_word[k] = letter
    
    def __try(self, letter, letters, used_letters, counter):
        counter += 1
        self.__update(letter, letters, used_letters)
    

# =============================================================================
# Matching words with definitions
# =============================================================================

#class Matching(object):



# =============================================================================
# Controllers
# =============================================================================

class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
class HangmanController(Controller):
    def __init__(self, *args, **kwargs):
        Controller.__init__(self, Hangman, HangmanView)
    
    def initGame(self, Hangman, HangmanView):
        letter = HangmanView.getLetter()
        nb_letters = Hangman.__nb_letters
        letters = set(letter for letter in Hangman.__word)
        counter = 0
        used_letters = set()
        
        while counter <= nb_letters and self.__hasBlank():
            Hangman.__try(Hangman, letter, letters, used_letters, counter)
        
        if Hangman.__hasBlank():
            print("Too bad, you lost! The word was " + Hangman.__word)
        else:
            print("Great job! You got it!")


if __name__ == "__main__":
    root = tk.Tk()
    main = App(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x600")
    root.mainloop()

  