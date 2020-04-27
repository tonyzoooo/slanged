#!/usr/bin/env python3
# -*- coding: utf-8 -*-



# =============================================================================
# Imports
# =============================================================================

import tkinter as tk
import requests
import re
from random import randint
import textwrap
import time
import math


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
    while not(re.search("^[A-Za-z]*$", name) or 15 < len(name)<=3) or name in word['definition']:
        word = data[randint(0, size - 1 )]
        name = word["word"]
    #print(json.dumps(data[randint(0,size - 1)], sort_keys=True, indent=4))
    Dict = {'word' : name, 'definition' : findWordDefinition(name) }
    return Dict

def storeWord(word):
    Dict = {'word' : word, 'definition' : findWordDefinition(word) }
    with open("vocabulary.txt", "a+") as file:
        for key, value in Dict.items():
            file.write('%s:%s\n' % (key, value))
        file.write("\n\n")

   
def storeCompleteWord(word):
    with open("vocabulary.txt", "a+") as file:
        for key, value in word.items():
            file.write('%s:%s\n' % (key, value))
        file.write("\n\n")

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
        self.menubar.config(font=('Helvetica bold', 12))
        master.config(menu=self.menubar)
        self.pages[0].show()
        

    
#basic view which every other other view will inherit from
class View(tk.Frame):
    def __init__(self, name, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.name = name
        top = tk.Frame(self, bg ='white')
        self.container = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, bg ='white')
        top.pack()
        self.container.place(relx=0.5, rely=0.5, anchor='center')
        self.title = tk.Label(top, text= self.name, font=('Helvetica bold', 28))
        self.title.pack()
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
        elif not self.won and lives == 0 and score <5 and not self.guess:
            self.score.set(0)
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
        self.title.config(text = self.name)
        self.gamename = tk.Label(self.container, text="Slanged!", bg = 'white',  
                                  font = ('Helvetica', 40))
        self.description = tk.Label(self.container, 
                                    text = "An interactive way of learning English colloquialism", 
                                    bg = 'white')
        self.authors = tk.Label(self.container, text = "Made by L. Mazou and T. Zhou", bg = 'white')
        self.gamename.pack()
        self.description.pack()
        self.authors.pack()

      
       
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
        turtle = turtle_du_pauvre(self.container, width=500, height=600, bg = "white")
        self.turtle = turtle
        dialogbox = tk.Frame(self.container, bg = 'white')
        self.dialog = self.genDialog(dialogbox)
        playground = tk.Frame(self.container, bg = 'white')
        keyboard = tk.Frame(self.container, bg = 'white')
        scoreboard = tk.Frame(self.container, bg = 'white', relief=tk.GROOVE, borderwidth=2)
        self.buttons = self.genKeyboard(keyboard)
        self.genScoreboard(scoreboard)
        self.word = self.genPlayground(playground)
        self.entry = self.genEntry(playground)
        self.title.config(text=self.name)
        self.turtle.grid(row=1, column =0)
        playground.grid(row = 2, column = 0)
        scoreboard.grid(row = 2, column = 1)
        keyboard.grid(row = 1,  column = 1)
        dialogbox.grid(row = 3, column=0, columnspan=2)
        
    def genDialog(self, master):
        label = tk.Label(master, text="Good luck!", bg = 'white', font=('Helvetica', 16))
        label.pack()
        return label

        
    def genEntry(self, master):
        entry = tk.Entry(master, font=('Helvetica', 16))
        entry.pack()
        return entry
    
    def genScoreboard(self, master):
        labels = []
        score_lbl = tk.Label(master, textvariable= self.score, bg = 'white', font=('Helvetica', 16))
        labels.append(score_lbl)
        tries_lbl = tk.Label(master, textvariable = self.letters, bg = 'white', font=('Helvetica', 16))
        labels.append(tries_lbl)
        lives_lbl = tk.Label(master, textvariable =self.lives, bg = 'white', font=('Helvetica', 16))
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
            im = im.subsample(7,7)
            button = tk.Button(master, bg = 'white')
            button.text = letter
            button.im = im
            button.configure(image = button.im)
            button.grid(row = i, column= j)
            buttons.append(button)
        
        letter = chr(65+4*6)
        im = tk.PhotoImage(file = "alphabet/"+letter+".png")
        im = im.subsample(7,7)
        button = tk.Button(master, bg = 'white')
        button.text = letter
        button.im = im
        button.configure(image = button.im)
        button.grid(row = 6, column= 1)
        buttons.append(button)
        master.grid()
        
        letter = chr(65+4*6+1)
        im = tk.PhotoImage(file = "alphabet/"+letter+".png")
        im = im.subsample(7,7)
        button = tk.Button(master, bg = 'white')
        button.text = letter
        button.im = im
        button.configure(image = button.im)
        button.grid(row = 6, column= 2)
        buttons.append(button)
        return buttons
    
    def genPlayground(self, master):
        greet_lbl = tk.Label(master, text='Try to find the word!', bg = 'white', font=('Helvetica', 16))
        greet_lbl.pack()
        word_lbl = tk.Label(master, font=('Helvetica', 11))
        word_lbl.pack()
        return word_lbl
    
