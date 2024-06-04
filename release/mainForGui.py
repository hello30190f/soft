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


def updatePanel(state:tkinter.LabelFrame,refList:list,datas:data) -> None:
    interval = int(1.0 / 5 * 1000)
    for ref,AcandidateInfo in zip(refList,datas.candidateList):
        # code of first line for the debug purpose
        ref["id"].set("id: " + "%4d" % (AcandidateInfo["id"]))
        ref["count"].set("count: " + "%4d" % (AcandidateInfo["count"]))
        ref["exclude"].set("exclude: " + str(AcandidateInfo["exclude"]))
    state.after(interval,lambda :updatePanel(state,refList,datas))


def candidateStatePanel(root:tkinter.Tk,datas:data) -> None:
    mainFrame = tkinter.Frame(root)
    mainFrame.pack()
    
    scrollContainer = tkinter.Canvas(mainFrame)
    scrollContainer.grid(padx=20,pady=20,row=0,column=0)

    scroll = tkinter.Scrollbar(mainFrame,command=scrollContainer.yview)
    scroll.grid(row=0,column=1,sticky=tkinter.NS)
    scrollContainer.configure(yscrollcommand=scroll.set)

    state = tkinter.LabelFrame(scrollContainer,text="candidate state")
    state.pack(padx=20,pady=20) 

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

    state.update_idletasks()
    root.update_idletasks()
    scrollContainer.create_window(0,0,window=state,anchor="nw")
    scrollContainer.config(scrollregion=(0,0,state.winfo_reqwidth(),state.winfo_reqheight()))
    if(state.winfo_reqheight() > 200):
        scrollContainer.configure(width=state.winfo_reqwidth(),height=200)
    else:
        scrollContainer.configure(width=state.winfo_reqwidth(),height=state.winfo_reqheight())

    updater = threading.Thread(target=updatePanel,args=(state,refList,datas))
    updater.start()
    # need to be updated
    # state.after(interval,lambda :updatePanel(state,refList,datas))


if __name__ == "__main__":
    initMainFunc()

    datas.showInfo()

    root = tkinter.Tk()
    root.title("result")

    start = tkinter.Button(root,text="start process")
    start.bind("<1>",lambda event:getWinner(root))
    start.pack(padx=10,pady=10)

    candidateStatePanel(root,datas)

    root.mainloop()


