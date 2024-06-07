import tkinter
from data import *
import threading



























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