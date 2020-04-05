#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
#from tkinter import font  as tkfont 
#from itertools import count


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg = 'blue')
        self.master.title('Slanged!')
        controller = HangmanViewController()
        self.pages = [MainView("Homepage"), controller.view, GameView("Matching"), 
                        GameView("Crosswords"), GameView("Guess the Word")]

        
        for page in self.pages:
           page.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
           page.genButtons(page.header, self.pages)
        self.pages[0].show()
    

class View(tk.Frame):
    def __init__(self, name, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.name = name
        self.container = tk.Frame(self)
        self.header = tk.Frame(self)
        self.header.pack(side="top", fill="both", expand=True)
        self.container.pack()
    
    def show(self):
        self.lift()
        
    @property
    def name(self):
        return self.__name
    
    @name.setter 
    def name(self, value):
        self.__name = value
    

        
class MainView(View):
    def __init__(self, name, *args, **kwargs):
        super().__init__(self, bg ='red')
        label = tk.Label(self, text="Homepage")
        label.pack(side="top", fill="x", expand=False) 
       
    def genButtons(self, master, pages):
        buttons = list()
        nbGames = 0
        buttonframe = tk.Frame(master)
        buttonframe.pack(side="top", fill="x", expand=False)
        for page in pages:
            if isinstance(page, GameView):
                newBtn = tk.Button(buttonframe, text = page.name, command=page.show)
                buttons.append(newBtn)
                binary = "{0:02b}".format(nbGames)
                newBtn.grid(row = int(binary[0]), column= int(binary[1]))
                nbGames+=1
        buttonframe.pack()
      
       
class GameView(View):
    def __init__(self, name, *args, **kwargs):
        super().__init__(self, bg ='yellow')
        
        
    def genButtons(self, master, pages):
        buttons = list()
        buttonframe = tk.Frame(master)
        buttonframe.pack(side="top", fill="x", expand=False)
        for page in pages:
            if not isinstance(page, HangmanView):
                newBtn = tk.Button(buttonframe, text = page.name, command=page.show)
                buttons.append(newBtn)
                newBtn.pack(side="left")
        newBtn = tk.Button(buttonframe, text = "Leaderboard", command=page.show)
        buttons.append(newBtn)
        newBtn.pack(side="right")
        buttonframe.pack()
            
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
            self.score.set(lives + 1)
            self.reset()
        elif not self.won and lives == 0 and score !=0:
            self.score.set(score-1)
            self.reset()
        elif self.guess and lives != 0:
            self.guess = False
        elif lives == 0:
            self.reset()
        else:
            self.lives.set(lives-1)
    
        def reset(self):
            self.guess = False
            self.game.won = False

class Hangman(Game):
    def __init__(self):    
        super().__init__(self)
        self.score.set(0)
        self.word = 'hello'
        self.lives.set(len(self.word))
        self.letters = []
        
    
    def reset(self):
        self.guess = False
        self.word = 'goodbye'
        self.lives.set(len(self.word))
        self.letters = []

class Controller(object):
    def __init__(self, view, game, *args, **kwargs):
        self.view = view
        self.game = game

class HangmanViewController:
    def __init__(self):
        super().__init__()
        self.view = HangmanView("Hangman")
        self.game = Hangman()
        self.hword = list('_'*len(self.game.word))
        self.bindButtons()
        self.initGame()

        
    def bindButtons(self):
        for button in self.view.buttons :
            letter = button['text']
            button['command']= lambda x = letter: self.addLetter(x)
        
    def initGame(self):
        hw = tk.StringVar(value = ' '.join(self.hword))
        self.view.score.set("Current score: "+ str(self.game.score.get()))
        self.view.letters.set("Input letters:\n"+ str(self.game.letters))
        self.view.lives.set("Remaining attempts: "+ str(self.game.lives.get()))
        self.view.word['textvariable'] = hw
        
    

    

    def addLetter(self, letter):
        hw = tk.StringVar()
        if letter not in self.game.letters :
            self.game.letters.append(letter)
            for i in range(len(self.hword)):
                if self.game.word[i].upper() == letter :
                    self.game.guess = True
                    self.hword[i] = letter
                    hw.set(' '.join(self.hword))
                    self.view.word['textvariable'] = hw
            self.game.won = not '_' in self.hword
            self.game.updateScore()
                    
        
        self.view.letters.set("Input letters:\n"+ ', '.join(self.game.letters))
        self.view.lives.set("Remaining attempts: "+ str(self.game.lives.get()))
        while self.game.won or self.game.lives.get()==0:
            self.hword = list('_'*len(self.game.word))
            self.game.won = False
            self.initGame()
        
    


    
    
if __name__ == "__main__":
    root = tk.Tk()
    main = App(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x600")
    root.mainloop()
