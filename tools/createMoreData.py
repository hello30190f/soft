import tkinter
import random
from tkinter import messagebox
from tkinter import filedialog
from multiprocessing import Pool
import os

def createVote(candidate:int):
    new = []
    for i in range(candidate):
        new.append(i + 1)
    
    for i in range(candidate):
        randIndexA = 0
        randIndexB = 0
        while(randIndexA == randIndexB):
            randIndexA = random.randint(0,candidate - 1)
            randIndexB = random.randint(0,candidate - 1)
            if(randIndexA != randIndexB): break

        temp = new[randIndexB]
        new[randIndexB] = new[randIndexA]
        new[randIndexA] = temp

    return new


def createData(argList):
    voteStr = argList[0]
    candidateStr = argList[1]
    filepath = argList[2]
        
    try:
        vote = int(voteStr)
        candidate = int(candidateStr)
    except:
        messagebox.askyesno(title="error",message="please enter number")
        return

    voteData = []
    for voteIndex in range(vote):
        Avote = createVote(candidate)
        voteData.append(Avote)
    
    # file path
    # create file
    # write value with sparetor as space
    with open(filepath,"w") as data:
        candidateCountStr = "CANDIDATES = " + candidateStr + "\n"
        voteCountStr = "VOTES = " + voteStr + "\n\n"
        data.write(candidateCountStr)
        data.write(voteCountStr)

        for Avote in voteData:
            dataText = ""
            for Aselection in Avote:
                dataText += str(Aselection) + " "
            dataText += "\n"
            data.write(dataText)


def createMoreData(voteStr,candidateStr,directoryPath,amountStr):
    try:
        vote = int(voteStr)
        candidate = int(candidateStr)
        amount = int(amountStr)
    except:
        messagebox.askyesno(title="error",message="please enter number")
        return

    p = Pool(os.cpu_count())

    argsList = []
    for i in range(amount):
        argList = [voteStr,candidateStr,directoryPath + "/" + str(i) + "_data.txt"]
        argsList.append(argList)
    p.map(createData,argsList)
    print(argsList)
    
    messagebox.askyesno(title="finished",message="data creation is finished.")

def refFile(entry:tkinter.Entry):
    filepath = filedialog.askdirectory()
    entry.insert("0",filepath)


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title('data creation')

    dataForm = tkinter.LabelFrame(root,text="data input")
    dataForm.pack(padx=30,fill=tkinter.X)

    tkinter.Label(dataForm,text="number of vote").pack()
    vote = tkinter.Entry(dataForm)
    vote.pack(padx=10,pady=(0,10))

    tkinter.Label(dataForm,text="number of candidate").pack()
    candidate = tkinter.Entry(dataForm)
    candidate.pack(padx=10,pady=(0,10))

    filePath = tkinter.LabelFrame(root,text="file path")
    filePath.pack()
    filePathInput = tkinter.Entry(filePath,width=40)
    filePathInput.pack(side=tkinter.LEFT)
    fileInputDialog = tkinter.Button(filePath,text="ref...")
    fileInputDialog.bind("<1>",lambda event:refFile(filePathInput))
    fileInputDialog.pack(padx=20)

    create = tkinter.Button(root,text="start creation of data")
    create.bind("<1>",lambda event:createMoreData(vote.get(),candidate.get(),filePathInput.get(),"10"))
    create.pack(padx=10,pady=10)

    root.mainloop()