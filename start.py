from tkinter import *
import random

def init(data):
    data.rows = 15
    data.cols = 10
    data.cellSize = 20
    data.margin = 25
    data.emptyColor = "blue"
    data.board = []
    data.isGameOver = False
    data.score = 0
    
    for x in range(data.rows):
        new = []
        for y in range(data.cols):
            new.append(data.emptyColor)
        data.board.append(new)
    
    # data.board[0][0] = "red"
    # data.board[0][data.cols - 1] = "white"
    # data.board[data.rows - 1][0] = "green"
    # data.board[data.rows - 1][data.cols - 1] = "gray"
    
    iPiece = [
        [  True,  True,  True,  True ]
    ]

    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]

    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]

    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]

    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]

    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]

    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    
    data.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    data.tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan", "green", "orange" ]
    
    newFallingPiece(data)
    
def newFallingPiece(data):
    randomIndex = random.randint(0, len(data.tetrisPieces) - 1)
    data.fallingPiece = data.tetrisPieces[randomIndex]
    data.fallingPieceColor = data.tetrisPieceColors[randomIndex]
    
    data.fallingPieceRow = 0
    data.fallingPieceCol = int(data.cols/2 - (len(data.fallingPiece[0]) // 2))
    
def drawFallingPiece(canvas, data):
    for x in range(len(data.fallingPiece)):
        for y in range(len(data.fallingPiece[0])):
            if data.fallingPiece[x][y]:
                drawCell(canvas, data, data.fallingPieceRow + x, data.fallingPieceCol + y, data.fallingPieceColor)
                
def moveFallingPiece(data, drow, dcol):
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    
    if not fallingPieceIsLegal(data):
        data.fallingPieceRow -= drow
        data.fallingPieceCol -= dcol
        return False
        
    return True
    
def fallingPieceIsLegal(data):
    for x in range(len(data.fallingPiece)):
        for y in range(len(data.fallingPiece[0])):
            if data.fallingPiece[x][y] == True:
                if data.fallingPieceRow + x < 0 or data.fallingPieceRow + x > data.rows - 1 or data.fallingPieceCol + y < 0 or data.fallingPieceCol + y > data.cols - 1 or data.board[data.fallingPieceRow + x][data.fallingPieceCol + y] != data.emptyColor:
                    return False
    
    return True 
    
def rotateFallingPiece(data):
    
    tempX = len(data.fallingPiece)
    tempY = len(data.fallingPiece[0])
    tempRow = data.fallingPieceRow
    tempCol = data.fallingPieceCol
    tempPiece = data.fallingPiece
    
    colNum = tempX
    rowNum = tempY - 1
    
    # oldRow + oldNumRows/2 - newNumRows/2
    data.fallingPieceRow = int(tempRow + tempX//2 - tempY//2)
    data.fallingPieceCol = int(tempCol + tempY//2 - tempX//2)
    
    lst = []
    for x in range(tempY):
        part = []
        for y in range(tempX):
            part.append(None)
        lst.append(part)
        
    for a in range(len(tempPiece)):
        for b in range(len(tempPiece[0])):
            lst[len(lst) - 1 - b][a] = tempPiece[a][b]
            
    data.fallingPiece = lst
    
    if fallingPieceIsLegal(data) == False:
        data.fallingPiece = tempPiece
        data.fallingPieceCol = tempCol
        data.fallingPieceRow = tempRow
        
def placeFallingPiece(data):
    for x in range(len(data.fallingPiece)):
        for y in range(len(data.fallingPiece[0])):
            if data.fallingPiece[x][y]:
                data.board[data.fallingPieceRow + x][data.fallingPieceCol + y] = data.fallingPieceColor
                
    removeFullRows(data)
                
def removeFullRows(data):
    data.fullRows = 0
    filled = []
    
    for x in range(len(data.board)):
        count = 0
        for y in range(len(data.board[0])):
            if not data.board[x][y] == data.emptyColor:
                count += 1
        if count == data.cols:
            filled.append(x)
            data.fullRows += 1
            
    data.newBoard = []
    
    for x in range(len(data.board)):
        appnd = []
        for y in range(len(data.board[0])):
            appnd.append(None)
        data.newBoard.append(appnd)
        
    if data.fullRows > 0:
        
        data.score += data.fullRows ** 2
        
        bottom = max(filled)
        top = min(filled)
        
        for x in range(bottom + 1, data.rows):
            for y in range(len(data.board[0])):
                data.newBoard[x][y] = data.board[x][y]
                
        for x in range(bottom, data.fullRows, -1):
            for y in range(len(data.board[0])):
                data.newBoard[x][y] = data.board[top - (bottom - x) - 1][y]
                
        for x in range(len(data.board)):
            for y in range(len(data.board[0])):
                if data.newBoard[x][y] == None:
                    data.newBoard[x][y] = data.emptyColor
                    
        data.board = data.newBoard
        
def drawCell(canvas, data, row, col, fillColor):
    canvas.create_rectangle(data.margin + col * data.cellSize, data.margin + row * data.cellSize, data.margin + col * data.cellSize + data.cellSize, data.margin + row * data.cellSize + data.cellSize, fill = fillColor, width = 3)
    
def drawScore(canvas, data):
    canvas.create_text(data.width / 2, data.margin / 2, fill = "blue", font = "Arial 12", text = "Score: " + str(data.score))
    
def drawBoard(canvas, data):
    for x in range(data.rows):
        for y in range(data.cols):
            drawCell(canvas, data, x, y, data.board[x][y])

def keyPressed(event, data):
    if data.isGameOver == False:
        if event.keysym == "Left":
            moveFallingPiece(data, 0, -1)
        elif event.keysym == "Right":
            moveFallingPiece(data, 0, 1)
        elif event.keysym == "Down":
            moveFallingPiece(data, 1, 0)
        elif event.keysym == "Up":
            rotateFallingPiece(data)
            
    if event.keysym == 'r':
        init(data)

def timerFired(data):
    if data.isGameOver == False:
        if moveFallingPiece(data, 1, 0) == False:
            placeFallingPiece(data)
            newFallingPiece(data)
            if fallingPieceIsLegal(data) == False:
                data.isGameOver = True

def redrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = 'orange', width = 0)
    drawBoard(canvas, data)
    drawFallingPiece(canvas, data)
    drawScore(canvas, data)
    
    if data.isGameOver == True:
        canvas.create_rectangle(data.margin , data.margin + 2 * data.cellSize, data.width - data.margin, data.margin + 5 * data.cellSize + data.cellSize, fill = "black", width = 3)
        canvas.create_text( data.width / 2, data.height / 2 - 70, fill = "yellow", font = "Arial 35", text = "Game Over")

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
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
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 500 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

def playTetris(rows=15, cols=10, cellSize=20, margin=25):
    width = cols * cellSize + margin * 2
    height = rows * cellSize + margin * 2
    run(width, height)
    
playTetris()