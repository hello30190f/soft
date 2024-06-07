from io import TextIOWrapper
import string
from multiprocessing import Pool
import os
# error check functions
# return:
# false -> no error found
# true  -> error found

def wordCheck(text:str) -> bool:
    if("CANDIDATES = " in text[:256] and
       "VOTES = " in text[:256]): return False
    return True

def valueCheck(text:str) -> bool:
    for Achar in "BFGHJKLMPQRUWXYZ-" + string.ascii_lowercase:
        if(Achar in text): return True
    return False

def checkVoteData(text:str) -> bool:
    lines = text.split("\n")

    counter = 0
    numberOfCandidate = 0
    numberOfVote = 0
    for line in lines:
        element = line.split(" ")

        if(counter == 0):
            try:
                numberOfCandidate = int(element[2])
            except:
                return True
            counter += 1
            continue

        if(counter == 1):
            try:
                numberOfVote = int(element[2])
            except:
                return True
            counter += 1
            continue

        if(counter == 2):
            counter += 1
            continue

        votes = []
        for i in range(numberOfCandidate):
            try:
                votes.append(int(element[i]))
            except:
                return True

        checked = []
        for aVote in votes:
            for check in checked:
                if(aVote == check): return True
            checked.append(aVote)

        if(counter == numberOfVote): break
        counter += 1

    return False

# each error check should be separeted into function
# and then executed as multiprocess
def errCehck(blob:TextIOWrapper) -> bool:
    text = blob.read()

    # check include "CANDIDATES" and "VOTES" value
    if(wordCheck(text)): return True

    # check unwanted char are included
        # check is there negative value
        # check format correctness
    if(valueCheck(text)): return True

    # check dupulicate data in vote data row
    # check are there alphabets in vote data row
    if(checkVoteData(text)): return True

    # check are there worng amount of data in vote date row


    blob.seek(0)
    return False
