import tkinter as tk
import math

global screen, win, digitList, trigList, trigButtons, operButtons, operList, actionButtons, actionList, strLength, string, numbers, operators, counter, n
ALIGNMENT, FONT_STYLE, FONT_SIZE, FONT_TYPE, WIDTHxHEIGHT = tk.RIGHT, 'Times New Roman', 25, 'bold', '500x500'

numbers, operators = [[]], [[]]
digitList = []
trigButtons, trigList = ['sin', 'cos', 'tan'], []
operButtons, operList = ['(', ')', '^', '%', '/', 'x', '+', '-'], []
actionButtons, actionList = ['C','.', '='], []
opButtons = ['^', '%', '/', '*', '-', '+']
counter, n, historyIndex =0, 0, 0
historyList=[]


def initialise():

    global win
    win = tk.Tk()

    for i in range(4):
        win.columnconfigure(i, weight=1, minsize= 80)
    for i in range(7):
        win.rowconfigure(i, weight=1, minsize= 60)

    win.bind('<Return>', startEngine)


def editScreen(text):

    screen.insert(tk.END, text)

def makeScreen():

    global screen
    screen = tk.Entry(win, font=(FONT_STYLE, FONT_SIZE, FONT_TYPE), justify= ALIGNMENT)
    #screen.pack()

def createButton(text, list):

    button = tk.Button(win, text=text, font=(FONT_STYLE, FONT_SIZE, FONT_TYPE), command=lambda : editScreen(text))
    list.append(button)


def makeButtons():

    for index in range(10):
        createButton(index, digitList)

    for trig in trigButtons :
        createButton(trig, trigList)

    for oper in operButtons:
        createButton(oper, operList)

    for act in actionButtons:
        createButton(act, actionList)




def addWidgets():

    index=0
    screen.grid(row=0, column=0, columnspan=4, sticky='nwes')

    for button in trigList:
        button.grid(row=1, column=index, sticky='nwes')
        index+=1

    for index in range(0,3):
         if index<=1:
            operList[index].grid(row=2, column=index, sticky='nwes')
         else:
            actionList[index-2].grid(row=2, column=index, sticky='nwes')

    index=9
    for i in range(3,6):
        for j in range(0,3):
            digitList[index].grid(row=i, column=j, sticky='nwes')
            index-=1

    for i in range(2,8):
        operList[i].grid(row=i-1, column=3, sticky='nwes')

    for i in range(1,3):
        actionList[i].grid(row=6, column=i, sticky='nwes')

    digitList[0].grid(row=6, column=0, sticky='nwes')


def getString():

    global strLength, string

    string = screen.get()
    strLength = len(string)


def clear():

    getString()
    screen.delete(strLength-1, tk.END)


def addSpecialCommands():

    operList[5]['command'] = lambda : editScreen('*')
    actionList[0]['command'] = lambda : clear()
    trigList[0]['command'] = lambda : editScreen('sin(')
    trigList[1]['command'] = lambda: editScreen('cos(')
    trigList[2]['command'] = lambda: editScreen('tan(')
    actionList[2]['command'] = lambda : startEngine(None)


def menu():

    global menuBar, edit, history, help, about, rightMenu, history1, help1, about1

    menuBar = tk.Menu(win)
    edit = tk.Menu(menuBar, tearoff=0)
    history = tk.Menu(menuBar, tearoff=0)
    help = tk.Menu(menuBar, tearoff=0)
    about = tk.Menu(menuBar, tearoff=0)
    rightMenu = tk.Menu(win, tearoff=0)

    history1 = tk.Menu(rightMenu, tearoff=0)
    help1 = tk.Menu(rightMenu, tearoff=0)
    about1 = tk.Menu(rightMenu, tearoff=0)


    edit.add_command(label='Copy', command= lambda: screen.event_generate('<<Copy>>'))
    edit.add_command(label='Cut', command=lambda: screen.event_generate('<<Cut>>'))
    edit.add_command(label='Paste', command=lambda: screen.event_generate('<<Paste>>'))
    edit.add_separator()
    edit.add_command(label='Clear Engine', command=lambda:clearEngine())

    rightMenu.add_command(label='Copy', command=lambda: screen.event_generate('<<Copy>>'))
    rightMenu.add_command(label='Cut', command=lambda: screen.event_generate('<<Cut>>'))
    rightMenu.add_command(label='Paste', command=lambda: screen.event_generate('<<Paste>>'))
    rightMenu.add_separator()
    rightMenu.add_command(label='Clear Engine', command=lambda: clearEngine())

    history.add_command(label='Clear History', command=lambda:delHistory())
    history.add_separator()
    history.add_command(label='Previous expression', command=lambda:getHistory(-1))
    history.add_separator()

    history1.add_command(label='Clear History', command=lambda: delHistory())
    history1.add_separator()
    history1.add_command(label='Previous expression', command=lambda: getHistory(-1))
    history1.add_separator()


    win.config(menu=menuBar)
    menuBar.add_cascade(label='Edit', menu=edit)
    menuBar.add_cascade(label='History', menu=history)
    menuBar.add_cascade(label='Help', menu=help)
    menuBar.add_cascade(label='About', menu=about)

    rightMenu.add_cascade(label='History', menu=history1)
    rightMenu.add_separator()
    rightMenu.add_cascade(label='Help', menu=help1)
    rightMenu.add_separator()
    rightMenu.add_cascade(label='About', menu=about1)

    win.bind('<Button-2>', popUp)

