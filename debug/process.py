from data import data

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

# def findAllCandidateExcluded(data:data) -> bool:
#     for aCandidateInfo in data.candidateList:
#         if(not aCandidateInfo["exclude"]): False
#     return True

def process(data:data) -> str:

    winner = None

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


    return winner
