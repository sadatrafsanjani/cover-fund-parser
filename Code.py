import pandas as pd
import collections

codes = []
dictionary = {}
branches = []

def processBranchInfo():
    
    bc = pd.ExcelFile('resources/files/bc.xlsx')
    sheets = []
    
    for i in range(len(bc.sheet_names)):
    
        sheets.append(bc.parse(i))
            
    for i in range(len(sheets)):
        for j in range(len(sheets[i])):
            
            key = str(sheets[i].iloc[j][1])
            
            if(len(key) == 4):
                key = '0' + key
            
            dictionary[key] = str(sheets[i].iloc[j][2])
            codes.append(key)
    
        
    codes.sort()
    
    d = collections.OrderedDict(sorted(dictionary.items(), key=lambda x:x[1]))
    
    for key, value in d.items():
        t = [key, value]
        branches.append(t)
    
    

processBranchInfo()        
        
#Branch Codes
def branchCode():
    return codes
    
#Branch Details    
def branchDetails():
    return branches

#Branch Name by Code
def getBranchByCode(code):

    if(code in dictionary):
        return dictionary.get(code)
    else:
        return None