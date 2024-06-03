from data import *
from process import process
from err import errCehck

datas  = None

if __name__ == "__main__":
    
    with open("./target.txt","r") as blob:
        if(errCehck(blob)):
            print("error ocurred while read the file data. Please check your data file is correct.")
            exit(0)        
        datas  = data(blob)


    winner = process(datas)
    if(winner != None):
        print("The winner is " + str(winner["id"]))
    else:
        print("All candidates are excluded!")
    exit(0)
    
    
    
    
    



