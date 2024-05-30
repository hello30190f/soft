from data import data

def findCandidate(data:data,id:int):
    for AcandidateInfo in data.candidateList:    
        if(AcandidateInfo["id"] == id):
            return AcandidateInfo
    
    return None

def _findNoneExculde(data:data,vote):
    for aCandidate in vote:
        info = findCandidate(data,aCandidate)
        if(not info["exclude"]): return aCandidate
    return None

def countCaindidate(data:data,voteList):
    for aCandidateInfo in data.candidateList:
        for aCandidate in voteList:
            if(aCandidate == aCandidateInfo["id"]):
                aCandidateInfo["count"] += 1

def findWinner(data:data):
    threshold = int(data.numberOfVote / 2) + 1
    for aCandidateInfo in data.candidateList:
        if(aCandidateInfo["count"] >= threshold and not aCandidateInfo["exclude"]):
            return aCandidateInfo
    return None
    
def findExclude(data:data):
    minVote = data.candidateList[0]
    
    for aCandidateInfo in data.candidateList:
        if(minVote["count"] > aCandidateInfo["count"]):
            minVote = aCandidateInfo

    minVote["exclude"] = True



def process(data:data) -> str:
    
    winner = None
    
    while(1):
        voteList = []
        
        for vote in data.voteList:
            voteList.append(_findNoneExculde(data,vote))

        countCaindidate(data,voteList)
        winner = findWinner(data)
        if(winner != None):
            break
        findExclude(data)
        data.resetCandidateListCount()
    
    return winner
                
        