#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 08:08:20 2020

@author: mazou
"""
import tkinter as tk
import math
import time
import requests
from random import randint
import re


def void(event):
  pass

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

class turtle_du_pauvre(tk.Canvas):
  def __init__(self, master, **args):
    super(turtle_du_pauvre,self).__init__(master, **args)
    self.angle = 0
    self.pos = (250,250)
    self.unit = 1
    self.speed = 4
    
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



def del_frame_content(frame):
  for child in frame.winfo_children():
    child.destroy()

class App:
  def __init__(self):
    self.fenetre = tk.Tk()
    fenetre = self.fenetre
    fenetre.attributes('-fullscreen', True)
    self.menubar = tk.Menu(fenetre)
    menubar = self.menubar
    self.game = tk.Frame(fenetre, borderwidth=2, relief=tk.GROOVE)
    game = self.game
    self.menubar.add_command(label = "hangman", command = self.HangMan)
    menubar.add_command(label = "guess the word", command = self.Guess_TheWord)
    menubar.add_command(label = "quit", command = self.fenetre.destroy)
    fenetre.config(menu = menubar)
    game.pack(side=tk.LEFT, padx=100, pady=30)
    fenetre.mainloop()
    
  def HangMan(self):
    del_frame_content(self.game)
    Hangman_control(self.game,self.fenetre)
  
  def Guess_TheWord(self):
    del_frame_content(self.game)
    GuessTheWorld(self.game)
    
class Hangman_control:
  def __init__(self,master,root):
    self.game = Hangman()
    self.fenetre = master
    fenetre = self.fenetre
    fenetre.config(bg = 'green')
    
    frame_pendu = tk.Frame(fenetre)
    
    frame_pendu.config(width=500,height=500)
    frame_pendu.columnconfigure(0, weight=2)
    frame_pendu.rowconfigure(0, weight=1)
    
    frame_pendu.grid(row=0,column = 0)
    
    frame_entree = tk.Frame(fenetre)
    frame_entree.grid(row = 0, column = 1)
    
    
    turtle = turtle_du_pauvre(frame_pendu, width=500, height=500, bg = "white")
    self.turtle = turtle
    turtle.pack()
    
    self.entree_controleur(frame_entree, turtle)
    
    
  def entree_controleur(self, master, turtle):
    fenetre = master
    
    mot_cherche = tk.Label(fenetre)
    self.mot_cherche = mot_cherche
    mot_cherche.grid(row = 0)
    hw = tk.StringVar()          
    hw.set(' '.join(self.game.hword))
    self.mot_cherche['textvariable'] = hw
    
    self.word = tk.Label(fenetre, textvariable = tk.StringVar(value = "     "))
    self.word.grid(row=1)
    
    word_try = tk.StringVar() 
    word_try.set("try a word")
    self.try_word = word_try
    try_word = tk.Entry(fenetre, textvariable = word_try)
    try_word.grid(row=2)
    try_word.bind("<Return>", self.try_word_controlleur)
    
    frame_buttons = tk.Frame(fenetre)
    
    frame_buttons.grid(row = 3)
    self.button_ls = []
    for i in range(6):
      for j in range(4):
        letter = chr(65+4*i+j)
        im = tk.PhotoImage(file = "alphabet/"+letter+".png")
        im = im.subsample(10,10)
        button = tk.Button(frame_buttons)
        button.text = letter
        button.im = im
        button.configure(image = button.im)
        button.configure(command = lambda b=button: self.button_f(b))
        button.grid(row = i, column= j)
        self.button_ls.append(button)
    
    letter = chr(65+4*6)
    im = tk.PhotoImage(file = "alphabet/"+letter+".png")
    im = im.subsample(10,10)
    button = tk.Button(frame_buttons)
    button.text = letter
    button.im = im
    button.configure(image = button.im)
    button.configure(command = lambda b=button: self.button_f(b))
    button.grid(row = 6, column= 1)
    frame_buttons.grid()
    self.button_ls.append(button)
    
    letter = chr(65+4*6+1)
    im = tk.PhotoImage(file = "alphabet/"+letter+".png")
    im = im.subsample(10,10)
    button = tk.Button(frame_buttons)
    button.text = letter
    button.im = im
    button.configure(image = button.im)
    button.configure(command = lambda b=button: self.button_f(b))
    button.grid(row = 6, column= 2)
    self.button_ls.append(button)
    
    self.get_key = tk.IntVar()
    get_key = tk.Checkbutton(fenetre, text="Use the keyboard", command = self.check, variable=self.get_key)
    get_key.grid(row=4)
    
  def try_word_controlleur(self, event):
    word = self.try_word.get().upper()
    print(word+ " : "+ self.game.word)
    if(self.game.word.upper() == word):
      self.game.score.set(self.game.score.get() +self.game.lives.get())
      self.game.reset()
      self.reset_buttons()
      hw = tk.StringVar()
      hw.set(' '.join(self.game.hword))
      self.mot_cherche['textvariable'] = hw
    else :
      self.addLetter("")

  def check(self):
    if(self.get_key.get()==1):
      self.fenetre.bind("<Key>", self.keyEvent)
      self.fenetre.focus_set()
    else :
      self.fenetre.bind("<Key>", void)

  def keyEvent(self,event):
    if(self.get_key.get()==1):
      letter = event.keysym.upper()
      for b in self.button_ls:
        if b.text == letter :
          b.im = tk.PhotoImage(file = "alphabet/noir.png").subsample(10,10)
          b.configure(image = b.im)
      self.addLetter(letter)
      
  def button_f(self,b):
    b.im = tk.PhotoImage(file = "alphabet/noir.png").subsample(10,10)
    b.configure(image = b.im)
    l = b.text
    self.addLetter(l)

  def addLetter(self, letter):
        hw = tk.StringVar()
        if letter not in self.game.letters :
            if letter != "":
                self.game.letters.append(letter)
            for i in range(len(self.game.word)):
                if self.game.word[i].upper() == letter :
                    self.game.guess = True
                    self.game.hword[i] = letter
            self.game.won = not '_' in self.game.hword
            
            lives = self.game.lives.get()
            score = self.game.score.get()
            word = self.game.word.upper()
            if self.game.won and lives!=0:
                self.game.score.set(score +lives)
                self.game.reset()
                self.reset_buttons()
                x = tk.StringVar()
                x.set("gg, well play")
                self.word['textvariable']=x
                self.turtle.reset()
            elif not self.game.won and lives == 1 and score >=5 and not self.game.guess:
                self.game.score.set(score-5)
                self.game.reset()
                self.reset_buttons()
                x = tk.StringVar()
                x.set("you loose : the word to find was : " + word)
                self.word['textvariable']=x
                self.turtle.reset()
            elif self.game.guess and lives != 0:
                self.game.guess = False
            elif lives == 1 and not self.game.guess:
                self.game.reset()
                self.reset_buttons()
                x = tk.StringVar()
                x.set("you loose : the word to find was : " + word)
                self.word['textvariable']=x
                self.turtle.reset()
            else:
                self.game.lives.set(lives-1)
                self.draw()
          
        hw.set(' '.join(self.game.hword))
        self.mot_cherche['textvariable'] = hw
        
  def reset_buttons(self):
    for b in self.button_ls:
                im = tk.PhotoImage(file = "alphabet/"+b.text+".png")
                im = im.subsample(10,10)
                b.im = im
                b.configure(image = b.im)
  
  def draw(self):
    
    turtle = self.turtle
    
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
    
    
      
    

class Hangman(Game):
    def __init__(self):    
        super().__init__(self)
        self.score.set(0)
        self.word = findRandomWord()['word']
        self.lives.set(12)
        self.hword=list(len(self.word)*'_')
        self.letters = []
        
    
    def reset(self):
        self.guess = False
        self.word = findRandomWord()['word']
        self.lives.set(12)
        self.hword=list(len(self.word)*'_')
        self.letters = []





class GuessTheWorld:
  def __init__(self, master):
    self.fenetre = master

App()