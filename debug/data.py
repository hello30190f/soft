import csv
from io import TextIOWrapper
import tkinter
import threading
from tkinter import ttk

class data:

    def __init__(self,blob:TextIOWrapper) -> None:
        self.candidateList      = []
        self.voteList           = []

        self.numberOfCandidate  = 0
        self.numberOfVote       = 0

        self.initProgressPanel()

        threading.Thread(target=self.getData,args=(blob,)).start()
        self.showProgress()

    def initProgressPanel(self):
        self.progressPanel = tkinter.Tk()
        self.progressPanel.title("reading data...")

        self.progressStatus = {
            "readVote"          : tkinter.StringVar(self.progressPanel,"0"),
            "currentData"       : tkinter.StringVar(self.progressPanel,""),
            "numberOfCandidate" : tkinter.StringVar(self.progressPanel,"wait"),
            "numberOfVote"      : tkinter.StringVar(self.progressPanel,"wait"),
            "status"            : tkinter.StringVar(self.progressPanel,"None")
        }

        self.progressBarState = {
            "initStep"              :10,
            "countVoteStepLength"   :50,
            "initCandidateLength"   :40,
            "prevStep"              :tkinter.IntVar(self.progressPanel,0),
            "step"                  :tkinter.IntVar(self.progressPanel,0)
        }
        self.progressBar = ttk.Progressbar(self.progressPanel,maximum=100,variable=self.progressBarState["step"])

    def showProgress(self) -> None:
        tkinter.Label(self.progressPanel,textvariable=self.progressStatus["status"]).pack()
        frame = tkinter.Frame(self.progressPanel)
        frame.pack()

        #------
        infoPanel = tkinter.LabelFrame(frame,text="info")
        infoPanel.pack(padx=50,pady=10,side=tkinter.RIGHT)

        numberOfCandidate = tkinter.LabelFrame(infoPanel,text="number of candidate")
        numberOfCandidate.pack(padx=10,pady=10)
        tkinter.Label(numberOfCandidate,textvariable=self.progressStatus["numberOfCandidate"]).pack()

        numberOfVote = tkinter.LabelFrame(infoPanel,text="number of vote")
        numberOfVote.pack(padx=10,pady=10)
        tkinter.Label(numberOfVote,textvariable=self.progressStatus["numberOfVote"]).pack()
        #------


        #------
        progress = tkinter.LabelFrame(frame,text="Progress")
        progress.pack(padx=50,pady=10)

        readVote = tkinter.LabelFrame(progress,text="number of read vote")
        readVote.pack(padx=10,pady=10)
        tkinter.Label(readVote,textvariable=self.progressStatus["readVote"]).pack()

        currentData = tkinter.LabelFrame(progress,text="current read data")
        currentData.pack(padx=10,pady=10)
        tkinter.Label(currentData,textvariable=self.progressStatus["currentData"]).pack()
        #------

        self.progressBar.pack(fill=tkinter.X)
        self.progressPanel.mainloop()


    def updateProgress(self,mode:str) -> None:

        self.updateProgressBar(mode)

        if(mode == "countVote"):
            self.progressStatus["status"].set(mode)
            self.progressStatus["readVote"].set(str(self.counter))
            currentData = ""
            for index,vote in enumerate(self.voteList[-1]):
                if(index == 6):
                    currentData += "..."
                    break
                currentData += str(vote) + ","
            self.progressStatus["currentData"].set(currentData)
            return

        if(mode == "initCandidate"):
            self.progressStatus["status"].set(mode)
            return

        if(mode == "init"):
            self.progressStatus["status"].set(mode)
            self.progressStatus["numberOfVote"].set(str(self.numberOfVote))
            self.progressStatus["numberOfCandidate"].set(str(self.numberOfCandidate))
            return


    def updateProgressBar(self,mode):
        if(mode == "countVote"):
            progress = self.progressBarState["initStep"] + self.progressBarState["countVoteStepLength"] * float(self.counter) / self.numberOfVote
            self.progressBarState["step"].set(int(progress))
            self.progressBarState["prevStep"].set(self.progressBarState["step"].get())
            return

        if(mode == "initCandidate"):
            progress = self.progressBarState["initStep"] + self.progressBarState["prevStep"].get() + (self.progressBarState["countVoteStepLength"] * float(self.candidateIndex) / self.numberOfCandidate)
            self.progressBarState["step"].set(int(progress))
            return

        if(mode == "init"):
            self.progressBarState["step"].set(int(self.progressBarState["initStep"]))
            return


    def getData(self,blob:TextIOWrapper) -> None:
        reader = csv.reader(blob,delimiter=" ")

        self.counter = 0
        for index,row in enumerate(reader):
            if(index == 0):
                self.numberOfCandidate = int(row[2])
                self.updateProgress("init")
                continue

            if(index == 1):
                self.numberOfVote = int(row[2])
                self.updateProgress("init")
                continue

            if(index == 2):
                # do nothing
                continue

            new = []
            for i in range(self.numberOfCandidate):
                new.append(int(row[i]))
            self.voteList.append(new)

            if(self.counter == self.numberOfVote):
                break

            self.counter += 1
            self.updateProgress("countVote")


        self.candidateIndex = 0
        self.updateProgress("initCandidate")
        for i in range(self.numberOfCandidate):
            self.candidateIndex = i
            self.updateProgress("initCandidate")
            new = {"id":i + 1,"count":0,"exclude":False}
            self.candidateList.append(new)

        self.progressPanel.destroy()

    def resetCandidateListCount(self) -> None:
        for aCandidate in self.candidateList:
            aCandidate["count"] = 0

    def findAllCandidateExcluded(self) -> bool:
        for aCandidateInfo in self.candidateList:
            if(not aCandidateInfo["exclude"]): False
        return True

    def showInfo(self) -> None:
        print(self.voteList)
        print(self.candidateList)
        print(self.numberOfVote)
        print(self.numberOfCandidate)
