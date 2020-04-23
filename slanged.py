#!/usr/bin/env python3
# -*- coding: utf-8 -*-



# =============================================================================
# Imports
# =============================================================================

import tkinter as tk
import requests
import re
from random import randint
import time
import math
import textwrap
#from tkinter import font  as tkfont 
#from itertools import count


# =============================================================================
# Useful functions
# =============================================================================

def findWordDefinition(word="lol"):
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
    while (re.search("\W[0-9]\s", name) or 15 < len(name)<=3) :
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
        master.attributes('-fullscreen', True)
        master.bind("<Escape>", lambda e: master.destroy())
        controller1 = HangmanViewController()
        controller2 = GuessWordViewController()
        self.menubar = tk.Menu(master)
        controller3 = MatchWordViewController()
        #controller4 = CrosswordViewController()
        self.pages = [MainView(), controller1.view, controller2.view, controller3.view]
        for page in self.pages:
            page.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
            if isinstance(page, HangmanView):    
                self.menubar.add_command(label = page.name + " (F1)", command=page.show)
                master.bind("<F1>", lambda e:controller1.view.show())
            elif isinstance(page, GuessWordView):    
                self.menubar.add_command(label = page.name + " (F2)", command=page.show)
                master.bind("<F2>", lambda e:controller2.view.show())
            elif isinstance(page, MatchWordView):    
                self.menubar.add_command(label = page.name + " (F3)", command=page.show)
                master.bind("<F3>", lambda e:controller3.view.show())
        self.menubar.add_command(label = "Quit (Esc)", command = self.master.destroy)
        master.config(menu=self.menubar)
        self.pages[0].show()
        

    
#basic view which every other other view will inherit from
class View(tk.Frame):
    def __init__(self, name, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.name = name
        self.container = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, bg ='white')
        self.container.place(relx=0.5, rely=0.5, anchor='center')
    def show(self):
        self.lift()
        self.focus_set()

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
        elif not self.won and lives == 0 and score >=5 and not self.guess:
            self.score.set(score-5)
            self.reset()
        elif self.guess and lives != 0:
            self.guess = False
        elif lives == 0 and not self.guess:
            self.reset()
        else:
            self.lives.set(lives-1)
    
    def reset(self):
        self.guess = False
        self.won = False
        

  
#basic controller
class Controller(object):
    def __init__(self, view, game, leaderboard, *args, **kwargs):
        self.view = view
        self.game = game
        self.leaderboard = leaderboard
        
        
# =============================================================================
# Homepage
# =============================================================================
        
class MainView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(self, bg ='white')
        self.name = "Homepage"
        self.container.place(relx=0.5, rely=0.5, anchor='center')

      
       
# =============================================================================
# Hangman
# =============================================================================
            
