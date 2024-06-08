from data import data
from multiprocessing import Pool
import os
from multiProcess import _findNoneExculdeMulti
import tkinter
from tkinter import ttk
import threading
from statusPanel import progressPanel

def findCandidate(data:data,id:int) -> dict:
    for AcandidateInfo in data.candidateList:
        if(AcandidateInfo["id"] == id):
            return AcandidateInfo

    return None

def findNoneExculde(data:data,vote) -> int:
    for aCandidate in vote:
        info = findCandidate(data,aCandidate)
        if(not info["exclude"]): return aCandidate
    return None

def countCaindidate(data:data,voteList) -> None:
    for aCandidateInfo in data.candidateList:
        for aCandidate in voteList:
            if(aCandidate == aCandidateInfo["id"]):
                aCandidateInfo["count"] += 1

def findWinner(data:data) -> dict:
    threshold = int(data.numberOfVote / 2) + 1
    for aCandidateInfo in data.candidateList:
        if(aCandidateInfo["count"] >= threshold and not aCandidateInfo["exclude"]):
            return aCandidateInfo
    return None

def findExclude(data:data) -> None:
    minVote = data.candidateList[0]

    counter = 1
    while(minVote["exclude"]):
        minVote = data.candidateList[counter]
        counter += 1

    for aCandidateInfo in data.candidateList[counter:]:
        if(minVote["count"] > aCandidateInfo["count"] and not aCandidateInfo["exclude"]):
            minVote = aCandidateInfo

    minVote["exclude"] = True



def process(data:data,statusPanel:progressPanel) -> str:

    winner = None

    counter = 0
    while(1):
        voteList = []

        for vote in data.voteList:
            voteList.append(findNoneExculde(data,vote))
        print("find non excluded candidate")
        statusPanel.updateProgress("findNonExclude")

        # slow
        countCaindidate(data,voteList)
        print("count candidate")
        statusPanel.updateProgress("countCandidate")

        winner = findWinner(data)
        print("found winner")
        statusPanel.updateProgress("foundWinner")

        if(winner != None): break
        findExclude(data)
        print("find to exclude")
        statusPanel.updateProgress("findToExclude")

        data.resetCandidateListCount()
        print("reset vote counter of candidates")
        statusPanel.updateProgress("resetVote")

        if(not data.findAllCandidateExcluded()):
            return None
        print("check all candidates are excluded")
        statusPanel.updateProgress("checAllCandidate")

        print("progress: " + str(counter) + "\n\n")
        counter += 1

    statusPanel.processProgressPanel.destroy()
    return winner



def multiProcess(data:data) -> str:
    winner = None

    # subporcess creater
    # not always the number of cpu is the appropriate amount of subprocess
    core = os.cpu_count()
    if(data.numberOfVote >= core):
        p = Pool(os.cpu_count())
    else:
        p = Pool(data.numberOfVote)

    counter = 0
    while(1):

        # is multiprocess need in _findNoneExculde
        args = []
        for vote in data.voteList:
            args.append([data,vote])
        voteList = p.map(_findNoneExculdeMulti,args)
        print("find non excluded candidate")

        # slow
        countCaindidate(data,voteList)
        print("count candidate")

        winner = findWinner(data)
        print("found winner")

        if(winner != None): break
        findExclude(data)
        print("find to exclude")

        data.resetCandidateListCount()
        print("reset vote counter of candidates")

        if(not data.findAllCandidateExcluded()):
            return None
        print("check all candidates are excluded")

        print("progress: " + str(counter) + "\n\n")
        counter += 1

    return winner