def popUp(event):

    try:
        rightMenu.tk_popup(event.x_root, event.y_root)
    finally:
        rightMenu.grab_release()


def uploadToHistory1(str):

    global historyIndex

    historyList.append(str)

    # x is a local variable of lamda whose value is same as historyindex at the time of initialisation
    history.add_command(label=historyList[-1], command= lambda x = historyIndex: getHistory(x))
    history1.add_command(label=historyList[-1], command=lambda x=historyIndex: getHistory(x))
    historyIndex+=1


def delHistory():

    global historyList, historyIndex
    historyList, historyIndex = [], 0

    history.delete(4, tk.END)
    history1.delete(4, tk.END)

def getHistory(index):

    try:
        value = historyList[index]
    except (IndexError):
        display('Error.')
    else:
        display(value)


def startEngine(e):

    getString()
    uploadToHistory1(string)
    calEngine(string+' ')
    answer = numbers[0][0]
    display(answer)
    clearEngine()


def display(str):
    delScreen('a')
    screen.insert(0,str)


def delScreen(e):
    screen.delete(0,tk.END)


def clearEngine():

    global numbers, operators, counter, n
    del numbers
    del operators

    numbers, operators = [[]], [[]]
    counter, n = 0, 0


# calculation engine

def calEngine(s):

    global numbers, operators

    read(s+' ', numbers[0], operators[0])
    cal1(numbers[0], operators[0])


def f1(str,trig):

    global numbers, operators, counter
    numbers.append([])
    operators.append([])
    counter+=1
    return f2(str, counter, trig)


def f2(str, counter, trig):

    read(str, numbers[counter], operators[counter])
    cal1(numbers[counter], operators[counter])

    n = float(numbers[counter][0])

    #print('This: ',numbers[counter][0])

    if trig == 'c':
        n = math.cos(n)

    elif trig == 's':
        n = math.sin(n)

    elif trig == 't':
        n = math.tan(n)

    #print('n: ', n)
    return n


def error():
    pass


def read(s, numm, oper):

    #print('non edit: ',s)
    counter1, counter2 =0, 0
    subString = ''
    start = 0
    index = 0
    trig = 'a'

    while True:

        if not s[index].isalnum():

            if s[index] == '-' or s[index] == '+':

                if s[index-1].isalnum():

                    num = s[start:index]
                    start = index
                    numm.append(num)
                    oper.append('+')

                if s[index-1] == '-' and s[index] == '-':
                    start = index + 1

            elif s[index] == '(':
                #print("working")
                index2 = index

                    # to find the index of the closing bracket
                    # index2 goes out of range where are more ( than )

                while s[index2] != ')' or counter1 != counter2+1 :

                    if s[index2] == '(':
                            counter1+=1
                    if s[index2] == ')':
                            counter2 +=1

                    index2+=1

                    # after running loop we have the index of the closing bracket

                subString = s[index+1:index2]

                 # it stores the answer of terms inside bracket
                #print('inside bracket: ',subString)
                subString = f1(subString+' ', trig)

                # replacing the bracket with the solved answer inside bracket
                # because float cant convert +-
                subString = str(subString)
                if subString[0] == '+':
                    subString = subString[1:]

                if trig !='a':
                    index = index-3


                s = s[0:index] + subString +s[index2+1:]
                #print('edited:',s)

                counter1 = counter2 = 0
                trig = 'a'

            elif s[index] != '.':

                num = s[start:index]
                numm.append(num)
                if s[index]!=' ':
                    oper.append(s[index])
                start = index+1

        if s[index] == 'c':
            trig = 'c'
            index += 2

        if s[index] == 't':
            trig = 't'
            index += 2

        if s[index:index+2] == 'si':
            trig = 's'
            index += 2

        # the code just replicates a for loop
        index+=1
        if index >= len(s):
            break


def cal1(num, oper):

    #print(num, oper)
    index2=0
    while oper != []:
        index = 0
        while index<len(oper): #1

            if oper[index] == opButtons[index2]:

                if num[index][0] == '+':
                    num[index] = num[index][1:]

                elif (num[index][0] == '-' and num[index][1] == '-'):
                    num[index] = num[index][2:]

                if num[index+1][0] == '+':
                    num[index+1] = num[index+1][1:]

                elif (num[index + 1][0] == '-' and num[index + 1][1] == '-'):
                    num[index + 1] = num[index + 1][2:]

                num[index] = str(cal(float(num[index]), float(num[index+1]), opButtons[index2]))

                del(num[index+1])
                del(oper[index])
                continue

            index+=1
        index2+=1


def cal(num1, num2, oper):

    if oper == '^':
        return num1 ** num2
    if oper == '%':
        return num1 % num2
    if oper == '/':
        return num1 / num2
    if oper == '*':
        return num1 * num2
    if oper == '+':
        return num1 + num2
    if oper == '-':
        return num1 - num2

# ...engine end...


def main():

    initialise()
    makeScreen()
    win.bind('<Escape>', delScreen)
    makeButtons()
    addWidgets()
    addSpecialCommands()
    menu()
    win.mainloop()


main()