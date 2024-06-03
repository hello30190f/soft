import string
exceptions = "CANDIDATESVOTES="

result = ""
for Achar in string.ascii_uppercase:
    
    found = False
    for checkMe in exceptions:
        if(Achar == checkMe): found = True
    
    if(not found):
        result += Achar

print(result)