import csv

class data:
    
    def __init__(self,blob) -> None:
        self.candidateList      = []
        self.voteList           = []  
          
        self.numberOfCandidate  = 0
        self.numberOfVote       = 0
        
        self.getData(blob)
            
    def getData(self,blob):
        reader = csv.reader(blob,delimiter=" ")
        
        counter = 0
        for index,row in enumerate(reader):
            if(index == 0):
                self.numberOfCandidate = int(row[2])
                continue

            if(index == 1):
                self.numberOfVote = int(row[2])
                continue

            if(index == 2):
                # do nothing
                continue

            if(row.__len__() == self.numberOfCandidate):
                new = []
                for i in range(self.numberOfCandidate):
                    new.append(int(row[i]))
                self.voteList.append(new)
                  
            else:
                # rise error
                pass
            
            if(counter == self.numberOfVote):
                break
            
            counter += 1
        
        for i in range(self.numberOfCandidate):
            new = {"id":i + 1,"count":0,"exclude":False}
            self.candidateList.append(new)
        
    def resetCandidateListCount(self):
        for aCandidate in self.candidateList:
            aCandidate["count"] = 0 
    
    def showInfo(self):
        print(self.voteList)
        print(self.candidateList)
        print(self.numberOfVote)
        print(self.numberOfCandidate)
        