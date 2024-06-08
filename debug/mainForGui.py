import tkinter.scrolledtext
from data import *
from process import process
from err import errCehck
from tkinter import filedialog
from tkinter import messagebox
import tkinter
import threading

datas  = None
winnerShown = False 

def errorMessage(text:str) -> None:
    messagebox.askokcancel(title="error",message=text)

def initMainFunc():
    global datas
    filePath = filedialog.askopenfilename()
    with open(filePath,"r") as blob:
        if(errCehck(blob)):
            errorMessage("error ocurred while read the file data. Please check your data file is correct.")
            print("error ocurred while read the file data. Please check your data file is correct.")
            exit(0)
        datas = data(blob)


def getWinner(root:tkinter.Tk):
    global datas
    global winnerShown
    if(winnerShown): return
    else: winnerShown = True

    def threadFunc(datas:data,root:tkinter.Tk):
        winner = process(datas)
        if(winner != None):
            tkinter.Label(root,text="The winner is " + str(winner["id"])).pack()
        else:
            tkinter.Label(root,text="All candidates are excluded!").pack()

    processThread = threading.Thread(target=threadFunc,args=(datas,root))
    processThread.start()





if __name__ == "__main__":
    initMainFunc()

    root = tkinter.Tk()
    root.title("Vote system")

    start = tkinter.Button(root,text="start process")
    start.bind("<1>",lambda event:getWinner(root))
    start.pack(padx=10,pady=10)

    end = tkinter.Button(root,text="exit")
    end.bind("<1>",lambda event:root.quit())
    end.pack(padx=10,pady=10)

    # candidateStatePanel(root,datas)

    root.mainloop()



