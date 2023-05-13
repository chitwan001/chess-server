import server.board as board

class Node:
    def __init__(self,board:board.Board) -> None:
        self.board = board
        self.firstChild = None
        self.nextSibling = None
    
    def addNode(self,node):
        if(self.firstChild == None):
            self.firstChild = node
        else:
            self.nextSibling = node
    def generateRandomPosition(self):
        return self.board.generateRandomPosition()
    def alphabeta(self):
        # print(self.board)
        # return self.board.generateRandomPosition()
        bestPosition = self.board.alphabeta(2,float('-inf'), float('inf'),True)
        return bestPosition

head = None
def __init__(boardData,check:bool) -> Node:
    chessboard = board.__init__(boardData,check)
    head = Node(chessboard)
    # print(head.board)
    return head
    # oneMove = head.board.generateRandomPosition()
    # print(oneMove.__repr__())
    # twoMove = oneMove.generateRandomPosition()
    # print(twoMove.__repr__())