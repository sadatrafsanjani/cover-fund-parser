from xlrd import open_workbook
import pandas as pd
import re
import Code

F20s = []
F32As = []
F32Amounts = []
F50Ks = []
F52As = []
F53As = []
F59s = []
F70s = []
Narratives = []
accounts = []
names = []
pounds = []
amounts = []
banks = []
modes = []
bdts = []
remarks = []
exchanges = []
references = []


column = ['Ref No.', 'Ref Date', 'Rem_name', 'Ben_name', 'Ben_bank', 'Ben_br_name', 
          'Ben_br_code', 'Pay_mode', 'Ben_ac_num', 'FC_amount', 'Exch_rate', 'FC_cur', 
          'Remit_amt', 'Pay_cur', 'Valu_dat', 'RMb_bank', 'Remarks']

data1 = []
data2 = []
data3 = []


def getF61(value, start, end):
    
    value = value[start : end]
    start = value.find('Reference for the Account Owner:')
    value = value[start : ]
    value = value[len('Reference for the Account Owner:') : ].strip()
    
    if( (len(value) == 10) and (value.find('3') == 0) ):
                
        return value
                

def getRefNo(filename):
    
    wb = open_workbook(filename)
    
    for s in wb.sheets():
        for row in range(1, s.nrows):
            col_names = s.row(0)
            
            for name, col in zip(col_names, range(s.ncols)):
                
                value  = (s.cell(row,col).value)
                
                try : 
                    value = str(int(value))
                except : 
                    pass
                
                if(value != ''):
                    if('F61:' in value):
                        
                        starts = [m.start() for m in re.finditer('F61:', value)]
                        ends = [m.start() for m in re.finditer('Reference of the Account Servicing Institution:', value)]
                        
                        for i, j in zip(starts, ends):
                            t = getF61(value, i, j)
                            references.append(t)

                        
def getDigitPosition(string):
    
    number = re.search("\d", string)
    
    if number:
        return number.start()
    else:
        return None
    

def getF20(value):
    
    start = value.find('F20')
    end = value.find('F23B')
    value = value[start : end]
    value = value[ value.find('Sender\'s Reference') : end ]
    value = value[18 : ].strip()
    
    return value


def getF32A(value):
    
    start = value.find('F32A')
    end = value.find('Currency:')
    value = value[start : end]
    value = value[-22 : -1].strip()
    value = value.replace(' ', '/')
    
    return value


def getF32Amounts(value):
    
    start = value.find('F32A')
    end = value.find('F33B')
    value = value[start : end]
    
    start = value.find('Amount:')
    end = value.find('#')
    value = value[start : end]
    amount = value[7 : ].strip()
    amount = amount.replace(",", ".")
    
    if(amount == ''):
        amount = 0.0
        
    value = ['POUND', float(amount)]
             
    return value

def getF50K(value):
    
    start = value.find('F50K')
    end = value.find('F52A')
    value = value[start : end]
    start = value.find('Name and Address:')
    value = value[start : ]
    value = value[len('Name and Address:') : ].strip()
    value = value[ : value.find('\n') ]
    
    return value


def getF52A(value):
    
    start = value.find('F52A')
    end = value.find('F53A')
    value = value[start : end]
    start = value.find('Identifier Code:')
    value = value[start : ]
    value = value[len('Identifier Code:') : ].strip()
    
    start = value.find('CITIIE2XXXX')
    value = value[start : ]
    value = value[len('CITIIE2XXXX') : ].strip()
    value = value[ : value.find('\n')].strip()
    
    return value

def getF53A(value):
    
    start = value.find('F53A')
    end = value.find('F59')
    value = value[start : end]
    start = value.find('Identifier Code:')
    value = value[start : ]
    value = value[len('Identifier Code:') : ].strip()
    
    start = value.find('SCBLGB2LXXX')
    value = value[start : ]
    value = value[len('SCBLGB2LXXX') : ].strip()
    value = value[ : value.find('\n')]
    
    return value


def getF59(value):
    
    start = value.find('F59')
    end = value.find('F70')
    value = value[start : end]
    
    start = value.find('Account:')
    value = value[start : ]
    account = value[len('Account:') : value.find('Name and Address:')].strip()
    account = account[1 : ]
    
    start = value.find('Name and Address:')
    value = value[start : ]
    name = value[len('Name and Address:') : ].strip()
    
    if(name.find('\n') > 0):
        name = name[ : name.find('\n')]
    
    value = [account, name]
    
    return value

def getF70(value):
    
    start = value.find('F70')
    end = value.find('F71A')
    value = value[start : end]
    start = value.find('Remittance Information')
    end = value.find('/ROC')
    value = value[start : end]
    value = value[len('Remittance Information') : ].strip()
    
    if(getDigitPosition(value) is not None):
    
        first = getDigitPosition(value)
        value = value[first : ]
    
    v = ''
    
    for i in range(len(value)):
        if(value[i].isdigit()):
            v += value[i]
           
    value = v.strip()
    
    return value


