from tkinter import *
from functools import partial

state = 0

def StartPracticeWindow(mydb):
    global state
    state = 0
    c = 0
    window = Tk()
    window.title(c)
    window.geometry('1050x200')
    state = 0


    def nextQuestion(c, mydb):
        global state
        if c == 100: window.destroy()
        c += 1
        window.title(c)

        words = (mydb.result_set[c - 1][1].replace('÷', '').replace('¤', '').replace(',', '')).split(' ')  # get the original sentence without commas

        lbl = Message(window, text=words, font=("Arial", 12), width=900)
        lbl.grid(column=0, row=0, pady=10, padx=10)

        solution = Button(window, text="Show solution", font=("Courier new", 10))
        solution.configure(command=partial(showSolution, lbl, solution, c, mydb))
        solution.grid(column=0, row=1, padx=10, pady=10)

        star = Button(window, text="⭐", font=("Courier new", 10))
        star.configure(command=partial(mydb.star, mydb.result_set[c-1][0]))
        star.grid(column=0, row=2, padx=10, pady=10)


    def showSolution(lbl, solution, c, mydb):
        global state
        if state == 0:
            lbl.configure(text=(mydb.result_set[c-1][1].replace('÷', '').replace('¤', ',')))
            solution.configure(text="Next sentence")
            state = 1
        else:
            state = 0
            lbl.destroy()
            solution.destroy()
            nextQuestion(c, mydb)


    nextQuestion(c, mydb)


    window.mainloop()

def StartMainWindow(mydb):

    window = Tk()
    window.title("Start")
    window.geometry('500x200')

    def practice(): 
        mydb.action = 1
        mydb.fetch100()
        window.destroy()
       # StartPractice(mydb)

    def viewStarred():
        mydb.action = 2
        window.destroy()
    
    practiceButton = Button(window, text="Practice 100 examples", command=practice, font=("Courier new", 15))
    practiceButton.grid(column=0, row=1, pady=10, padx=10)
    viewStarredButton = Button(window, text="View starred ⭐", command=viewStarred, font=("Courier new", 10))
    viewStarredButton.grid(column=0, row=2, padx=10, pady=10)

    window.mainloop()

