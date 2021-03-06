# -*- coding: utf-8 -*-
#
#  Class TangramPuzzle
# Author: Chali-Anne Lauzon
#         Marie-France Miousse
#         École Polytechnique de Montréal
#
# This class will be used to solve a tangram puzzle using a A* tree search

from hillclimbing import *
from tangram import *
from node import *
from state import *
import timeit

class TangramPuzzle(object):
    def __init__(self, grid, pieces):
        self.puzzle = grid               # The tangram puzzle
        self.puzzleWidth = len(grid[0])  # The columns
        self.puzzleHeight = len(grid)    # The rows
        self.availablePieces = []
        count = 0
        for x in pieces:
            pieceId = [Tangram(x), count]
            self.availablePieces.append(pieceId)
            count += 1
        self.counter = 0                # The number of choices
        self.nbTotalPieces = len(pieces)        #The number of total pieces
        self.emptyCells = 0             # The number of cells to fill
        for i in range(self.puzzleHeight):
            self.emptyCells += self.puzzle[i].count('*')
        self.availablePieces = sorted(self.availablePieces, key=lambda x:int(x[0].nbCells), reverse=True)

    # To check if two states are the same, we compare the puzzles' completion
    def equals(self, state):
        return self.emptyCells == state.emptyCells

    # Equivalent to printing, but specific to a state
    def show(self):
        for row in self.puzzle:
            for cell in row:
                if cell == -1:
                    print ' ',       # Empty spaces remain empty
                else:
                    print '{:2}'.format(cell),       # Eventually print the piece's number
            print

    # Defines the effects of the actions
    def executeAction(self,(row,cell,orientation, id)):
        self.counter += 1
        # For each space of the piece
        for piece in self.availablePieces:
            if id == piece[1]:
                config = piece[0].getOrientations()[orientation]
                for pieceRow in range(len(config)):
                    for pieceCell in range(len(config[0])):
                        if config[pieceRow][pieceCell] == '*':
                            puzzleRow = pieceRow + row
                            puzzleCell = pieceCell + cell
                            self.puzzle[puzzleRow][puzzleCell] = id
                            self.emptyCells -= 1
                self.availablePieces.remove(piece)

    # Defines the possible actions depending on the situation
    def possibleActions(self):
        actions = []
        tmp = self.goThroughPuzzle(self.availablePieces[0], actions)        # If the biggest piece doesn't fit, no solution will be found.
        if tmp is not None:
            return tmp

    # To break from the nested loops
    def goThroughPuzzle(self, currentPiece, listOfActions):
        actions = list(listOfActions)
        # We go through each space of the puzzle
        for row in range(self.puzzleHeight):
            for cell in range(self.puzzleWidth):
                if self.puzzle[row][cell] == '*':
                    for orientation in range(len(currentPiece[0].getOrientations())):
                        # Check if the piece fits
                        if self.pieceFits((currentPiece[0].getOrientations()[orientation], row, cell)):
                            actions.append((row, cell, orientation, currentPiece[1]))
        return actions

    # Defines the goal conditions
    def isGoal(self):
        # If there are no more available pieces and there are no more empty spaces.
        return self.emptyCells == 0

    # Defines the cost of the state
    def cost(self, (row,cell,orientation, id)):
        for piece in self.availablePieces:
            if id == piece[1]:
                return -1 * piece[0].nbCells

    # No better way to find the shortest path than by completing the puzzle in one go.
    def heuristic(self):
        return self.nbTotalPieces - self.counter

    # Determines if a given piece fits in a given area of the puzzle
    def pieceFits(self, (piece, puzzleRow, puzzleCell)):
        #Check if the top left corner of the piece fits in x,y
        if self.puzzle[puzzleRow][puzzleCell] == '*' and self.puzzle[puzzleRow].count('*') >= piece[0].count('*'):
            for i in range(len(piece)):
                for j in range(len(piece[0])):
                    # Check if out of range
                    if puzzleRow + i >= self.puzzleHeight or puzzleCell + j >= self.puzzleWidth:
                        return False
                    elif piece[i][j] == '*' and self.puzzle[puzzleRow+i][puzzleCell+j] != '*':
                        return False
            return True
        return False