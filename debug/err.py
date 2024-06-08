from io import TextIOWrapper
import string
from multiprocessing import Pool
import os
import tkinter
from tkinter import ttk
from statusPanel import errCheckProgressPanel
import threading


# error check functions
# return:
# false -> no error found
# true  -> error found

def wordCheck(text:str,panel:errCheckProgressPanel) -> bool:
    panel.ProgressUpdate("wordCheck",{"progress":0})
    
    if("CANDIDATES = " in text[:256] and
       "VOTES = " in text[:256]): return False
    
    panel.ProgressUpdate("wordCheck",{"progress":100})
    return True

def valueCheck(text:str,panel:errCheckProgressPanel) -> bool:
    panel.ProgressUpdate("valueCheck",{"status": "start","progress":0})

    maxLength = ("BFGHJKLMPQRUWXYZ-" + string.ascii_lowercase).__len__()
    for index,Achar in enumerate("BFGHJKLMPQRUWXYZ-" + string.ascii_lowercase):
        panel.ProgressUpdate("valueCheck",{"status": "onProcess","index":index,"max":maxLength})
        if(Achar in text): return True
    
    panel.ProgressUpdate("valueCheck",{"status": "end","progress":100})
    return False

def checkVoteData(text:str,panel:errCheckProgressPanel) -> bool:
    panel.ProgressUpdate("checkVoteData",{"status": "start","progress":0})
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
        for index,aVote in enumerate(votes):
            panel.ProgressUpdate("checkVoteData",{"status": "onProcessVoteRow","index":index,"numberOfCandidate":numberOfCandidate})
            for check in checked:
                if(aVote == check): return True
            checked.append(aVote)

        if(counter == numberOfVote): break
        panel.ProgressUpdate("checkVoteData",{"status": "onProcessEntire","counter":counter,"numberOfVote":numberOfVote})
        counter += 1

    panel.ProgressUpdate("checkVoteData",{"status": "end","progress":100})
    return False


def errCheckWithGui(blob:TextIOWrapper,panel:errCheckProgressPanel):
    # panel = errCheckProgressPanel()
    check = threading.Thread(target=errCehck,args=(blob,panel))
    check.start()
    panel.ProgressShow()


# each error check should be separeted into function
# and then executed as multiprocess
def errCehck(blob:TextIOWrapper,panel:errCheckProgressPanel) -> bool:
    text = blob.read()

    # check include "CANDIDATES" and "VOTES" value
    if(wordCheck(text,panel)): return True

    # check unwanted char are included
        # check is there negative value
        # check format correctness
    if(valueCheck(text,panel)): return True

    # check dupulicate data in vote data row
    # check are there alphabets in vote data row
    if(checkVoteData(text,panel)): return True

    # check are there worng amount of data in vote date row


    blob.seek(0)
    panel.root.destroy()
    return False
