#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 08:08:20 2020

@author: mazou
"""
import tkinter as tk
import math
import time

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
    Hangman(self.game,self.fenetre)
  
  def Guess_TheWord(self):
    del_frame_content(self.game)
    GuessTheWorld(self.game)
    
class Hangman:
  def __init__(self,master,root):
    self.fenetre = master
    fenetre = self.fenetre
    fenetre.focus_set()
    fenetre.bind("<Key>", self.keyEvent)
    fenetre.config(bg = 'green')
    
    frame_pendu = tk.Frame(fenetre)
    frame_pendu.grid(row=0,column = 0)
    
    frame_entree = tk.Frame(fenetre)
    frame_entree.grid(row = 0, column = 1)
    
    
    turtle = turtle_du_pauvre(frame_pendu, width=500, height=500, bg = 'blue')
    self.turtle = turtle
    turtle.pack()
    
    self.entree_controleur(frame_entree, turtle)
    
    
  def entree_controleur(self, master, turtle):
    fenetre = master
    
    mot_cherche = tk.Label(fenetre, text = "________")
    mot_cherche.grid(row = 0)
    
    word_try = tk.StringVar() 
    word_try.set("try a word")
    self.try_word = word_try
    try_word = tk.Entry(fenetre, textvariable = word_try)
    try_word.grid(row=2)
    try_word.bind("<Return>", self.try_word_controlleur)
    
    frame_buttons = tk.Frame(fenetre)
    for i in range(5):
      for j in range(4):
        letter = chr(65+4*i+j)
        im = tk.PhotoImage(file = "./alphabet/"+letter+".png")
        im = im.subsample(10,10)
        button = tk.Button(frame_buttons, image=im, command = lambda x=letter: self.addLetter(x))
        button.grid(row = i, column= j)
    
    letter = chr(65+4*5)
    im = tk.PhotoImage(file = "./alphabet/"+letter+".png")
    im = im.subsample(10,10)
    button = tk.Button(frame_buttons, image=im, command = lambda x=letter: self.addLetter(x))
    button.grid(row = 5, column= 1)
    frame_buttons.grid()
    
    letter = chr(65+4*5+1)
    im = tk.PhotoImage(file = "./alphabet/"+letter+".png")
    im = im.subsample(10,10)
    button = tk.Button(frame_buttons, image=im, command = lambda x=letter: self.addLetter(x))
    button.grid(row = 5, column= 2)
    
    frame_buttons.grid()
    
  def try_word_controlleur(self, event):
    word = self.try_word.get()
    pass

  def keyEvent(self,event):
    letter = event.keysis()
    self.addLetter(letter)

  def addLetter(letter):
    print(letter)
    pass
  
  



class GuessTheWorld:
  def __init__(self, master):
    self.fenetre = master

App()