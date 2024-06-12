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


def initMainFunc():
    global datas
    filePath = filedialog.askopenfilename()

    errPanel = errCheckProgressPanel()
    errFlag = False
    try:
        with open(filePath,"r") as blob:
            if(errCheckWithGui(blob,errPanel)):
                errFlag = True
            datas = data(blob)
    except:
        errFlag = True

    if(errFlag):
        errorMessage("error ocurred while read the file data. Please check your data file is correct.")
        print("error ocurred while read the file data. Please check your data file is correct.")
        exit(0)



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
    initMainFunc()
    root = tkinter.Tk()

    root.title("Vote system")
    root.geometry("400x250")

    commandList = tkinter.LabelFrame(root,text="command button")
    commandList.pack(padx=10,pady=10)

    start = tkinter.Button(commandList,text="start process")
    start.bind("<1>",lambda event:getWinner(root))
    start.pack(padx=10,pady=10,side=tkinter.LEFT)

    end = tkinter.Button(commandList,text="exit")
    end.bind("<1>",lambda event:root.destroy())
    end.pack(padx=10,pady=10)

    panel = progressPanel(root)
    panel.showPanel()

    root.mainloop()



