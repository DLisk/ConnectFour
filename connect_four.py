import random

def initiateboard(rows,cols):
    '''
    rows and cols are ints that represent the number of rows and columns
    in the connect4 board. Standard is 6 rows and 7 columns.
    '''
    board = []
    for i in range(cols):
        board.append([' ']*rows)
    return board

def drawboard(currentBoard):
    '''
    currentBoard should be a list of size column, with each of those lists
    with size row.
    The values of each item in the list reflect positions of chips 
    '''
    #prints out the heading of the board, which shows user where each column is
    heading = ''
    for i in range(len(currentBoard)):
        heading = heading + '  col' + str(i+1) + ' '
    print heading

    #prints out the rest of the board and values
    for k in range(len(currentBoard[0][:])):
        temprow = '|'
        underline = '|'
        for j in range(len(currentBoard)):
            temprow = temprow + '   ' + str(currentBoard[j][k]) + '  |'
            underline = underline + '------|'
        print temprow
        print underline

    
def MakeAMove(col, symbol, board):
    '''
    col is an int representing the name of the column, NOT the index in the list
    board. The index is col-1
    symbol is the string that represents the player's chip
    board is a list with the current values on the board.
    This function places the symbol that the player is using at the bottom
    most available row of the column chosen
    Returns symbol, the row the chip is placed in, and the column the chip is placed in
    '''
    for i in range(len(board[col-1])-1,-1,-1):
        if board[col-1][i] == ' ':
            board[col-1][i] = str(symbol)
            break
    return (symbol, i, col-1)

def ifMadeAMove(col, board):
    '''
    col is an int. It is the number of the column, NOT the index in the list board
    board is a list with the current values on the board.
    Function returns the row that chip would land in if placed in column col
    If column is full, returns -1
    '''
    for i in range(len(board[col-1])-1,-1,-1):
        if board[col-1][i] == ' ':
            return i    
    return -1

def isValidMove(board, column):
    '''
    column is the int that is the number of the column printed, NOT the index
    index is equal to column - 1
    board is the list representing the board
    returns true if the move is valid, else returns false
    '''
    if column <= 0 or column > len(board) or board[column-1][0] != ' ':
        print('Not a Valid Move.')
        return False    
    return True

def isBoardFull(board):
    '''
    returns True if board is full, otherwise returns False
    '''
    for i in range(len(board)):
        if board[i][0] == ' ':
            return False
    return True

def isWinner(board, letter, currow, curcol):
    '''
    board is a list of lists representing the current state of the board
    letter is the symbol of the player
    currow and curcol are ints that represent the position that is being checked
    to see if there is a winning move
    returns true if letter in positions currow and curcol
    produces a winner, otherwise it return false
    '''
  
    #counts number of tiles in a row in direction given
    def inarow(incr, incc, currow, curcol):
        '''
        position at row currow and column curcol, both of which are ints
        incr represents how to increment the row each step, it is an int
        incc represents how to increment the column each step, it is an int
        the row and column are incremented according to incr and incc and the
        amount of symbols in a row are returned
        currow and curcol represent the indexes, not the names columns and rows
        '''
        
        row = currow + incr
        col = curcol + incc

        if col== len(board) or col== -1 or row == len(board[0]) or row==-1:
            return 0
        elif board[col][row] != str(letter):
            return 0
        else:
            return 1 + inarow(incr, incc, row, col)
    
    ## to check diagonal from bottom left to top right
    if inarow(-1,1,currow, curcol) + inarow(1,-1,currow, curcol) >= 3:
        return True
    ## to check diagonal from top left to bottom right
    elif inarow(1,1,currow,curcol) + inarow(-1,-1,currow,curcol) >= 3:
        return True
    ## to check horizontal
    elif inarow(0, 1, currow, curcol) + inarow(0,-1,currow,curcol) >= 3:
        return True
    ## to check vertical
    elif inarow(-1,0,currow, curcol) + inarow(1,0,currow, curcol) >= 3:
        return True

    return False
            
    
def computermove(board,player,computer):
    '''
    board is list of list.
    player is symbol player uses and computer is symbol computer uses
    decides where computer should move
    '''

    allowedCols = []
    okCols = []
    recommendedCols = []

    for column in range(len(board)):
        row = ifMadeAMove(column+1, board)
        if row != -1:
            allowedCols.append(column)
            okCols.append(column)
            recommendedCols.append(column)
            #if this move would make the computer win, make that move
            if isWinner(board, computer, row, column):
                return MakeAMove(column+1, computer, board) 

            #if this move would block the player from winning, moake that move
            elif isWinner(board, player, row, column):
                return MakeAMove(column+1, computer, board)
            
            #if your move will make it possible for player to win next move,
            #make it a less favorable move
            if isWinner(board, player, row-1, column):
                recommendedCols.remove(column)
                okCols.remove(column)

            #if this move will stop you from winning the next move, if player
            #blocks it, make it a less favorable move
            if isWinner(board,computer,row-1,column):
                recommendedCols.remove(column)
                
    #if there are recommended moves (in list recommendedcols), choose from those
    #otherwise, if there are ok moves (in list OKCols), choose from those
    #otherwise choose from any available moves
    if len(recommendedCols) != 0:
        return MakeAMove(random.choice(recommendedCols)+1, computer, board)
    elif len(okCols) != 0:
        return MakeAMove(okCols.choice(allowedCols)+1, computer, board)
    return MakeAMove(random.choice(allowedCols)+1, computer, board)
        

def replay():
    '''
    Finds out if player would like to play again
    '''
    answer = raw_input('Would you like to play again? If yes type y. Otherwise type any key: ')
    if answer.lower() == 'y':
        print('Lets start a new game!')
        play()
    else:
        print('It was great playing with you, Goodbye! :)')


## SETS UP AND STARTS THE GAME
def play():
    print("Hello, Welcome to Connect Four!")
    rows = 6
    cols = 7
    player = ' '
    computer = ' '
    playing = True

    # assigns symbols to players
    while player not in 'XxOo' or player == '':
        player = raw_input('Please choose either X or O as your symbol during this game. Print your choice: ').upper()
    if player == 'X':
        computer = 'O'
    else:
        computer = 'X'

    #decides which player goes first
    if random.randrange(0,2) == 0:
        print('You have the first turn!')
        turnNow = 'player'
    else:
        print('The computer has the first turn, I will go first!')
        turnNow = 'computer'

    print 'Lets start playing :)'
    board = initiateboard(rows,cols)
    drawboard(board)

    while playing:       
        if turnNow == 'player':
            valid = False
            while not valid:
                move = raw_input('It is your turn. \nPrint the number of the column you would like to drop your chip in: ')                
                try:
                    move = int(move)
                    valid = isValidMove(board,move)
                except ValueError:
                    print('Oops, please enter a column number.')
                    valid = False
            move = int(move)            
            symbol1, r1, c1 = MakeAMove(move, player ,board)
            drawboard(board)
            if isWinner(board,player,r1,c1):
                print('Congrats! You Win!')
                playing = False        
            elif isBoardFull(board):
                print('Game over, its a tie.')
                playing = False
            else:
                turnNow = 'computer'
        else:
            print('My turn now')
            symbol2, r2, c2 = computermove(board, player, computer)
            drawboard(board)
            print('I just dropped my chip in column ' + str(c2+1))
            if isWinner(board,computer,r2,c2):
                print('I win. Good luck next time!')
                playing = False
            elif isBoardFull(board):
                print('Game over, its a tie.')
                playing = False
            else:
                turnNow = 'player'
    replay()
        
play()
