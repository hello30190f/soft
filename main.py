from data import *
from process import process
from err import errCehck

datas  = None

if __name__ == "__main__":
    
    with open("./target.txt","r") as blob:
        if(errCehck(blob)):
            print("error ocurred while reading file data. Please check your data file is correct.")
            exit(0)        
        datas  = data(blob)


    winner = process(datas)
    print("The winner is " + str(winner["id"]))
    exit(0)
    
    
    
    
    



