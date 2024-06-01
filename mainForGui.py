from data import *
from process import process
from err import errCehck
from tkinter import filedialog
from tkinter import messagebox
import tkinter

datas  = None

def errorMessage(text:str) -> None:
    messagebox.askokcancel(title="error",message=text)

def initMainFunc():
    global datas 
    filePath = filedialog.askopenfilename()
    try:
        with open(filePath,"r") as blob:
            if(errCehck(blob)):
                errorMessage("error ocurred while read the file data. Please check your data file is correct.")
                print("error ocurred while read the file data. Please check your data file is correct.")
                exit(0)        
            datas = data(blob)
    except:
        errorMessage("error ocurred while read the file data. Please check your data file is correct.")
        print("error ocurred while read the file data. Please check your data file is correct.")
        exit(0)

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



