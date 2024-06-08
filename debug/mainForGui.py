import tkinter.scrolledtext
from data import *
from process import process
from err import errCheckWithGui
from tkinter import filedialog
from tkinter import messagebox
import tkinter
import threading
from statusPanel import progressPanel
from statusPanel import errCheckProgressPanel

datas  = None
winnerShown = False 
panel:progressPanel = None

def errorMessage(text:str) -> None:
    messagebox.askokcancel(title="error",message=text)


def initMainFunc(root:tkinter.Tk):
    global datas
    filePath = filedialog.askopenfilename()
    
    errPanel = errCheckProgressPanel(root)
    
    with open(filePath,"r") as blob:
        if(errCheckWithGui(blob,errPanel)):
            errorMessage("error ocurred while read the file data. Please check your data file is correct.")
            print("error ocurred while read the file data. Please check your data file is correct.")
            exit(0)
        datas = data(blob)

    errPanel.ProgressHide()


def getWinner(root:tkinter.Tk):
    global datas,winnerShown,panel
    if(winnerShown): return
    else: winnerShown = True

    def threadFunc(datas:data,panel:progressPanel):
        winner = process(datas,panel)
        if(winner != None):
            tkinter.Label(root,text="The winner is " + str(winner["id"])).pack()
        else:
            tkinter.Label(root,text="All candidates are excluded!").pack()

    processThread = threading.Thread(target=threadFunc,args=(datas,panel))
    processThread.start()



if __name__ == "__main__":
    root = tkinter.Tk()
    initMainFunc(root)

    root.title("Vote system")

    commandList = tkinter.LabelFrame(root,text="command button")
    commandList.pack(padx=10,pady=10)

    start = tkinter.Button(commandList,text="start process")
    start.bind("<1>",lambda event:getWinner(root))
    start.pack(padx=10,pady=10,side=tkinter.LEFT)

    end = tkinter.Button(commandList,text="exit")
    end.bind("<1>",lambda event:root.quit())
    end.pack(padx=10,pady=10)

    panel = progressPanel(root)
    panel.showPanel()

    root.mainloop()