class turtle_du_pauvre(tk.Canvas):
  def __init__(self, master, **args):
    super(turtle_du_pauvre,self).__init__(master, **args)
    self.angle = 0
    self.pos = (250,250)
    self.unit = 1
    self.speed = 100
    
  def reset(self):
    self.delete("all")
    self.pos = (250,250)  
    self.angle=0
  
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
      time.sleep(0.01/self.speed)
    (x1,y1) = self.pos
    self.pos = (x+d*x_unit,y+d*y_unit)
    
  def backward(self,d):
    angle = self.angle*math.pi/180 + math.pi
    (x,y) = self.pos
    x_unit=self.unit*math.cos(angle)
    y_unit=self.unit*math.sin(angle)
    for k in range(round(d/math.sqrt(2*(self.unit**2)))) :
      self.create_line(x,y,round(x+k*x_unit),round(y+k*y_unit))
      self.update()
      time.sleep(0.01/self.speed)
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
      time.sleep(0.01/self.speed)
      
  def move(self,x,y):
    (bx,by) = self.pos
    self.pos = (bx+x,by+y)

class Hangman(Game):
    def __init__(self):    
        super().__init__(self)
        self.score.set(0)
        self.word = findRandomWord()['word']
        self.lives.set(11)
        self.hword=list(len(self.word)*'_')
        self.letters = []
    
    def updateScore(self):
        lives = self.lives.get()
        score = self.score.get()
        if self.won and lives!=0:
            self.score.set(score +lives)
        elif not self.won and lives == 1 and score >=5 and not self.guess:
            self.score.set(score-5)
        elif not self.won and lives == 0 and score <5 and not self.guess:
            self.score.set(0)
            self.reset()
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
            
    def unbindButtons(self):
        for button in self.view.buttons :
            button['command']= lambda : self.reset()
        
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
            self.view.dialog.config(text="Damn, you're good!\nPress 'R' to play again!")
        else :
            self.game.lives.set(0)
            self.game.updateScore()
            self.view.dialog.config(text="That was reckless dude!\nPress 'R' to play again!"+
                                    "\nThe word was actually: "+self.game.word)
        self.unbindButtons()
        self.view.bind("r",lambda e:self.reset())
        self.view.focus_set()
        
            
    def reset(self):
        self.view.entry.delete(0, 'end')
        self.resetButtons()
        self.bindButtons()
        self.game.guess = False
        self.game.word = findRandomWord()['word']
        self.game.lives.set(11)
        self.game.hword=list(len(self.game.word)*'_')
        hw = tk.StringVar(value = ' '.join(self.game.hword))
        self.view.word['textvariable'] = hw
        self.game.letters = []
        hw = tk.StringVar()
        self.view.turtle.destroy()
        self.view.turtle = turtle_du_pauvre(self.view.container, width=500, height=500, bg = "white")
        self.view.turtle.grid(row=1 , column =0)
        self.view.dialog.config(text="Good luck again!")
        self.view.letters.set("Input letters:\n"+ ', '.join(self.game.letters))
        self.view.lives.set("Remaining attempts: "+ str(self.game.lives.get()))
        self.bindButtons()
        self.view.unbind("r")
        
    def resetButtons(self):
        for button in self.view.buttons:
            for attempt in self.game.letters:
                if attempt==button.text:
                    button.configure(relief = tk.RAISED, bg='white')

    def addLetter(self, letter):
        hw = tk.StringVar()
        if letter not in self.game.letters :
            self.game.letters.append(letter)
            for i in range(len(self.game.word)):
                if self.game.word[i].upper() == letter :
                    self.game.guess = True
                    self.game.hword[i] = letter
            self.game.won = not '_' in self.game.hword
            if self.game.guess ==False:
                self.draw()
            self.game.updateScore()
        for button in self.view.buttons:
            if button.text == letter:
                button.configure(relief = tk.SUNKEN, bg='black')
        hw.set(' '.join(self.game.hword))
        self.view.word['textvariable'] = hw
        self.view.letters.set("Input letters:\n"+ ', '.join(self.game.letters))
        self.view.lives.set("Remaining attempts: "+ str(self.game.lives.get()))
        if (11 > self.game.lives.get()> 7):
            self.view.dialog.config(text="Come on!\nYou can do it!")
        elif 7>=self.game.lives.get()>0 :
            self.view.dialog.config(text="Hmmmm...")
        elif self.game.lives.get()==0:
            self.view.dialog.config(text="Too bad, you lost!\nPress 'R' to play again!"+
                                    "\nThe word was actually: "+self.game.word)
            self.unbindButtons()
            self.view.bind("r", lambda e:self.reset())
      
    def draw(self):
        turtle = self.view.turtle
        
        def case11(pos):
            turtle.move(100,200)
            turtle.forward(100)
            
        def case10(pos):
            turtle.move(-50,0)
            turtle.left(90)
            turtle.forward(400)
        
        def case9(pos):
            turtle.left(90)
            turtle.forward(200)
            self.pos = turtle.pos
            
        def case8(pos):
            turtle.move(150,0)
            turtle.left(135)
            turtle.forward(math.sqrt(2*(50**2)))
            
        def case7(pos9):
            (x,y) = pos9
            turtle.goto(x,y)
            turtle.seth(90)
            turtle.forward(100)
        
        def case6(pos):
            turtle.circle(25)
            
        def case5(pos):
            turtle.seth(90)
            turtle.move(0,50)
            turtle.forward(120)
            
        def case4(pos):
            turtle.right(math.atan(40/80)*180/math.pi)
            turtle.forward(math.sqrt((40**2)+(80**2)))
            
        def case3(pos):
            turtle.move(80,0)
            turtle.left(2*math.atan(40/80)*180/math.pi+180)
            turtle.forward(math.sqrt((40**2)+(80**2)))
            self.pos = turtle.pos
            
        def case2(pos):
            turtle.move(0,-70)
            turtle.left(10)
            turtle.forward(math.sqrt((40**2)+(80**2)))
                
        def case1(pos3):
            (x,y)=pos3
            turtle.goto(x,y-70)
            turtle.right(2*(math.atan(40/80)*180/math.pi+10))
            turtle.forward(math.sqrt((40**2)+(80**2)))
            
        def case0():
          pass
        if(turtle.pos == (250,250)):
          self.pos=(0,0)
        
        
        switcher = {
            0 : case0,
            1 : case1,
            2 : case2,
            3 : case3,
            4 : case4,
            5 : case5,
            6 : case6,
            7 : case7,
            8 : case8,
            9 : case9,
            10 : case10,
            11 : case11}
        
        f = switcher.get(self.game.lives.get())
        f(self.pos)

              
          

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
        playground = tk.Frame(self.container, bg = 'white')
        scoreboard = tk.Frame(self.container, bg = 'white', relief = tk.GROOVE, borderwidth=2)
        workzone = tk.Frame(self.container, bg = 'white')
        dialogbox = tk.Frame(self.container, bg = 'white')
        self.dialog = self.genDialog(dialogbox)
        self.genScoreboard(scoreboard)
        self.definition = self.genPlayground(playground)
        self.word = self.genEntry(workzone)
        self.title.config(text = self.name)
        playground.grid(row = 1, column = 0, columnspan=2)
        scoreboard.grid(row = 1, column = 2)
        workzone.grid(row = 2, column = 0, columnspan =2)
        dialogbox.grid(row = 3, column=0, columnspan =2)
        
        
    def genDialog(self, master):
        label = tk.Label(master, text="Good luck!", bg = 'white', font=('Helvetica', 16))
        label.pack()
        return label
        
    def genScoreboard(self, master):
        labels = []
        score_lbl = tk.Label(master, textvariable= self.score, bg = 'white', font=('Helvetica', 16))
        labels.append(score_lbl)
        tries_lbl = tk.Label(master, textvariable = self.attempts, bg = 'white', font=('Helvetica', 16))
        labels.append(tries_lbl)
        lives_lbl = tk.Label(master, textvariable =self.lives, bg = 'white', font=('Helvetica', 16))
        labels.append(lives_lbl)
        score_lbl.pack(side = 'top')
        tries_lbl.pack(side = 'top')
        lives_lbl.pack(side = 'top')
        return labels
    
    def genPlayground(self, master):
        greet_lbl = tk.Label(master, text='Try to find the word!', bg = 'white', font=('Helvetica', 18))
        greet_lbl.pack()
        def_lbl = tk.Label(master, bg = 'white', font=('Helvetica', 16))
        def_lbl.pack()
        return def_lbl

    def genEntry(self, master):
        word = tk.Entry(master, font=('Helvetica', 16))
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
        elif not self.game.won and lives == 0 and score <5 and not self.game.guess:
            self.score.set(0)
            self.reset()
        elif self.game.guess and lives != 0:
            self.game.guess = False
        else:
            self.game.lives.set(lives-1)
            self.view.dialog.config(text="Wrong!", bg ='red')
    
    def initGame(self):
        my_wrap = textwrap.TextWrapper(width=70)
        new_text = my_wrap.fill(self.game.word['definition'])
        definition = tk.StringVar(value = "Here's its' definition:\n"+new_text)
        self.view.score.set("Current score: "+ str(self.game.score.get()))
        self.view.attempts.set("Input words:\n"+ str(self.game.attempts))
        self.view.lives.set("Remaining attempts: "+ str(self.game.lives.get()))
        self.view.definition.config(textvariable=definition, width=70, justify=tk.LEFT)
        
    def submit(self):
        word = self.view.word.get()
        if word.lower() == self.game.word['word'].lower():
            self.view.dialog.config(text="GGWP!\n Press 'R' to play again!", bg ='green')
            self.game.won = True
            self.view.bind("r", lambda e : self.reset())
            self.view.word.unbind("<Return>")
            self.view.focus_set()
        else:
            self.game.attempts.append(word)
            self.view.word.delete(0, 'end')
        self.updateScore()
        self.view.attempts.set("Input words:\n"+ str(self.game.attempts))
        self.view.lives.set("Remaining attempts: "+ str(self.game.lives.get()))
        if self.game.lives.get()==0:
            self.view.dialog.config(text="Better luck next time!\nPress 'R' to play again!\n"+
                                    "The word was "+self.game.word['word'], bg = 'white')
            self.view.bind("r", lambda e : self.reset())
            self.view.word.unbind("<Return>")
            self.view.focus_set()
        
    def reset(self):
        storeCompleteWord(self.game.word)
        self.view.word.delete(0, 'end')
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
        self.view.definition.config(textvariable=definition, width=70, justify=tk.LEFT)
        self.view.dialog.config(text="Good luck!", bg ='white')
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
        buttonframe = tk.Frame(self.container, bg = 'white')
        playground=tk.Frame(self.container, bg = 'white')
        dialogbox = tk.Frame(self.container, bg = 'white')
        self.dialog = self.genDialog(dialogbox)
        self.definition = self.genPlayground(playground)
        self.buttons =[tk.Radiobutton(buttonframe, font=('Helvetica', 16)),
                       tk.Radiobutton(buttonframe, font=('Helvetica', 16)),
                       tk.Radiobutton(buttonframe, font=('Helvetica', 16))]
        self.submit = tk.Button(playground, text="Submit", font=('Helvetica', 16))
        for button in self.buttons:
            button.pack(side="left")
        self.submit.pack()
        self.title.config(text = self.name)
        playground.grid(row = 1, column = 0, columnspan=2)
        buttonframe.grid(row = 2, column = 0, columnspan=2)
        scoreboard = tk.Frame(self.container, bg = 'white', relief=tk.GROOVE, borderwidth=2)
        self.genScoreboard(scoreboard)
        scoreboard.grid(row = 1, column = 2)
        dialogbox.grid(row = 3, column = 0 , columnspan=2)
        
    def genDialog(self, master):
        label = tk.Label(master, bg = 'white', font=('Helvetica', 16))
        label.pack()
        return label
        
    def genScoreboard(self, master):
        score_lbl = tk.Label(master, textvariable= self.score, bg = 'white', font=('Helvetica', 16))
        score_lbl.pack(side = 'top')
        return score_lbl
        
    def genPlayground(self, master):
        greet_lbl = tk.Label(master, text='Try to find the word!', bg = 'white', font=('Helvetica', 18))
        greet_lbl.pack()
        def_lbl = tk.Label(master, bg = 'white', font=('Helvetica', 16))
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



    
    def initGame(self):
        self.view.dialog.config(text = 'Good luck!');
        self.view.score.set("Current score: "+ str(self.game.score.get()))
        self.view.buttons[0].config(text=self.game.word1["word"], variable=self.view.buttonvar, value = 1)
        self.view.buttons[1].config(text=self.game.word2["word"],variable=self.view.buttonvar, value = 2)
        self.view.buttons[2].config(text=self.game.word3["word"], variable=self.view.buttonvar, value = 3)
        my_wrap = textwrap.TextWrapper(width=70)
        new_text = my_wrap.fill(self.game.word['definition'])
        definition = tk.StringVar(value = "Here's its' definition:\n"+new_text)
        self.view.score.set("Current score: "+ str(self.game.score.get()))
        self.view.definition.config(textvariable=definition, width=70, justify=tk.LEFT)
        
    def submit(self):
        ans = self.view.buttonvar.get()
        for button in self.view.buttons:
            if button['value']==ans:
                if button['text'].lower() == self.game.word['word'].lower():
                    self.view.dialog.config(text = 'Correct!', bg = 'green');
                    self.game.won = True
                else :
                    self.view.dialog.config(text = 'Wrong!', bg = 'red');
        
        self.game.updateScore()
        self.view.score.set("Current score: "+ str(self.game.score.get()))
        self.view.submit.config(text ="Play again?", command = lambda:self.reset())
        
        
    
    def reset(self):
        self.view.buttonvar.set(0)
        storeCompleteWord(self.game.word)
        self.view.dialog.config(text = 'Good luck!', bg = 'white');
        self.view.submit.config(text ="Submit", command = lambda:self.submit())
        self.view.buttons[0].config(text=self.game.word1["word"], variable=self.view.buttonvar, value = 1)
        self.view.buttons[1].config(text=self.game.word2["word"],variable=self.view.buttonvar, value = 2)
        self.view.buttons[2].config(text=self.game.word3["word"], variable=self.view.buttonvar, value = 3)
        my_wrap = textwrap.TextWrapper(width=70)
        new_text = my_wrap.fill(self.game.word['definition'])
        definition = tk.StringVar(value = "Here's its' definition:\n"+new_text)
        self.view.definition.config(textvariable=definition, width=70, justify=tk.LEFT)

# =============================================================================
# To be executed...
# =============================================================================
    
if __name__ == "__main__":
    root = tk.Tk()
    main = App(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