class HangmanView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(self, bg = "white")
        self.name = "Hangman"
        self.score = tk.StringVar()
        self.letters = tk.StringVar()
        self.lives = tk.StringVar()
        image = tk.Frame(self.container)
        self.image = self.genPicture(image)
        dialogbox = tk.Frame(self.container)
        self.dialog = self.genDialog(dialogbox)
        playground = tk.Frame(self.container)
        keyboard = tk.Frame(self.container)
        scoreboard = tk.Frame(self.container)
        self.buttons = self.genKeyboard(keyboard)
        self.genScoreboard(scoreboard)
        self.word = self.genPlayground(playground)
        self.entry = self.genEntry(playground)
        image.grid(row= 0, column=0)
        playground.grid(row = 1, column = 0)
        scoreboard.grid(row = 1, column = 1)
        keyboard.grid(row = 0,  column = 1)
        dialogbox.grid(row = 2, column=0, columnspan=2)
        
    def genDialog(self, master):
        label = tk.Label(master, text="Good luck!")
        label.pack()
        return label

    def genPicture(self, master):
        im = tk.PhotoImage(file = "states/0.png")
        label = tk.Label(master)
        label.im = im
        label.configure(image = label.im, bg = 'white', borderwidth=1, relief=tk.GROOVE)
        label.pack()
        return label
        
    def genEntry(self, master):
        entry = tk.Entry(master)
        entry.pack()
        return entry
    
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
        master.grid(row = 3)
    
        for i in range(6):
          for j in range(4):
            letter = chr(65+4*i+j)
            im = tk.PhotoImage(file = "alphabet/"+letter+".png")
            im = im.subsample(10,10)
            button = tk.Button(master)
            button.text = letter
            button.im = im
            button.configure(image = button.im)
            button.grid(row = i, column= j)
            buttons.append(button)
        
        letter = chr(65+4*6)
        im = tk.PhotoImage(file = "alphabet/"+letter+".png")
        im = im.subsample(10,10)
        button = tk.Button(master)
        button.text = letter
        button.im = im
        button.configure(image = button.im)
        button.grid(row = 6, column= 1)
        buttons.append(button)
        master.grid()
        
        letter = chr(65+4*6+1)
        im = tk.PhotoImage(file = "alphabet/"+letter+".png")
        im = im.subsample(10,10)
        button = tk.Button(master)
        button.text = letter
        button.im = im
        button.configure(image = button.im)
        button.grid(row = 6, column= 2)
        buttons.append(button)
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
        self.lives.set(8)
        self.hword=list(len(self.word)*'_')
        self.letters = []
    
    def updateScore(self):
        lives = self.lives.get()
        score = self.score.get()
        if self.won and lives!=0:
            self.score.set(score +lives)
        elif not self.won and lives == 1 and score >=5 and not self.guess:
            self.score.set(score-5)
        elif self.guess and lives != 0:
            self.guess = False
        else:
            self.lives.set(lives-1)

class HangmanViewController:
    def __init__(self):
        super().__init__()
        self.view = HangmanView()
        self.game = Hangman()
        self.bindButtons()
        self.initGame()
        self.view.entry.bind("<Return>", lambda e:self.allin())


    def bindButtons(self):
        for i in range(len(self.view.buttons)) :
            letter = chr(65 + i)
            self.view.buttons[i]['command']= lambda x = letter: self.addLetter(x)
        
    def initGame(self):
        hw = tk.StringVar(value = ' '.join(self.game.hword))
        self.view.score.set("Current score: "+ str(self.game.score.get()))
        self.view.letters.set("Input letters:\n"+ str(self.game.letters))
        self.view.lives.set("Remaining attempts: "+ str(self.game.lives.get()))
        self.view.word['textvariable'] = hw
        
    def allin(self):
        if self.view.entry.get().lower()==self.game.word.lower():
            self.game.won =True
            self.game.updateScore()
            self.view.dialog.config(text="Damn, you're good!")
        else :
            self.game.lives.set(0)
            self.game.updateScore()
            im = tk.PhotoImage(file = "states/8.png")
            self.im = im
            self.view.image.configure(image = self.im)
            self.view.dialog.config(text="That was reckless dude!\nPress 'R' to play again"+
                                    "\nThe word was actually: "+self.game.word)
        self.view.bind("r",lambda e:self.reset())
        self.view.focus_set()
        
            
    def reset(self):
        self.game.guess = False
        self.game.word = findRandomWord()['word']
        self.game.lives.set(8)
        self.game.hword=list(len(self.game.word)*'_')
        self.game.letters = []
        im = tk.PhotoImage(file = "states/0.png")
        self.im = im
        self.view.image.configure(image = self.im)
        self.view.dialog.config(text="Good luck again!")
        self.view.letters.set("Input letters:\n"+ ', '.join(self.game.letters))
        self.view.lives.set("Remaining attempts: "+ str(self.game.lives.get()))
        self.bindButtons()
        self.view.unbind("r")
        


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
        im = tk.PhotoImage(file = "states/"+str(8-self.game.lives.get())+".png")
        self.im = im
        self.view.image.configure(image = self.im)
        self.view.word['textvariable'] = hw
        self.view.letters.set("Input letters:\n"+ ', '.join(self.game.letters))
        self.view.lives.set("Remaining attempts: "+ str(self.game.lives.get()))
        if (7 > self.game.lives.get()> 4):
            self.view.dialog.config(text="Come on!\nYou can do it!")
        elif 4>=self.game.lives.get()>0 :
            self.view.dialog.config(text="Hmmmm...")
        elif self.game.lives.get()==0:
            self.view.dialog.config(text="Too bad, you lost!\nPress 'R' to play again!"+
                                    "\nThe word was actually: "+self.game.word)
            self.view.bind("r", lambda e:self.reset())
            

              
          

