from io import TextIOWrapper
import string
# error check functions
# return:
# false -> no error found
# true  -> error found

def wordCheck(text:str) -> bool:
    if("CANDIDATES" in text and
       "VOTES" in text and
       "=" in text): return False
    return True

def valueCheck(text:str) -> bool:
    if("-" in text): return True
    for Achar in "BFGHJKLMPQRUWXYZ" + string.ascii_lowercase:
        print(Achar)
        if(Achar in text): return True

    return False


# each error check should be separeted into function
# and then executed as multiprocess
def errCehck(blob:TextIOWrapper) -> bool:
    text = blob.read()

    # check include "CANDIDATES" and "VOTES" value
    if(wordCheck(text)): return True

    # check unwanted char is included
        # check is there negative value
        # check format correctness
    if(valueCheck(text)): return True

    # check are there worng amount of data in vote date row

    blob.seek(0)
    return False
