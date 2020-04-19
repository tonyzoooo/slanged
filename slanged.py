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
            if not isinstance(page, MainView):
                self.menubar.add_command(label = page.name, command=page.show)
                
        self.menubar.add_command(label = "Quit (Esc)", command = self.master.destroy)
        master.config(menu=self.menubar)
        self.pages[0].show()
        

    
#basic view which every other other view will inherit from
class View(tk.Frame):
    def __init__(self, name, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.name = name
        self.container = tk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        self.container.pack(side="left", padx=100, pady=30)
    def show(self):
        self.lift()
    
    def hide(self):
        self.lower()
       


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
    def __init__(self, view, game, leaderboard, *args, **kwargs):
        self.view = view
        self.game = game
        self.leaderboard = leaderboard
        
        
# =============================================================================
# Homepage
# =============================================================================
        
class MainView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(self, bg ='red')
        self.name = "Homepage"
        self.container.place(relx=0.5, rely=0.5, anchor='center')

      
       
# =============================================================================
# Hangman
# =============================================================================
            
class HangmanView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(self)
        self.name = "Hangman"
        self.score = tk.StringVar()
        self.letters = tk.StringVar()
        self.lives = tk.StringVar()
        self.drawing = tk.Frame(self.container)
        playground = tk.Frame(self.container)
        keyboard = tk.Frame(self.container)
        scoreboard = tk.Frame(self.container)
        self.buttons = self.genKeyboard(keyboard)
        self.genScoreboard(scoreboard)
        self.word = self.genPlayground(playground)
        playground.grid(row = 1, column = 0)
        scoreboard.grid(row = 1, column = 1)
        keyboard.grid(row = 0,  column = 1)
        self.drawing.grid(row= 0, column=0)
        turtle = turtle_du_pauvre(self.drawing, width=500, height=500, bg = 'blue')
        self.turtle = turtle
        turtle.pack()
        

        
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
        self.view = HangmanView()
        self.game = Hangman()
        self.bindButtons()
        self.initGame()


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

class turtle_du_pauvre(tk.Canvas):
  def __init__(self, master, **args):
    super(turtle_du_pauvre,self).__init__(master, **args)
    self.angle = 0
    self.pos = (250,250)
    self.unit = 0.6
  
  def seth(self,angle):
    self.angle = angle
  
  def goto(self, x, y):
    self.pos = (x,y)
  
  def right(self, angle):
    self.angle = self.angle + angle
  
  def left(self, angle):
    self.angle = self.angle - angle
  
  def forward(self, d):
    angle = self.angle*math.pi/180
    (x,y) = self.pos
    x_unit=self.unit*math.cos(angle)
    y_unit=self.unit*math.sin(angle)
    for k in range(round(d/self.unit)) :
      self.create_line(x,y,round(x+k*x_unit),round(y+k*y_unit))
      self.update()
      time.sleep(0.01)
    (x1,y1) = self.pos
    self.pos = (x+d*x_unit,y+d*y_unit)
    
  def backward(self,d):
    angle = self.angle*math.pi/180 + math.pi
    (x,y) = self.pos
    x_unit=self.unit*math.cos(angle)
    y_unit=self.unit*math.sin(angle)
    for k in range(round(d/self.unit)) :
      self.create_line(x,y,round(x+k*x_unit),round(y+k*y_unit))
      self.update()
      time.sleep(0.01)
    (x1,y1) = self.pos
    self.pos = (x+d*x_unit,y+d*y_unit)
    
  
  def circle(self, r):
    (x,y) = self.pos
    angle = self.angle*math.pi/180
    x_centre = x + r*math.cos(angle)
    y_centre = y + r*math.sin(angle)
    angle_unit = self.unit/r
    new_angle = angle + math.pi
    for k in range(round(2*math.pi*r/self.unit+1)):
      new_x = x_centre + r*math.cos(new_angle)
      new_y = y_centre + r*math.sin(new_angle)
      self.create_line(x,y,new_x,new_y)
      x,y= new_x,new_y
      new_angle = new_angle + angle_unit
      self.update()
      time.sleep(0.01)

# =============================================================================
# Guess the word        
# =============================================================================
    
class GuessWordView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(self)
        self.name = "GuessWord"
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
        self.view = GuessWordView()
        self.game = GuessWord()
        self.view.submit['command'] = lambda : self.submit()
        self.initGame()
    
    def initGame(self):
        my_wrap = textwrap.TextWrapper(width=50)
        new_text = my_wrap.fill(self.game.word['definition'])
        definition = tk.StringVar(value = "Here's its' definition:\n"+new_text)
        self.view.score.set("Current score: "+ str(self.game.score.get()))
        self.view.attempts.set("Input words:\n"+ str(self.game.attempts))
        self.view.lives.set("Remaining attempts: "+ str(self.game.lives.get()))
        self.view.definition.config(textvariable=definition, width=50)
        
    def submit(self):
        word = self.view.word.get()
        if word.lower() == self.game.word['word'].lower():
            self.game.won = True
        else:
            self.game.attempts.append(word)
        self.game.updateScore()
        my_wrap = textwrap.TextWrapper(width=70)
        new_text = my_wrap.fill(self.game.word['definition'])
        self.view.attempts.set("Input words:\n"+ str(self.game.attempts))
        self.view.lives.set("Remaining attempts: "+ str(self.game.lives.get()))
        definition = tk.StringVar(value = "Here's its' definition:\n"+new_text)
        self.view.definition.config(textvariable=definition, width=70)
        
        
# =============================================================================
# Match the word
# =============================================================================
        
class MatchWordView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(self)
        self.name = "MatchWord"
        self.score = tk.StringVar()


class MatchWord(Game):
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
        
          
class MatchWordViewController:
    def __init__(self):
        super().__init__()
        self.view = MatchWordView()
        self.game = MatchWord()

    
    def initGame(self):
        my_wrap = textwrap.TextWrapper(width=70)
        new_text = my_wrap.fill(self.game.word['definition'])
        definition = tk.StringVar(value = "Here's its' definition:\n"+new_text)
        self.view.score.set("Current score: "+ str(self.game.score.get()))
        self.view.definition.config(textvariable=definition, width=70)
        
    def submit(self):
        word = self.view.word.get()
        if word.lower() == self.game.word['word'].lower():
            self.game.won = True
        else:
            self.game.attempts.append(word)
        self.game.updateScore()
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
    root.wm_geometry("800x600")
    root.mainloop()
