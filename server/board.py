from random import randint as random
from typing import Any

colsName = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
rowsName = ['1', '2', '3', '4', '5', '6', '7', '8']
rowsName.reverse()
class Board:
    def __init__(self,boardData:list[list[str]],maxPlayer:int,movePlayed:str,check:bool) -> None:
        self.boardData = boardData
        self.maxPlayer = maxPlayer
        self.AIColor = 'black'
        self.blackPoints = self.calculatePlayerPoints('black')
        self.whitePoints = self.calculatePlayerPoints('white')
        self.movePlayed = movePlayed
        self.heuristic = self.calculateHeuristic()
        self.whoWon = self.isGameOver() # N= None or continued D = draw B = Black W = White
        self.result = False
        self.check = check

    def __repr__(self):
        strOfBoardData = ''
        for boardRow in self.boardData:
            for square in boardRow:
                if square == '':
                    strOfBoardData+='|    '
                else:
                    strOfBoardData+='| '+square+' '
            strOfBoardData+='|\n'
        strForWhitePoints = 'White Points: '+(str(self.whitePoints))
        strForBlackPoints = 'Black Points: '+(str(self.blackPoints))
        return strOfBoardData+'\n'+strForWhitePoints+'\t'+strForBlackPoints

    def calculateHeuristic(self):
       noOfPieces = {
          'K':0,
          'K1':0,
          'Q':0,
          'Q1':0,
          'N':0,
          'N1':0,
          'B':0,
          'B1':0,
          'P':0,
          'P1':0,
          'R':0,
          'R1':0,
       }
       for boardRow in self.boardData:
           for square in boardRow:
               if(square == ''):
                    continue
               elif(square[0] == 'w'):
                  noOfPieces[square[1].upper()+'1'] += 1 
               elif(square[0] == 'b'):
                  noOfPieces[square[1].upper()] += 1

       #print(noOfPieces) 
       D = 0
       D1 = 0
       I = 0
       I1 = 0
       for row in range(1,7):
          for col in range(0,8):
             nextRow = row+1
             nextCol = col+1
             if(nextCol < 8):
                if((self.boardData[row][col] != '') & (self.boardData[row][nextCol] != '')):
                  if((self.boardData[row][col][1] == 'p') & (self.boardData[row][nextCol][1] != 'p')):
                     if((self.boardData[row][col][0] == 'w') & (self.boardData[row][nextCol][1] == 'w')):
                        I+=1
                     elif((self.boardData[row][col][0] == 'b') & (self.boardData[row][nextCol][1] == 'b')):
                        I1+=1
                if((self.boardData[row][col] != '') & (self.boardData[nextRow][col] != '')):
                  if((self.boardData[row][col][1] == 'p') & (self.boardData[nextRow][col][1] == 'p')): #same row as the next row pawn and same color
                     if((self.boardData[row][col][0] == 'w') & (self.boardData[nextRow][col][0] == 'w')):
                        D+=1
                     elif((self.boardData[row][col][0] == 'b') & (self.boardData[nextRow][col][0] == 'b')):
                        D1+=1
       K = noOfPieces['K']
       K1 = noOfPieces['K1']
       Q = noOfPieces['Q']
       Q1 = noOfPieces['Q1']
       R = noOfPieces['R']
       R1 = noOfPieces['R1']
       B = noOfPieces['B']
       B1 = noOfPieces['B1']
       N = noOfPieces['N']
       N1 = noOfPieces['N1']
       P = noOfPieces['P']
       P1 = noOfPieces['P1']
      
       heu = 200*(K-K1)
       + 9*(Q-Q1)
       + 5*(R-R1)
       + 3*(B-B1 + N-N1)
       + 1*(P-P1)
       - 0.5*(D-D1 + I-I1)
      #  print("Heuristic:",heu)
       return heu

    def ifPieceOnSquare(self,row:int,col:int):
        if self.boardData[row][col] == '':
            return ''
        elif self.boardData[row][col][0] == 'w':
            return 'white'
        elif self.boardData[row][col][0] == 'b':
            return 'black'
        else:
            return ''

    def generateActiveSquaresForPawn (self,row:int,col:int,piece:str):
        # for pawn
        active:list[list[int]] = []
        if(row == 1):
           if self.ifPieceOnSquare(row+2,col) == '':
            if self.ifPieceOnSquare(row+1,col) == '':
              active.append([row+2,col]); #if not moved then 2 squares
              active.append([row+1,col]);
        else:
          if(row<7 and col < 8):
             if self.ifPieceOnSquare(row+1,col) == '':
              active.append([row+1,col]);
        
        if(col<7): #attack on right
           if self.ifPieceOnSquare(row+1,col+1) == 'white': # attack possible
              active.append([row+1,col+1]);
        if(col>0): #attack on left
           if self.ifPieceOnSquare(row+1,col-1) == 'white': # attack possible
              active.append([row+1,col-1]);

        return active
    
    def generateActiveSquaresForWhitePawn(self,row:int,col:int,piece:str):
       # for pawn
        active:list[list[int]] = []
        if(row == 6):
           if self.ifPieceOnSquare(row-2,col) == '':
            active.append([row-2,col]); #if not moved then 2 squares
        else:
          if(row>1 and col < 8):
             if self.ifPieceOnSquare(row-1,col) == '':
              active.append([row-1,col]);
        return active

    def generateActiveSquaresForRook(self,row:int,col:int,piece:str,color:str):
        #for rooks
        active:list[list[int]] = []
           #for down move
        for i in reversed(range(0,row-1)):
          if self.ifPieceOnSquare(i,col) == '':
             active.append([i,col])
          elif self.ifPieceOnSquare(i,col) != color:
            active.append([i,col]);
            break;
          else:
            break
        #for up move
        for i in range(row+1,8):
          if self.ifPieceOnSquare(i,col) == '': active.append([i,col]);
          elif self.ifPieceOnSquare(i,col) != color:
            active.append([i,col]);
            break;
          else:
            break;
        #for right
        for i in range(col+1,8):
          if self.ifPieceOnSquare(row,i) == '':
            active.append([row,i]);
          elif (self.ifPieceOnSquare(row,i) != color):
            active.append([row,i]);
            break;
          else:
            break;
        #for left
        for i in reversed(range(0,col-1)):
          if (self.ifPieceOnSquare(row,i) == ''):
            active.append([row,i]);
          elif (self.ifPieceOnSquare(row,i) != color):
            active.append([row,i]);
            break;
          else:
            break;
        return active

    def generateActiveSquaresForKnight(self,row:int,col:int,piece:str,color:str):
        active:list[list[int]] = []
        upRow = row + 2;
        if upRow <= 7:
          if col - 1 >= 0:
            if self.ifPieceOnSquare(upRow,col-1) != color:
              active.append([upRow,col-1]);
          if col + 1 < 8:
            if self.ifPieceOnSquare(upRow,col+1) != color:
              active.append([upRow,col+1]);
        # #moving down
        downRow = row - 2;
        if downRow >= 1:
          if col - 1 >= 0:
            if self.ifPieceOnSquare(downRow,col-1) != color:
              active.append([downRow,col-1]);
          if col + 1 < 8:
            if self.ifPieceOnSquare(downRow,col+1) != color:
              active.append([downRow,col+1]);
        # #moving left
        leftcol = col - 2;
        if leftcol >= 0:
          if row - 1 >= 1:
            if self.ifPieceOnSquare(row-1,leftcol) != color:
              active.append([row-1,leftcol]);

          if row + 1 <= 7:
            if self.ifPieceOnSquare(row+1,leftcol) != color:
              active.append([row+1,leftcol]);

        # //moving right
        rightcol = col + 2;
        if rightcol < 8:
          if row - 1 >= 1:
            if self.ifPieceOnSquare(row-1,rightcol) != color:
              active.append([row-1,rightcol]);
          if row + 1 <= 7:
            if self.ifPieceOnSquare(row+1,rightcol) != color:
              active.append([row+1,rightcol]);
        return active
    
    def generateActiveSquaresForBishop(self,row:int,col:int,piece:str,color:str):
        active:list[list[int]] = []
        #for down
        if row > 1:
            # for down right
            drTempRow = row - 1
            for i in range(col+1,8):
                if drTempRow == 0:
                    break
                if self.ifPieceOnSquare(drTempRow,i) == '':
                  active.append([drTempRow,i])
                elif self.ifPieceOnSquare(drTempRow,i) == color:
                  break
                else :
                  active.append([drTempRow,i])
                drTempRow -= 1;
            #   //for down left
            dlTempRow = row - 1;
            for i in reversed(range(0,col-1)):
                if dlTempRow == 0:
                  break
                if self.ifPieceOnSquare(dlTempRow,i) == '':
                  active.append([dlTempRow,i])
                elif self.ifPieceOnSquare(dlTempRow,i) != color:
                  active.append([dlTempRow,i])
                else :
                  break
                dlTempRow -= 1;
        # //for up
        if row < 7:
          #for up right
          urcol = col + 1;
          for i in range(row+1,8):
            if urcol > 7:
              break

            if self.ifPieceOnSquare(i,urcol) == '':
              active.append([i,urcol]);
            elif self.ifPieceOnSquare(i,urcol) != color:
              active.append([i,urcol]);
            else:
              break;
            urcol += 1;
          #//for up left
          ulcol = col - 1;
          for i in range(row+1,8):
            if ulcol == -1:
              break

            if self.ifPieceOnSquare(i,ulcol) == '':
              active.append([i,ulcol]);
            elif self.ifPieceOnSquare(i,ulcol) != color:
              active.append([i,ulcol]);
            else :
              break
            ulcol -= 1;
        return active;
    
    def generateActiveSquaresForQueen(self,row:int,col:int,piece:str,color:str):
        #queen behaves as bishop and rook both
        bishopActiveSquares = self.generateActiveSquaresForBishop(row,col,piece,color);
        rookActiveSquares = self.generateActiveSquaresForRook(row,col,piece,color);
        active = bishopActiveSquares + rookActiveSquares;
        return active;
    
    def generateActiveSquaresForKing(self,row:int,col:int,piece:str,color:str):
        active:list[list[int]] = []
        # TODO: if not moved can be castled
        # if (!piece.moved:
        #   // king not moved then can be castled right or left
        #   if (self.ifPieceOnSquare(colsName[col + 2] + row) != self.AIColor)
        #     active.append([colsName[col + 2] + row); // right
        #   if (self.ifPieceOnSquare(colsName[colIndex - 3] + row) != self.AIColor)
        #     active.append([colsName[colIndex - 3] + row); // left

        #move up 1square
        if row < 7:
          if self.ifPieceOnSquare(row+1,col) != color:
            active.append([row+1,col]); #up
          if col > 0:
            if self.ifPieceOnSquare(row+1,col-1) != color:
              active.append([row+1,col-1]); #up left
          if col < 7:
            if self.ifPieceOnSquare(row+1,col+1) != color:
              active.append([row+1,col+1]); #up right


        #move down 1 square
        if row > 1:
          if self.ifPieceOnSquare(row-1,col) != color:
            active.append([row-1,col]); #down
          if col > 0:
            if self.ifPieceOnSquare(row-1,col-1) != color:
              active.append([row-1,col-1]); #down left
          if col < 7:
            if self.ifPieceOnSquare(row-1,col+1) != color:
              active.append([row-1,col+1]); #down right

        #move right 1 square
        if col < 7:
          if self.ifPieceOnSquare(row,col+1) != color:
            active.append([row,col+1]);

        #move left 1 square
        if col > 0:
          if self.ifPieceOnSquare(row,col-1) != color:
            active.append([row,col-1]);
        return active;

    def calculatePossibleMovesForWhite(self,activeSquare):
      if(activeSquare == [-1,-1]):
           return []
      else:
         boardData = self.boardData
         activeMoves =[]
         row = activeSquare[0]
         col = activeSquare[1]
         pieceSelected = boardData[row][col]
         # print("Selected piece: ",pieceSelected)
         if(self.check == False):
          if( pieceSelected[1] == 'p'):
             activeMoves = self.generateActiveSquaresForWhitePawn(row,col,pieceSelected)
          elif( pieceSelected[1] == 'n'):
             activeMoves = self.generateActiveSquaresForKnight(row,col,pieceSelected,'white')
          elif( pieceSelected[1] == 'b'):
             activeMoves = self.generateActiveSquaresForBishop(row,col,pieceSelected,'white')
          
          elif( pieceSelected[1] == 'r'):
             activeMoves = self.generateActiveSquaresForRook(row,col,pieceSelected,'white')
          
          elif( pieceSelected[1] == 'q'):
             activeMoves = self.generateActiveSquaresForQueen(row,col,pieceSelected,'white')
          
          elif( pieceSelected[1] == 'k'):
             activeMoves = self.generateActiveSquaresForKing(row,col,pieceSelected,'white')
         else:
            if(pieceSelected[1] == 'k'):
                  activeMoves = self.generateActiveSquaresForKing(row,col,pieceSelected,'white')
         return activeMoves   
  
    def calculatePossibleMovesForBlack(self,activeSquare):
        if(activeSquare == [-1,-1]):
           return []
        else:
            boardData = self.boardData
            activeMoves =[]
            row = activeSquare[0]
            col = activeSquare[1]
            pieceSelected = boardData[row][col]
            # print("Selected piece: ",pieceSelected)
            if(self.check == False):
               if( pieceSelected[1] == 'p'):
                activeMoves = self.generateActiveSquaresForPawn(row,col,pieceSelected)
               elif( pieceSelected[1] == 'n'):
                  activeMoves = self.generateActiveSquaresForKnight(row,col,pieceSelected,'black')
               elif( pieceSelected[1] == 'b'):
                  activeMoves = self.generateActiveSquaresForBishop(row,col,pieceSelected,'black')
               elif( pieceSelected[1] == 'r'):
                  activeMoves = self.generateActiveSquaresForRook(row,col,pieceSelected,'black')
               elif( pieceSelected[1] == 'q'):
                  activeMoves = self.generateActiveSquaresForQueen(row,col,pieceSelected,'black')
               elif( pieceSelected[1] == 'k'):
                  activeMoves = self.generateActiveSquaresForKing(row,col,pieceSelected,'black')
            else:
               if(pieceSelected[1] == 'k'):
                  activeMoves = self.generateActiveSquaresForKing(row,col,pieceSelected,'black')
            return activeMoves      

    def toggleMaxPlayer(self):
        self.maxPlayer = 0 if self.maxPlayer == 1 else 1
    
    # Pawn -> 10
    # Knight -> 30
    # Bishop -> 30
    # Rook -> 50
    # Queen -> 90
    # King -> 900
    # TOTAL -> 1290

    def calculatePoints(self,piece):
        points = 0
        if(piece[1] == 'p'): #pawn
            points=10
        elif(piece[1] == 'n' or piece[1] == 'b'): #knight or bishop
            points=30
        elif(piece[1] == 'r'): #rook
            points=50
        elif(piece[1] == 'q'): #queen
            points=90
        elif(piece[1] == 'k'): #king
            points=900
        return points

    def calculatePlayerPoints(self,type):
        boardData = self.boardData
        whitePointsLeft = 0
        blackPointsLeft = 0
        for boardRow in boardData:
            for square in boardRow:
                if(square == ''):
                    continue
                elif(square[0] == 'w'):
                    whitePointsLeft += self.calculatePoints(square)
                elif(square[0] == 'b'):
                    blackPointsLeft += self.calculatePoints(square)
        whitePoints = 1290 - blackPointsLeft
        blackPoints = 1290 - whitePointsLeft
        if(type == 'white'):
            return whitePoints
        elif(type == 'black'):
            return blackPoints
        return 0

    def generateSquaresAttackedByBlackPawn(self,row:int,colIndex:int):
       active: list[str] = [];
       if (row != '1'):
         if (colIndex > 0 & self.ifPieceOnSquare(row+1,colIndex+1) == 'white'):
           #attack to its right
           active.append(colsName[colIndex - 1] + (row - 1));
         if (colIndex < 7 & self.ifPieceOnSquare(row+1,colIndex-1) == 'white'):
           #can attack to its left
           active.append(colsName[colIndex + 1] + (row - 1));
       return active;
    def generateSquaresAttackedByBlackKing(self,row:int,colIndex:int,playerColor):
        active: list[str] = [];
        #move up 1 square
        if (row < 8):
          if (self.ifPieceOnSquare(row+1,colIndex) != playerColor):
            active.append(colsName[colIndex] + str(row + 1)); #up
          if (colIndex > 0):
            if (self.ifPieceOnSquare(row+1,colIndex-1) != playerColor):
              active.append(colsName[colIndex - 1] + str(row + 1)); #up left

          if (colIndex < 7):
            if (self.ifPieceOnSquare(row+1,colIndex+1) != playerColor):
              active.append(colsName[colIndex + 1] + str(row + 1)); #up right

        #move down 1 square
        if (row > 1):
          if (self.ifPieceOnSquare(row-1,colIndex) != playerColor):
            active.append(colsName[colIndex] + str(row - 1)); #down
          if (colIndex > 0):
            if (self.ifPieceOnSquare(row-1,colIndex-1) != playerColor):
              active.append(colsName[colIndex - 1] + str(row - 1)); #down left

          if (colIndex < 7):
            if (self.ifPieceOnSquare(row-1,colIndex+1) != playerColor):
              active.append(colsName[colIndex + 1] + str(row - 1)); #down right

        #move right 1 square
        if (colIndex < 7):
          if (self.ifPieceOnSquare(row,colIndex+1) != playerColor):
            active.append(colsName[colIndex + 1] + str(row));
        #move left 1 square
        if (colIndex > 0):
          if (self.ifPieceOnSquare(row,colIndex-1) != playerColor):
            active.append(colsName[colIndex - 1] + str(row));
        return active;


    def checkIfSquaresAreAttackedByBlack(self):
       blackPieces:list[dict[str, Any]]= [];
       for row in range(0,8):
          for col in range(0,8):
             if(self.boardData[row][col] != ''):
              if(self.boardData[row][col][0] == 'b'):
                 blackPieces.append({
                    "row": row,
                    "col": col,
                    "piece": self.boardData[row][col][1]
                 })
       squaresAttacked:list[str] = [];
       for i in range (0,len(blackPieces)):
        aPiece = blackPieces[i];
        row = aPiece['row']
        col = aPiece['col']
        piecename = aPiece['piece'];
        if (piecename == 'p'):
          squaresAttacked.append(self.generateSquaresAttackedByBlackPawn(row,col))
        elif (piecename == 'r'):
          squaresAttacked.append(self.generateActiveSquaresForRook(row,col, 'br','black'))
        elif (piecename == 'n'):
          squaresAttacked.append(self.generateActiveSquaresForKnight(row,col, 'bn','black'))
        elif (piecename == 'b'):
          squaresAttacked.append(self.generateActiveSquaresForBishop(row,col, 'bb','black'));
        elif (piecename == 'q'):
          squaresAttacked.append(self.generateActiveSquaresForQueen(row,col, 'bq','black'));
        elif (piecename == 'k'):
          squaresAttacked.append(self.generateSquaresAttackedByBlackKing(row,col, 'black'));
        return squaresAttacked
    def generateRandomPosition(self,maxPlayer:bool):
        boardData = self.boardData
        selectedPiece = ''
        while(True):
           randomRow = random(0,7)
           randomCol = random(0,7)
           piece = boardData[randomRow][randomCol]
           if(piece ==''):
              continue
           elif(piece[0] == 'b' and maxPlayer == True):
              selectedPiece = piece
              # print("Selected square: ",[randomRow,randomCol])
              activeMoves = self.calculatePossibleMovesForBlack([randomRow,randomCol])
              if(activeMoves != []):
                 randomMoveInd = random(0,len(activeMoves)-1)
                 randomMove = activeMoves[randomMoveInd]
                 newBoardData = boardData
                 newBoardData[randomRow][randomCol] = ''
                 newBoardData[randomMove[0]][randomMove[1]] = selectedPiece
                 toggledMaxPlayer = 0 if self.maxPlayer == 1 else 1
                 movePlayed = colsName[randomCol]+rowsName[randomRow]+'->'+colsName[randomMove[1]]+rowsName[randomMove[0]]
                #  print("Move Played: ",movePlayed)
                 newBoard = Board(newBoardData,toggledMaxPlayer,movePlayed,False)
                 return newBoard
           elif(piece[0]=='w' and maxPlayer == False):
              selectedPiece = piece
              # print("Selected square: ",[randomRow,randomCol])
              activeMoves = self.calculatePossibleMovesForWhite([randomRow,randomCol])
              if(activeMoves != []):
                 randomMoveInd = random(0,len(activeMoves)-1)
                 randomMove = activeMoves[randomMoveInd]
                 #print(rowsName[randomRow])
                 newBoardData = boardData
                 newBoardData[randomRow][randomCol] = ''
                 newBoardData[randomMove[0]][randomMove[1]] = selectedPiece
                 toggledMaxPlayer = 0 if self.maxPlayer == 1 else 1
                 movePlayed = colsName[randomCol]+rowsName[randomRow]+'->'+colsName[randomMove[1]]+rowsName[randomMove[0]]
                #  print("Move Played: ",movePlayed)
                 newBoard = Board(newBoardData,toggledMaxPlayer,movePlayed,False)
                 return newBoard

    def isGameOver(self):
      whiteking = {
         "row" : -1,
         "col": -1
      }
      blackKing = {
         "row" : -1,
         "col": -1
      }
      for row in range(0,8):
         for col in range(0,8):
            if(self.boardData[row][col] == 'wk'):
               whiteking['col'] = col
               whiteking['row'] = row
            if(self.boardData[row][col] == 'bk'):
               blackKing['col'] = col
               blackKing['row'] = row
      if(whiteking['row'] != -1 & whiteking['col'] != -1):
         whitekingMoves = self.generateActiveSquaresForKing(whiteking['row'],whiteking['col'],'wk','white')
         attackedSquares: list[str] = self.checkIfSquaresAreAttackedByBlack();
         result = True
         for whiteKingMove in whitekingMoves:
            if(attackedSquares.__contains__(whiteKingMove) == False):
               result = False
               break
        
         if(result == True):
            checkmate = attackedSquares.__contains__(whiteking['col']+whiteking['row'])
            if(checkmate == True):
               self.result = True
               self.whoWon = 'B'
            else:
               self.result = True
               self.whoWon = 'D'
      if(blackKing['row'] != -1 & blackKing['col'] != -1):
         blackKingMoves = self.generateActiveSquaresForKing(blackKing['row'],blackKing['col'],'bk','black')
         attackedSquares: list[str] = self.generateActiveSquaresForKing(blackKing['row'],blackKing['col'],'bk','black');
         result = True
         for blackKingMove in blackKingMoves:
            if(attackedSquares.__contains__(blackKingMove) == False):
               result = False
               break
        
         if(result == True):
            checkmate = attackedSquares.__contains__(blackKing['col']+blackKing['row'])
            if(checkmate == True):
               self.result = True
               self.whoWon = 'W'
            else:
               self.result = True
               self.whoWon = 'D'
    
    def alphabeta(self,depth:int,alpha: float,beta:float,maxPlayer:bool):
       if depth == 0 or self.result == True:
        return self.heuristic
       if maxPlayer == True:
           value = float('-inf')
           for i in range(0,depth):
               newPos = self.generateRandomPosition(maxPlayer)
              #  print("Random Position: ",print(newPos))
               heuristic = newPos.alphabeta(depth - 1, alpha, beta, False)
               if(isinstance(heuristic,int)):
                value = max(value, heuristic)
               elif(isinstance(heuristic,Board)):
                  value = max(value,heuristic.heuristic)
              #  print("Heuristic:",value)
              #  self.boardData.undo_move(move)
               alpha = max(alpha, value)
              #  print("Alpha:",alpha)
               if alpha >= beta:
                   break
           if(len(self.movePlayed) == 0):
              self.movePlayed=newPos.movePlayed
           else:
              self.movePlayed+='->'+newPos.movePlayed
           return newPos
       else:
           value = float('inf')
           for i in range(0,depth):
               #print(self.boardData)
               newPos = self.generateRandomPosition(maxPlayer)
              #  print("Random Position: ",print(newPos))
               heuristic = newPos.alphabeta(depth - 1, alpha, beta, True)
               if(isinstance(heuristic,int)):
                value = max(value, heuristic)
               elif(isinstance(heuristic,Board)):
                  value = max(value,heuristic.heuristic)
              #  self.boardData.undo_move(move)
               beta = min(beta, value)
              #  print("Beta:",beta)
               if alpha >= beta:
                   break
           if(len(self.movePlayed) == 0):
              self.movePlayed=newPos.movePlayed
           else:
              self.movePlayed+='->'+newPos.movePlayed
           return newPos


def __init__(boardData:list[list[str]],check:bool) -> Board:
    board = Board(boardData,1,'',check)
    return board