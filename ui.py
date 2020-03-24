import tkinter as tk                
from tkinter import font  as tkfont 
from main import *





class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PlayPage, HangmanPage, MatchingPage, CrosswordsPage, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        frame.update()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        lbl_welcome = tk.Label(self, text="Hello, TNCY!", font=controller.title_font)
        lbl_welcome.pack(side="top", fill="x", pady=10)
        lbl_about = tk.Label(self, text="More about Slanged")
        btn_play = tk.Button(self, text="Play",
                            command=lambda: controller.show_frame("PlayPage"))
        btn_quit = tk.Button(self, text="Quit",
                            command= App.destroy)
        btn_play.pack()
        btn_quit.pack()
        lbl_about.pack()


class PlayPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        lbl_quest = tk.Label(self, text="What would you\nlike to try?", font=controller.title_font)
        lbl_quest.pack(side="top", fill="x", pady=10)
        btn_hangman = tk.Button(self, text="Hangman",
                           command=lambda: controller.show_frame("HangmanPage"))
        btn_mg = tk.Button(self, text="Matching Words",
                           command=lambda: controller.show_frame("MatchingPage"))
        btn_cw = tk.Button(self, text="Crosswords",
                           command=lambda: controller.show_frame("CrosswordsPage"))
        btn_hangman.pack()
        btn_mg.pack()
        btn_cw.pack()
        

class HangmanPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        lbl_title = tk.Label(self, text="Hangman", font=controller.title_font)
        lbl_title.pack(side="top", fill="x", pady=10)
        btn_quit = tk.Button(self, text="Quit",
                            command=App.quit)
        btn_quit.pack()
        hangman()


class MatchingPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        lbl_title = tk.Label(self, text="Matching Words", font=controller.title_font)
        lbl_title.pack(side="top", fill="x", pady=10)
        btn_quit = tk.Button(self, text="Quit",
                            command=App.quit)
        btn_quit.pack()

class CrosswordsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        lbl_title = tk.Label(self, text="Crosswords", font=controller.title_font)
        lbl_title.pack(side="top", fill="x", pady=10)
        btn_quit = tk.Button(self, text="Quit",
                            command=App.quit)
        btn_quit.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = App()
    app.title("Slanged!")
    app.mainloop()