import copy
import wx
import wx.grid

grammar = []
itemSet = []
NFA = []
DFA = []
Vn = []
Vt = []

def closure(item):
    global itemSet
    dot = []
    dot.append(item)
    olddot = []
    while len(dot) != len(olddot):
        olddot = copy.deepcopy(dot)
        temp = []
        for i in range(len(dot)):
            for j in range(len(itemSet)):
                if dot[i].index('·') + 1 < len(dot[i]) and dot[i][dot[i].index('·') + 1] == itemSet[j][0] and \
                        itemSet[j][itemSet[j].index('>') + 1] == '·':
                    temp.append(itemSet[j])
        for k in range(len(temp)):
            if temp[k] not in dot:
                dot.append(temp[k])
    return dot

def goto(item, a):
    global itemSet
    for i in range(len(item)):
        if item[i] == '·' and i != len(item) - 1:
            if item[i + 1] == a:
                item2 = item[:i] + item[i + 1] + '·' + item[i + 2:]
                if item2 in itemSet:
                    return item2
    return -1


def findItem(item):
    global DFA
    for i in range(len(DFA)):
        if item in DFA[i]:
            return i
    return -1

n = int(input('输入文法个数'))
for i in range(n):
    temp = input()
    if i == 0:
        grammar.append('S\'->' + temp[0])
    grammar.append(temp)
    for j in range(len(temp)):
        if temp[j].isupper() and temp[j] not in Vn:    # 如果是非终结符  放入VN
            Vn.append(temp[j])
        elif temp[j].islower() and temp[j] not in Vt:    # 如果是终结符 放入vt
            Vt.append(temp[j])
Vn.sort()
Vt.sort()    # 排序

for i in range(len(grammar)):
    flag = 0
    for j in range(len(grammar[i])):
        if grammar[i][j] == '>':
            flag = 1
        if flag == 1 and grammar[i][j] != '>':
            temp = grammar[i][:j] + '·' + grammar[i][j:]
            itemSet.append(temp)
    itemSet.append(grammar[i] + '·')

print(grammar)
print(itemSet)        # 输出LR(0)项目


NFA = itemSet
NFAtable = []

for i in range(len(NFA)):
    table = []
    temp_1 = 'e'
    position = NFA[i].index('·')
    if position == len(NFA[i]) - 1:
              temp = NFA[i]

    else:
      for k in range(len(Vt)):
        if NFA[i][position + 1] == Vt[k]:
           temp = Vt[k] + str(NFA.index(goto(NFA[i], Vt[k])))
           table.append(temp)
      for m in range(len(Vn)):
         if NFA[i][position + 1] == Vn[m]:
             temp = Vn[m] + str(NFA.index(goto(NFA[i], Vn[m])))
             table.append(temp)
             for n in range(len(NFA)):
               if NFA[n][0] == Vn[m] and NFA[n][NFA[n].index('>')+1] == '·':
                 temp_1=temp_1+'/'+str(n)
             table.append(temp_1)
    NFAtable.append(table)
print(NFAtable)


VtVn = Vt + ['e'] + Vn
NFASTATETABLE = [[' ' for col in range(len(VtVn))] for row in range(len(NFA) + 1)]

print('------------------------------------------------')
print('\t\t\t\tNFA状态转移图\t\t\t\t ')

for i in range(len(VtVn)):
    NFASTATETABLE[0][i] = VtVn[i] + ' '

for i in range(len(NFAtable)):

    for j in range(len(NFAtable[i])):

        try:
            NFASTATETABLE[i + 1][VtVn.index(NFAtable[i][j][0])] = str(NFAtable[i][j][1:])
        except:
            for k in range(len(VtVn)):
                NFASTATETABLE[i + 1][k] = str(NFAtable[i][j])


print('     ')
for i in range(len(NFASTATETABLE)):
    print('    ', end=' ')
    for j in range(len(NFASTATETABLE[i])):
        print(NFASTATETABLE[i][j], end='     ')
    print('')

# 打印NFA状态转移表

'''

class GridFrame(wx.Frame):
    def __init__(self_1, parent):
        global LR0TABLE

        wx.Frame.__init__(self_1, parent)

        # Create a wxGrid object
        grid = wx.grid.Grid(self_1, -1)

        # Then we call CreateGrid to set the dimensions of the grid
        # (100 rows and 10 columns in this example)
        grid.CreateGrid(len(NFASTATETABLE) + 5, len(VtVn) + 5)

        # We can set the sizes of individual rows and columns
        # in pixels

        grid.SetCellValue(0, 0, '-')
        grid.SetCellValue(0, 1, '-')
        grid.SetCellValue(0, 2, '-')
        grid.SetCellValue(0, 3, '-')
        grid.SetCellValue(0, 4, 'NFA状态转移图')
        grid.SetCellValue(0, 5, '-')
        grid.SetCellValue(0, 6, '-')
        grid.SetCellValue(0, 7, '-')
        grid.SetCellValue(0, 8, '-')

        for i in range(len(NFASTATETABLE)):
            grid.SetCellValue(i + 2, 0, str(i))
            for j in range(len(NFASTATETABLE[i])):
                grid.SetCellValue(i + 1, j + 1, NFASTATETABLE[i][j])

        self_1.Show()


app = wx.App(0)
frame = GridFrame(None)
app.MainLoop()
                                           '''




DFA.append(closure(itemSet[0]))


oldDFA = []

