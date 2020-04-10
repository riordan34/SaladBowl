# saladBowl

# Poppa K Code

from tkinter import *
import random, copy
####################################
# I don't know what I'm doing
####################################
#Can play with up to 6 players
#Each player writes 5 cards
#rounds are 60 seconds
#Rounds are taboo, charades, password

def init(data):
    data.players = 1 #default to single player
    data.round = ''
    data.timer = 10 #60 seconds for each round
    data.timeHelper = 0 #helper to account for 100millisecond delays
    data.cards = [] #blank deck of cards
    data.discard = [] #holder for discard pile
    data.turn = 1 #default to team 1's turn
    data.team1Score = 0 #team 1 score
    data.team2Score = 0 #team 2 Score
    data.cardCreation = True
    data.gameType = 0 #five options [start,taboo,charades,password,over]
    data.activeRound = False
    data.cardsRemaining = len(data.cards)
    data.currentCard =''
    data.drawCard = False
    data.drawCorrect = False
    data.drawSkip = False
    data.drawSkipButton = [data.width*.05,data.height*.85,data.width*.3,data.height*.95] #dimensions for "button"
    data.drawCorrectButton = [data.width*.7,data.height*.85,data.width*.95,data.height*.95] #dimensions for "button"
    data.activeCardXBuffer = 150
    data.activeCardYBuffer = 80
    data.activeScreen = 'Start'
    data.winner = 0

def mousePressed(event, data):
    if (data.activeScreen == 'Round'):
        #if "correct" pressed
        if (int(event.x) > data.drawCorrectButton[0]) and (int(event.x) < data.drawCorrectButton[2]):
            if (int(event.y) > data.drawCorrectButton[1]) and (int(event.y) < data.drawCorrectButton[3]):
                data.drawCorrect = True
        #if "skip" pressed
        elif (int(event.x) > data.drawSkipButton[0]) and (int(event.x) < data.drawSkipButton[2]):
            if (int(event.y) > data.drawSkipButton[1]) and (int(event.y) < data.drawSkipButton[3]):
                data.drawSkip = True
    else: pass

def keyPressed(event, data):
    if (data.activeScreen == 'Start'):
        if (event.keysym == 'Tab'):
            data.activeRound = True
        if (data.gameType == 4):
            if (event.keysym == 'Space'):
                init(data)
                run()

def timerFired(data):
    if (data.activeRound):
        data.timeHelper +=1
        if (data.timeHelper%10 == 0):
            data.timer -= 1
            if data.timer == 0:
                data.activeRound = False

def drawStartScreen(canvas,data):
    turnText = 'Team ' + str(data.turn) +'\'s turn'
    if (data.gameType == 1): data.round = 'Taboo!'
    elif (data.gameType == 2): data.round = 'Charades!'
    elif (data.gameType == 3): data.round = 'Password!'
    roundText = 'This round is ' + str(data.round)
    if (data.gameType >= 1) and (data.gameType <= 3): #taboo,charades or password
        if (data.activeRound == False):
            drawScore(canvas,data)
            drawTimer(canvas,data)
            canvas.create_text(data.width/2,data.height/4,text = roundText,font='Arial 24 bold')
            canvas.create_text(data.width/2,data.height/2,text = turnText,font='Arial 18 bold')
            canvas.create_text(data.width/2,data.height*.75,
                                text = "Click \'Tab\' to begin first round",font='Arial 18 bold')
            canvas.create_text(data.width/2,data.height*.9,text = str(len(data.cards)) + ' cards left',font='Arial 18 bold')
        elif (data.activeRound == True):
            data.drawCard = True
            data.activeScreen = 'Round'
    #draw extra screen if game is over
    elif (data.gameType == 4):
        data.activeRound = False
        data.activeScreen = 'Start'
        if (data.team1Score > data.team2Score):
            data.winner = 1
        elif (data.team1Score < data.team2Score):
            data.winner = 2
        winnerText = 'Team ' + str(data.winner) + ' wins!\nCongratulations!'
        canvas.create_text(data.width/2,data.height*.3,text = winnerText,font='Arial 24 bold')
        canvas.create_text(data.width/2,data.height*.67,
                            text = "Click \'Space\' to start a new game",font='Arial 18 bold')

