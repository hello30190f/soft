from data import *
from process import process
from err import errCehck
from tkinter import filedialog
from tkinter import messagebox
import tkinter
import threading

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

    def threadFunc(datas:data,root:tkinter.Tk):
        winner = process(datas)
        if(winner != None):
            tkinter.Label(root,text="The winner is " + str(winner["id"])).pack()
        else:
            tkinter.Label(root,text="All candidates are excluded!").pack()

    processThread = threading.Thread(target=threadFunc,args=(datas,root))
    processThread.start()

    # winner = process(datas)
    # if(winner != None):
    #     tkinter.Label(root,text="The winner is " + str(winner["id"])).pack()
    # else:
    #     tkinter.Label(root,text="All candidates are excluded!").pack()

interval = int(1.0 / 20 * 1000)

def updatePanel(state:tkinter.LabelFrame,refList:list,datas:data):
    for ref,AcandidateInfo in zip(refList,datas.candidateList):
        # code of first line for the debug purpose
        ref["id"].set("id: " + "%4d" % (AcandidateInfo["id"]))
        ref["count"].set("count: " + "%4d" % (AcandidateInfo["count"]))
        ref["exclude"].set("exclude: " + str(AcandidateInfo["exclude"]))
    state.after(interval,lambda :updatePanel(state,refList,datas))

def candidateStatePanel(root:tkinter.Tk,datas:data) -> None:
    state = tkinter.LabelFrame(root,text="candidate state")
    state.pack()

    refList = []
    # add candidate
    for AcandidateInfo in datas.candidateList:
        ref = {}
        frame = tkinter.Frame(state)
        frame.pack()

        candidateID = tkinter.StringVar(state,"id: " + "%4d" % (AcandidateInfo["id"]))
        count       = tkinter.StringVar(state,"count: " + "%4d" % (AcandidateInfo["count"]))
        exclude     = tkinter.StringVar(state,"exclude: " + str(AcandidateInfo["exclude"]))

        ref["id"]       = (candidateID)
        ref["count"]    = (count)
        ref["exclude"]  = (exclude)

        tkinter.Label(frame,textvariable=candidateID).pack(side=tkinter.LEFT)
        tkinter.Label(frame,textvariable=count).pack(side=tkinter.LEFT)
        tkinter.Label(frame,textvariable=exclude).pack()

        refList.append(ref)
    # need to be updated
    state.after(interval,lambda :updatePanel(state,refList,datas))


if __name__ == "__main__":
    initMainFunc()

    datas.showInfo()

    root = tkinter.Tk()
    root.title("result")
    root.geometry("400x400")

    candidateStatePanel(root,datas)

    start = tkinter.Button(root,text="start process")
    start.bind("<1>",lambda event:getWinner(root))
    start.pack()

    root.mainloop()