# =============================================================================
# Guess the word        
# =============================================================================
    
class GuessWordView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(self, bg ='white')
        self.name = "GuessWord"
        self.score = tk.StringVar()
        self.attempts = tk.StringVar()
        self.lives = tk.StringVar()
        playground = tk.Frame(self.container)
        scoreboard = tk.Frame(self.container)
        workzone = tk.Frame(self.container)
        dialogbox = tk.Frame(self.container)
        self.dialog = self.genDialog(dialogbox)
        self.genScoreboard(scoreboard)
        self.definition = self.genPlayground(playground)
        self.word = self.genEntry(workzone)
        playground.grid(row = 0, column = 0)
        scoreboard.grid(row = 0, column = 1)
        workzone.grid(row = 1, column = 1)
        dialogbox.grid(row = 2, column=0, columnspan =2)
        
        
    def genDialog(self, master):
        label = tk.Label(master, text="Good luck!")
        label.pack()
        return label
        
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
        
        
          
class GuessWordViewController:
    def __init__(self):
        super().__init__()
        self.view = GuessWordView()
        self.game = GuessWord()
        self.initGame()
        self.view.word.bind("<Return>", lambda e:self.submit())
    
    def updateScore(self):
        lives = self.game.lives.get()
        score = self.game.score.get()
        if self.game.won and lives!=0:
            self.game.score.set(score +lives)
        elif not self.game.won and lives == 1 and score >=5 and not self.game.guess:
            self.game.score.set(score-5)
        elif self.game.guess and lives != 0:
            self.game.guess = False
        else:
            self.game.lives.set(lives-1)
            self.view.dialog.config(text="Wrong!")
    
    def initGame(self):
        my_wrap = textwrap.TextWrapper(width=70)
        new_text = my_wrap.fill(self.game.word['definition'])
        definition = tk.StringVar(value = "Here's its' definition:\n"+new_text)
        self.view.score.set("Current score: "+ str(self.game.score.get()))
        self.view.attempts.set("Input words:\n"+ str(self.game.attempts))
        self.view.lives.set("Remaining attempts: "+ str(self.game.lives.get()))
        self.view.definition.config(textvariable=definition, width=70)
        
    def submit(self):
        word = self.view.word.get()
        if word.lower() == self.game.word['word'].lower():
            self.view.dialog.config(text="GGWP!\n Press 'R' to play again!")
            self.game.won = True
            self.view.bind("r", lambda e : self.reset())
            self.view.word.unbind("<Return>")
            self.view.focus_set()
        else:
            self.game.attempts.append(word)
        self.updateScore()
        self.view.attempts.set("Input words:\n"+ str(self.game.attempts))
        self.view.lives.set("Remaining attempts: "+ str(self.game.lives.get()))
        if self.game.lives.get()==0:
            self.view.dialog.config(text="Better luck next time!\nPress 'R' to play again!\n"+
                                    "The word was "+self.game.word['word'])
            self.view.bind("r", lambda e : self.reset())
            self.view.word.unbind("<Return>")
            self.view.focus_set()
        
    def reset(self):
        self.game.guess = False
        self.game.word = findRandomWord()
        self.game.lives.set(5)
        self.game.attempts = []
        my_wrap = textwrap.TextWrapper(width=70)
        new_text = my_wrap.fill(self.game.word['definition'])
        definition = tk.StringVar(value = "Here's its' definition:\n"+new_text)
        self.view.score.set("Current score: "+ str(self.game.score.get()))
        self.view.attempts.set("Input words:\n"+ str(self.game.attempts))
        self.view.lives.set("Remaining attempts: "+ str(self.game.lives.get()))
        self.view.definition.config(textvariable=definition, width=70)
        self.view.dialog.config(text="Good luck!")
        self.view.unbind("r")
        self.view.word.bind("<Return>", lambda e:self.submit())
        
        
