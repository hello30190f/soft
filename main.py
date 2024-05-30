from data import *
from process import process

datas  = None

if __name__ == "__main__":
    
    with open("./target.txt","r") as blob:
        datas  = data(blob)
        
    # datas.showInfo()
    winner = process(datas)
    print("The winner is " + str(winner["id"]))
    
    
    
    
    



