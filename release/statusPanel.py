import tkinter
from data import *
import threading
from tkinter import messagebox



class errCheckProgressPanel:
    def __init__(self) -> None:
        self.ProgressInit()

    def ProgressInit(self) -> None :
        self.root = tkinter.Tk()
        self.root.title("error check status")
        self.root.geometry("400x200")

        self.progressStatus = {
            "status": tkinter.StringVar(self.root,"please wait..."),
            "progress": tkinter.IntVar(self.root,0),
            "checkVoteData":tkinter.IntVar(self.root,0)
        }

        self.progressBar = ttk.Progressbar(self.root,variable=self.progressStatus["progress"],maximum=100)
        
        self.checkVoteDataBar = ttk.Progressbar(self.root,variable=self.progressStatus["checkVoteData"],maximum=100)
        self.checkVoteDataLabel = tkinter.Label(self.root,text="vote row check progress")


    def ProgressShow(self) -> None :
        status = tkinter.LabelFrame(self.root,text="status")
        status.pack(padx=10,pady=10)
        tkinter.Label(status,textvariable=self.progressStatus["status"]).pack()

        self.progressBar.pack(fill=tkinter.X)
        threading.Thread(self.root.mainloop()).start()

    def ProgressHide(self) -> None :
        self.root.destroy()

    def showCheckVoteDataInfo(self) -> None:
        self.checkVoteDataLabel.pack()
        self.checkVoteDataBar.pack(fill=tkinter.X)

    def hideCheckVoteDataInfo(self) -> None:
        self.checkVoteDataLabel.forget()
        self.checkVoteDataBar.forget()
        
    def showErrMessage(self):
        text = "err occured in " + self.progressStatus["status"].get() +" err check process\n"
        text += "Please check your data file is correct."
        messagebox.askokcancel(title="error",message=text)

    def ProgressUpdate(self,mode:str,data:dict) -> None :
        if(mode == "wordCheck"):
            self.progressStatus["status"].set(mode)
            self.progressStatus["progress"].set(data["progress"])

        # ------
        if(mode == "valueCheck"):
            if(data["status"] == "start"):
                self.progressStatus["status"].set(mode)
                self.progressStatus["progress"].set(data["progress"])
            
            if(data["status"] == "onProcess"):
                index = data["index"]
                maxVal = data["max"]
                progress = int(100 * (index / float(maxVal)))
                self.progressStatus["progress"].set(progress)

            if(data["status"] == "end"):
                self.progressStatus["progress"].set(data["progress"])
        # ------

        if(mode == "checkVoteData"):
            if(data["status"] == "start"):
                self.progressStatus["status"].set(mode)
                self.progressStatus["progress"].set(data["progress"])
                self.showCheckVoteDataInfo()

            if(data["status"] == "onProcessEntire"):
                self.progressStatus["status"].set(mode + " " + str(data["counter"]) + "/" + str(data["numberOfVote"]))
                counter = data["counter"]
                numberOfVote = data["numberOfVote"]
                progress = int(100 * ((counter - 2) / float(numberOfVote)))
                self.progressStatus["progress"].set(progress)

            if(data["status"] == "onProcessVoteRow"):
                index = data["index"]
                maxVal = data["numberOfCandidate"]
                progress = int(100 * (index / float(maxVal)))
                self.progressStatus["checkVoteData"].set(progress)

            if(data["status"] == "end"):
                self.progressStatus["status"].set(mode)
                self.progressStatus["progress"].set(data["progress"])
                self.hideCheckVoteDataInfo()


class progressPanel:

    def __init__(self,root:tkinter.Tk) -> None:
        self.root = root
        self.initProgress()

    def initProgress(self) -> None:
        self.processProgressPanel = tkinter.LabelFrame(self.root,text="process progress status")

        self.processStatus =  {
            "status": tkinter.StringVar(self.processProgressPanel,"None"),
            "progress": tkinter.IntVar(self.processProgressPanel,0),
            "findNonExclude": 10,
            "countCandidate": 20,
            "foundWinner": 30,
            "findToExclude": 40,
            "resetVote": 50,
            "checAllCandidate": 60,
            "total": 60
        }

        self.progressBar = ttk.Progressbar(self.processProgressPanel,variable=self.processStatus["progress"],maximum=self.processStatus["total"])

        #-----
        frameRow1 = tkinter.Frame(self.processProgressPanel)
        frameRow1.pack(padx=10,pady=10)

        self.status = tkinter.LabelFrame(frameRow1,text="status")
        self.status.pack()
        tkinter.Label(self.status,textvariable=self.processStatus["status"]).pack()
        #-----
        self.progressBar.pack(fill=tkinter.X)


    def updateProgress(self,mode:str) -> None:
        self.processStatus["progress"].set(self.processStatus[mode])
        self.processStatus["status"].set(mode)

    def showPanel(self) -> None:
        self.processProgressPanel.pack(fill=tkinter.X,padx=10,pady=10)


















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