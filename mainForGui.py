from data import *
from process import process
from err import errCehck
from tkinter import filedialog
import tkinter

datas  = None

def initMainFunc():
    global datas 
    filePath = filedialog.askopenfilename()
    with open(filePath,"r") as blob:
        if(errCehck(blob)):
            print("error ocurred while read the file data. Please check your data file is correct.")
            exit(0)        
        datas = data(blob)

def getWinner(root:tkinter.Tk):
    global datas
    winner = process(datas)
    if(winner != None):
        tkinter.Label(root,text="The winner is " + str(winner["id"])).pack()
    else:
        tkinter.Label(root,text="All candidates are excluded!").pack()


if __name__ == "__main__":
    initMainFunc()

    root = tkinter.Tk()
    root.title("result")

    start = tkinter.Button(root,text="start process")
    start.bind("<1>",lambda event:getWinner(root))
    start.pack()

    root.mainloop()
    
    
    
    
    