# =============================================================================
# Match the word
# =============================================================================
        
class MatchWordView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(self, bg = 'white')
        self.name = "MatchWord"
        self.score = tk.StringVar()
        self.buttonvar = tk.IntVar()
        buttonframe = tk.Frame(self.container)
        playground=tk.Frame(self.container)
        self.definition = self.genPlayground(playground)
        self.buttons =[tk.Radiobutton(buttonframe), tk.Radiobutton(buttonframe),tk.Radiobutton(buttonframe)]
        self.submit = tk.Button(playground, text="Submit")
        self.submit.pack()
        for button in self.buttons:
            button.pack(side="left")
        buttonframe.pack()
        playground.pack()
        scoreboard = tk.Frame(self.container)
        self.genScoreboard(scoreboard)
        scoreboard.pack()
        
    def genScoreboard(self, master):
        score_lbl = tk.Label(master, textvariable= self.score)
        score_lbl.pack(side = 'top')
        return score_lbl
        
    def genPlayground(self, master):
        greet_lbl = tk.Label(master, text='Try to guess the word!')
        greet_lbl.pack()
        def_lbl = tk.Label(master)
        def_lbl.pack()
        return def_lbl


class MatchWord(Game):
    def __init__(self):    
        super().__init__(self)
        self.score.set(0)
        
        self.word1 = findRandomWord()
        self.word2 = findRandomWord()
        self.word3 = findRandomWord()
        value = randint(1,3)
        if value == 1:
            self.word=self.word1
        elif value == 2:
            self.word=self.word2
        else:
            self.word=self.word3
        
    def updateScore(self):
        score = self.score.get()
        if self.won:
            self.score.set(score + 1)
        self.reset()

    
    def reset(self):
        self.guess = False
        self.won = False
        self.word1 = findRandomWord()
        self.word2 = findRandomWord()
        self.word3 = findRandomWord()
        value = randint(1,3)
        if value == 1:
            self.word=self.word1
        elif value == 2:
            self.word=self.word2
        else:
            self.word=self.word3
        
          
class MatchWordViewController:
    def __init__(self):
        super().__init__()
        self.view = MatchWordView()
        self.game = MatchWord()
        self.view.submit.config(command=lambda:self.submit())
        self.initGame()
        self.view.submit.bind("<Return>", lambda e:self.submit())


    
    def initGame(self):
        self.view.score.set("Current score: "+ str(self.game.score.get()))
        self.view.buttons[0].config(text=self.game.word1["word"], variable=self.view.buttonvar, value = 1)
        self.view.buttons[1].config(text=self.game.word2["word"],variable=self.view.buttonvar, value = 2)
        self.view.buttons[2].config(text=self.game.word3["word"], variable=self.view.buttonvar, value = 3)
        my_wrap = textwrap.TextWrapper(width=70)
        new_text = my_wrap.fill(self.game.word['definition'])
        definition = tk.StringVar(value = "Here's its' definition:\n"+new_text)
        self.view.score.set("Current score: "+ str(self.game.score.get()))
        self.view.definition.config(textvariable=definition, width=70)
        
    def submit(self):
        ans = self.view.buttonvar.get()
        for button in self.view.buttons:
            if button['value']==ans:
                if button['text'].lower() == self.game.word['word'].lower():
                    self.game.won = True
        self.view.buttonvar.set(0)
        self.game.updateScore()
        self.view.score.set("Current score: "+ str(self.game.score.get()))
        self.view.buttons[0].config(text=self.game.word1["word"], variable=self.view.buttonvar, value = 1)
        self.view.buttons[1].config(text=self.game.word2["word"],variable=self.view.buttonvar, value = 2)
        self.view.buttons[2].config(text=self.game.word3["word"], variable=self.view.buttonvar, value = 3)
        my_wrap = textwrap.TextWrapper(width=70)
        new_text = my_wrap.fill(self.game.word['definition'])
        definition = tk.StringVar(value = "Here's its' definition:\n"+new_text)
        self.view.definition.config(textvariable=definition, width=70)

# =============================================================================
# To be executed...
# =============================================================================
    
if __name__ == "__main__":
    root = tk.Tk()
    main = App(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
