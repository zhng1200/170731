#coding:utf-8
iniStr = ""
history = []
for i in range(int(raw_input())):
    myinput = raw_input().strip().split(' ')
    if myinput[0] == '1':
        history.append(iniStr)
        iniStr = iniStr + myinput[1]
    elif myinput[0] == '2':
        history.append(iniStr)
        iniStr = iniStr[0:len(iniStr) - int(myinput[1])]
    elif myinput[0] == '3':
        mypos = int(myinput[1]) - 1
        print iniStr[mypos]
    else:
        iniStr = history.pop()