def playRound(canvas,data):
    drawTimer(canvas,data)
    drawScore(canvas,data)
    #center rectangle of card in center, add/subtract buffer on each side to make card
    xCenter = data.width/2
    yCenter = data.height/2
    xBuf = data.activeCardXBuffer
    yBuf = data.activeCardYBuffer
    x1 = xCenter - xBuf
    x2 = xCenter + xBuf
    y1 = yCenter - yBuf
    y2 = yCenter + yBuf
    if (data.timer > 0):
        #draw card and start playing
        if (data.drawCard):
            data.currentCard = data.cards.pop(random.randint(0,len(data.cards)-1))
            data.drawCard = False
        canvas.create_rectangle(x1,y1,x2,y2,fill = 'lightblue')
        canvas.create_text(data.width/2,data.height/2,text = str(data.currentCard),font='Arial 20')

        #correct answer button
        canvas.create_rectangle(data.drawCorrectButton[0],data.drawCorrectButton[1],
                                data.drawCorrectButton[2],data.drawCorrectButton[3],fill='green')
        canvas.create_text((data.drawCorrectButton[0]+data.drawCorrectButton[2])/2,
                            (data.drawCorrectButton[1]+data.drawCorrectButton[3])/2,text="Correct!",font = "Arial 14 bold")
        #skip card button
        canvas.create_rectangle(data.drawSkipButton[0],data.drawSkipButton[1],
                                data.drawSkipButton[2],data.drawSkipButton[3],fill='red')
        canvas.create_text((data.drawSkipButton[0]+data.drawSkipButton[2])/2,
                            (data.drawSkipButton[1]+data.drawSkipButton[3])/2,text="Skip Card",font = "Arial 14 bold")
        #if "correct" pressed, add score to active team, add card to discard pile
        if (data.drawCorrect):
            data.discard.append(data.currentCard)
            if (data.turn == 1):
                data.team1Score += 1
            else: data.team2Score += 1
            #if no cards left, then move to next round
            if (len(data.cards) == 0):
                deckDepletion(canvas,data)
            #else, draw a new card
            else:
                data.currentCard = data.cards.pop(random.randint(0,len(data.cards)-1))
                data.drawCorrect = False
        if (data.drawSkip):
            data.cards.append(data.currentCard) #return card to deck
            data.currentCard = data.cards.pop(random.randint(0,len(data.cards)-1)) #draw new card
            data.drawSkip = False
    else:
        roundTimeOut(data)

def deckDepletion(canvas,data):
    data.cards = copy.copy(data.discard) #copy discard into active deck
    data.discard = [] #make discard blank
    data.currentCard ='' #make current card 'blank'
    data.gameType += 1
    data.activeRound = False
    data.activeScreen = 'Start'

def roundTimeOut(data):
    data.activeRound = False
    data.cards.append(data.currentCard) #return last card to deck
    if data.turn == 1: #swtich turns
        data.turn = 2
    else: data.turn = 1
    data.activeScreen = 'Start'
    data.timer = 10


def drawScore(canvas,data):
    score1 = 'Team 1 Score: ' + str(data.team1Score)
    score2 = 'Team 2 Score: ' + str(data.team2Score)
    canvas.create_text(data.width*.45,10,text=score1,font='Arial 12 bold')
    canvas.create_text(data.width*.8,10,text=score2,font='Arial 12 bold')

def drawDeck(canvas,data):
    canvas.create_text(data.width/2,data.height/2,text=data.cards[0])

def drawTimer(canvas,data):
    if data.timer > 0:
        time = int(data.timer)
    else: time = 0
    timeMsg = str(time) + ' seconds'
    highlight = 'lightGrey'
    if (time < 11) and (time > 5):
        highlight = 'yellow'
    elif (time <= 5): highlight = 'red'
    canvas.create_rectangle(0,0,80,20,fill=highlight)
    canvas.create_text(40,10,text=timeMsg)


def drawGame(canvas,data):
    if (data.cardCreation):
        inputCard(canvas,data)
    elif (data.activeScreen == "Start"):
        drawStartScreen(canvas,data)
    elif (data.activeScreen == "Round"):
        playRound(canvas,data)

def redrawAll(canvas, data):
    drawGame(canvas,data)

####################################
# use the run function as-is
####################################

def run(width=600, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        if (data.cardCreation == False):
            canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    def inputCard(canvas,data): #call input function to add cards
        def addCards(): #add inputed data to card array
            data.cards.append(e1.get()) #add contents of cell
            data.cards.append(e2.get())
            data.cards.append(e3.get())
            data.cards.append(e4.get())
            data.cards.append(e5.get())
            e1.delete(0,tk.END) #clear contents of cell
            e2.delete(0,tk.END)
            e3.delete(0,tk.END)
            e4.delete(0,tk.END)
            e5.delete(0,tk.END)
            data.cardCreation = False
            timerFiredWrapper(canvas,data)
            data.gameType = 1
            master.destroy() #close window

        master = Tk()
        master.geometry("500x500")
        tk.Label(master, text="Card 1").grid(row=0)
        tk.Label(master, text="Card 2").grid(row=1)
        tk.Label(master, text="Card 3").grid(row=2)
        tk.Label(master, text="Card 4").grid(row=3)
        tk.Label(master, text="Card 5").grid(row=4)

        e1 = tk.Entry(master)
        e2 = tk.Entry(master)
        e3 = tk.Entry(master)
        e4 = tk.Entry(master)
        e5 = tk.Entry(master)

        e1.insert(10,"Clue 1")
        e2.insert(10,"Clue 2")
        e3.insert(10,"Clue 3")
        e4.insert(10,"Clue 4")
        e5.insert(10,"Clue 5")

        e1.grid(row=0, column=1, ipadx=100)
        e2.grid(row=1, column=1, ipadx=100)
        e3.grid(row=2, column=1, ipadx=100)
        e4.grid(row=3, column=1, ipadx=100)
        e5.grid(row=4, column=1, ipadx=100)

        tk.Button(master, text='Submit and Close Window', command=addCards).grid(row=5,
                                                                    column=1,
                                                                    sticky=tk.W,
                                                                    pady=4)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas

    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    if (data.cardCreation == True):
        inputCard(canvas,data)
    elif (data.cardCreation == False):
        timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

####################################
# playSaladBowl() Function
####################################

def playSaladBowl():
    run()

playSaladBowl()