def getNarrative(value):
    
    start = value.find('Lines2to6')
    value = value[start :]
    start = value.find('//')
    end = value.find('\n')
    value = value[start : ]
    value = value[2 : ]
    
    if(value.find('\n') > 0):
        
        end = value.find('\n')
        value = value[ : end]

    return value


def matchBranch():
    
    codes = Code.branchCode()    

    for i in range(len(F20s)):
        
        branch = F70s[i]

        if(F20s[i] != ''):
            
            if(branch[ : 5] == '00001'):
                
                branch = branch[ 5 : ]
                F70s[i] = branch

                if(F20s[i] in references):
                    
                    if(branch in codes):
                    
                        if(Narratives[i] == ''):
                            Narratives[i] = Code.getBranchByCode(branch)
                        
                        t = [F20s[i], F32As[i], F50Ks[i], names[i], banks[i], Narratives[i], 
                         branch, modes[i], accounts[i], amounts[i], exchanges[i],
                         pounds[i], amounts[i] * exchanges[i], bdts[i], F32As[i], F53As[i], remarks[i]]
                        data2.append(t)
                        
                    else:
                        t = [F20s[i], F32As[i], F50Ks[i], names[i], banks[i], Narratives[i], 
                         F70s[i], modes[i], accounts[i], amounts[i], exchanges[i],
                         pounds[i], amounts[i] * exchanges[i], bdts[i], F32As[i], F53As[i], remarks[i]]
                        data1.append(t)
                else:
                    t = [F20s[i], F32As[i], F50Ks[i], names[i], banks[i], Narratives[i], 
                         branch, modes[i], accounts[i], amounts[i], exchanges[i],
                         pounds[i], amounts[i] * exchanges[i], bdts[i], F32As[i], F53As[i], remarks[i]]
                    data3.append(t)
                    
            else:
                F70s[i] = '00000'
                t = [F20s[i], F32As[i], F50Ks[i], names[i], banks[i], Narratives[i], 
                     F70s[i], modes[i], accounts[i], amounts[i], exchanges[i],
                     pounds[i], amounts[i] * exchanges[i], bdts[i], F32As[i], F53As[i], remarks[i]]
                data1.append(t)
                
                        
def setFileName(rate, step1, cover):
    
    getRefNo(cover)
    
    wb = open_workbook(step1)
    
    for s in wb.sheets():
    
        for row in range(1, s.nrows):
            
            col_names = s.row(0)
            
            for name, col in zip(col_names, range(s.ncols)):
            
                value  = (s.cell(row,col).value)
                
                try : 
                    value = str(int(value))
                except : 
                    pass
                
                if(value != ''):
                    
                    if('F20:' in value):
                    
                        t = getF20(value)
                        F20s.append(t)
                        
                        t = getF32A(value)
                        F32As.append(t)
                        
                        t = getF32Amounts(value)
                        pounds.append(t[0])
                        amounts.append(t[1])
                        F32Amounts.append(t)
                        
                        t = getF50K(value)
                        F50Ks.append(t)
                        
                        t = getF52A(value)
                        F52As.append(t)
                        
                        t = getF53A(value)
                        F53As.append(t)
                        
                        t = getF59(value)
                        accounts.append(t[0])
                        names.append(t[1])
                        F59s.append(t)
                        
                        t = getF70(value)
                        F70s.append(t)
                        
                        t = getNarrative(value)
                        Narratives.append(t)
                        
                        banks.append('SONALI BANK LTD')
                        modes.append('TRANSFER')
                        bdts.append('BDT')
                        remarks.append('BRITISH PENSION')
                        exchanges.append(rate)
    
    

def getData():

    df1 = pd.DataFrame(data1, columns=column)
    df2 = pd.DataFrame(data2, columns=column)
    df3 = pd.DataFrame(data3, columns=column)

    return df1, df2, df3


def printer():
    
    file = open('backup.txt', 'w')
    
    for i in range(len(F20s)):
        
        code = F70s[i]
        
        if(code[ : 5 ] == '00001'):
            code = code[ 5 : ]
        
        t = ''
        t += F20s[i] + '|'
        t += F32As[i] + '|'
        t += F50Ks[i] + '|'
        t += names[i] + '|'
        t += banks[i] + '|'
        t += Narratives[i] + '|'
        t += str(code) + '|'
        t += modes[i] + '|'
        t += accounts[i] + '|'
        t += str(amounts[i]) + '|'
        t += str(exchanges[i]) + '|'
        t += pounds[i] + '|'
        t += str(amounts[i] * exchanges[i]) + '|'
        t += bdts[i] + '|'
        t += F32As[i] +  ' | '
        t += F53As[i] + '|'
        t += remarks[i] + '\n'
    
        file.write(str(t))
        
    file.close()