while len(oldDFA) != len(DFA):
    oldDFA = copy.deepcopy(DFA)
    temp = []
    tDFA = []
    for i in range(len(DFA)):
        for j in range(len(DFA[i])):
            position = DFA[i][j].index('·')
            if position != len(DFA[i][j]) - 1:
                # print('@',goto(DFA[i][j], DFA[i][j][position+1]))
                tDFA.append(closure(goto(DFA[i][j], DFA[i][j][position + 1])))
    for k in range(len(tDFA)):
        if tDFA[k] not in DFA:
            DFA.append(tDFA[k])

print(DFA)

for i in range(len(DFA)):
    for j in range(len(DFA[i])):
        if len(DFA[i][j][-1]) == '·' and len(DFA[i]) != 1:
            print('非LR(0)文法')
            break

print(len(DFA))
DFAtable = []

for i in range(len(DFA)):
    table = []
    for j in range(len(DFA[i])):
        position = DFA[i][j].index('·')
        if position == len(DFA[i][j]) - 1:
            temp = DFA[i][j][:-1]

            table = [grammar.index(temp)] * (len(Vt) + 1)
            break
        for k in range(len(Vt)):
            if DFA[i][j][position + 1] == Vt[k]:
                temp = Vt[k] + 'S' + str(findItem(goto(DFA[i][j], Vt[k])))
                table.append(temp)
        for m in range(len(Vn)):
            if DFA[i][j][position + 1] == Vn[m]:
                temp = Vn[m] + str(findItem(goto(DFA[i][j], Vn[m])))
                table.append(temp)
    DFAtable.append(table)

# 判断是否为LR(0)文法


print(DFAtable)

VtVn = Vt + ['#'] + Vn
LR0TABLE = [[' ' for col in range(len(VtVn))] for row in range(len(DFA) + 1)]

print('------------------------------------------------')
print('状态\t\t\t\tAction\t\t\t\t GOTO')

for i in range(len(VtVn)):
    LR0TABLE[0][i] = VtVn[i] + ' '

for i in range(len(DFAtable)):
    if 0 in DFAtable[i]:

        LR0TABLE[2][VtVn.index('#')] = 'acc'     # 第二个状态为规约态
        continue
    for j in range(len(DFAtable[i])):
        try:
            LR0TABLE[i + 1][VtVn.index(DFAtable[i][j][0])] = DFAtable[i][j][1:]
        except:
            for k in range(len(Vt) + 1):
                LR0TABLE[i + 1][k] = 'r' + str(DFAtable[i][j])

print('     ')
for i in range(len(LR0TABLE)):
    print('    ', end=' ')
    for j in range(len(LR0TABLE[i])):
        print(LR0TABLE[i][j], end='     ')
    print('')

                         # 打印LR(0)表
#'''
class GridFrame(wx.Frame):
    def __init__(self, parent):
        global LR0TABLE

        wx.Frame.__init__(self, parent)

        # Create a wxGrid object
        grid = wx.grid.Grid(self, -1)

        # Then we call CreateGrid to set the dimensions of the grid
        # (100 rows and 10 columns in this example)
        grid.CreateGrid(len(LR0TABLE) + 5, len(VtVn) + 5)

        # We can set the sizes of individual rows and columns
        # in pixels

        grid.SetCellValue(0, 0, '状态')
        grid.SetCellValue(0, 1, '-')
        grid.SetCellValue(0, 2, 'ACTION')
        grid.SetCellValue(0, 3, '-')
        grid.SetCellValue(0, 4, '-')
        grid.SetCellValue(0, 5, '-')
        grid.SetCellValue(0, 6, 'GOTO')
        grid.SetCellValue(0, 7, '-')
        grid.SetCellValue(0, 8, '-')

        for i in range(len(LR0TABLE)):
            grid.SetCellValue(i + 2, 0, str(i))
            for j in range(len(LR0TABLE[i])):
                grid.SetCellValue(i + 1, j + 1, LR0TABLE[i][j])

        self.Show()


app = wx.App(0)
frame = GridFrame(None)
app.MainLoop()
#'''

string = input('输入一个句子：')
string += '#'
status = [0]
oper = ['#']
action = []

flag = 0
while flag != 1:
    symbol = string[0]
    try:
        if LR0TABLE[status[-1] + 1][VtVn.index(symbol)] != ' ' and LR0TABLE[status[-1] + 1][VtVn.index(symbol)][0] != 'r':  # 为移进项目 不为规约项目  status[-1]
            if LR0TABLE[status[-1] + 1][VtVn.index(symbol)] == 'acc':
                flag = 1
                print('接受！')
                break
            status.append(int(LR0TABLE[status[-1] + 1][VtVn.index(symbol)][-1]))
            oper.append(symbol)
            string = string[1:]
            # action.append(LR0TABLE[status[-1] + 1][VtVn.index(symbol)])
            print(status)
            print(oper)
            print('')

        elif LR0TABLE[status[-1] + 1][VtVn.index(symbol)][0] == 'r':         # 栈顶状态面临规约
            position = int(LR0TABLE[status[-1] + 1][VtVn.index(symbol)][1])
            Vnc = grammar[position][0]
            Grlen = len(grammar[position]) - grammar[position].index('>') - 1
            status = status[:-Grlen]
            oper = oper[:-Grlen]
            oper.append(Vnc)
            addx = int(LR0TABLE[status[-1] + 1][VtVn.index(Vnc)])  # 当前状态面临非终结符  下一状态入栈。
            status.append(int(addx))
            print(status)
            print(oper)
            print('')
            # action.append(str(LR0TABLE[status[-1] + 1][VtVn.index(symbol)]))
        else:
            print('错误')
            break
    except ValueError as e:
        print('错误')
