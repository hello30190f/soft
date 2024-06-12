from data import data
from multiprocessing import Pool
import os
from multiProcess import _findNoneExculdeMulti

def findCandidate(data:data,id:int) -> dict:
    for AcandidateInfo in data.candidateList:
        if(AcandidateInfo["id"] == id):
            return AcandidateInfo

    return None

def _findNoneExculde(data:data,vote) -> int:
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

def process(data:data) -> str:
    winner = None

    counter = 0
    while(1):
        voteList = []

        for vote in data.voteList:
            voteList.append(_findNoneExculde(data,vote))

        countCaindidate(data,voteList)
        winner = findWinner(data)
        if(winner != None): break
        findExclude(data)

        data.resetCandidateListCount()

        if(not data.findAllCandidateExcluded()):
            return None

        print(counter)
        counter += 1

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

        args = []
        for vote in data.voteList:
            args.append([data,vote])
        voteList = p.map(_findNoneExculdeMulti,args)

        countCaindidate(data,voteList)
        winner = findWinner(data)
        if(winner != None): break
        findExclude(data)

        data.resetCandidateListCount()

        if(not data.findAllCandidateExcluded()):
            return None

        print(counter)
        counter += 1

    return winner