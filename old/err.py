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
    if("-" in text): return True
    for Achar in "BFGHJKLMPQRUWXYZ" + string.ascii_lowercase:
        if(Achar in text): return True
    return False

def valueCheckMulti(text:str) -> bool:
    chars =  [Achar for Achar in "BFGHJKLMPQRUWXYZ-" + string.ascii_lowercase]
    texts = [text for i in range(chars.__len__())]
    args = zip(chars,texts)
    p = Pool(os.cpu_count())
    def check(args):
        char = args[0]
        text = args[1]
        if char in text: return True
        else: return False
    res = p.map(check,args)
    
    for checkBool in res:
        if(checkBool): return True

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

    # check are there worng amount of data in vote date row

    blob.seek(0)
    return False
