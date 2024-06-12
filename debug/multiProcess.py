from data import data

def findCandidate(data:data,id:int) -> dict:
    for AcandidateInfo in data.candidateList:
        if(AcandidateInfo["id"] == id):
            return AcandidateInfo
    return None

def _findNoneExculdeMulti(args) -> int:
    datas:data = args[0]
    vote:list = args[1]
    for aCandidate in vote:
        info = findCandidate(datas,aCandidate)
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