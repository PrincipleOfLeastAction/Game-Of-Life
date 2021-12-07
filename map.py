from numpy import random
from collections import Counter
from PIL import Image, ImageDraw

class Map:
    def __init__(self, width, height):
        self.__dimension = (width, height)
        self.__cells = Counter()

    @property
    def dimension(self):
        return self.__dimension

    # @dimension.setter
    # def dimension(self, dimension):
    #     self.__dimension = dimension
    
    @property
    def cells(self):
        return self.__cells

    ''' This function raises value error if the cells array is
    out of bounds.
    '''
    @cells.setter
    def cells(self, cells):
        ''' Disabled __cellsInBounds to improve performance.'''
        # if not self.__cellsInBounds(cells):
        #     raise ValueError("Cells array out of bounds.")
        # else:
        self.__cells = Counter(cells)
    
    ''' I may disable this to improve performance '''
    def __cellsInBounds(self, lst):
        for point in lst:
            # if x coordinate is smaller than 0 or is equal to or bigger than
            # width, we return false.
            if (point[0] < 0) or (point[0] >= self.dimension[0]):
                return False
            elif (point[1] < 0) or (point[1] >= self.dimension[1]):
                return False 
        return True

    ''' This function draws the map at the moment and then saves it as
    filename with an extension.
    '''
    def draw(self, filename, scaleFactor = 1):
        im = Image.new("1", self.__dimension, color=1)
        draw = ImageDraw.Draw(im)
        draw.point(list(self.__cells.keys()), fill=0)
        # del draw
        im = im.resize((self.__dimension[0] * scaleFactor, self.__dimension[1] * scaleFactor))
        im.save(filename)

    def __numNeighbours(self, key):
        numNeightbours = 0
        adjList = self.__adjacentList(key)
        for adjPos in adjList:
            # If a cell occupies an adjacent cell, then we add 1 to
            # num neighbours.
            if self.__cells[adjPos]:
                numNeightbours += 1
        return numNeightbours

    def __adjacentList(self, position):
        corners = [
            (position[0] - 1, position[1] - 1), 
            (position[0] + 1, position[1] - 1),
            (position[0] - 1, position[1] + 1),
            (position[0] + 1, position[1] + 1)]
        plus = [
            (position[0], position[1] - 1),
            (position[0], position[1] + 1),
            (position[0] - 1, position[1]),
            (position[0] + 1, position[1])]
        adjList = corners + plus

        # now remove any out of bounds points.
        for point in adjList:
            if (point[0] < 0) or (point[0] >= self.dimension[0]):
                adjList.remove(point)
            elif (point[1] < 0) or (point[1] >= self.dimension[1]):
                adjList.remove(point)
        return adjList
    
    ''' This function finds a list of dead cells which are going
    to reproduce in next state
    '''
    def __reproduceCells(self):
        # this list holds a list of BLANK adjacent cell for every cell in 
        # the map.
        allCellAdjList = Counter()
        reproduceCells = Counter()
        for cellPos in self.__cells.keys():
            tmpAdjList = self.__adjacentList(cellPos)
            # removing the non-blank cells.
            for position in tmpAdjList:
                # if it isn't a blank cell remove it from adj list.
                if self.__cells[position]:
                    tmpAdjList.remove(position)
            allCellAdjList += Counter(tmpAdjList)
        
        # now we have a Counter of all blank spaces that is next to a living cell.
        # Find a blank cell that is next to 3 living cell and add to list.
        for position in allCellAdjList.keys():
            # if it has exactly 3 occurances
            if allCellAdjList[position] == 3:
                reproduceCells[position] = 1
        return reproduceCells

    def update(self):
        nextState = Counter()
        # Grab the cells that survive to next state with 2/3
        # neighbours.
        for cellKeys in self.__cells.keys():
            numNeightbours = self.__numNeighbours(cellKeys)
            # if 2 or more neighbours, cell survive to next state.
            if numNeightbours == 2 or numNeightbours == 3:
                nextState[cellKeys] = 1
        # add the cells that give birth.
        nextState += self.__reproduceCells()
        self.__cells = nextState
        return

if __name__ == "__main__":

    # numPoints = 4
    # arr = np.random.randint(0,high=10, size=(numPoints,2))
    # arr = arr.tolist()
    # print(arr)
    # arr = [tuple(lst) for lst in arr]
    # 3 neighbour test
    # arr = [(4,4), (5,5),(4,5), (5,4)]
    # 2 neighbour and reproduction test
    # arr = [(4,4), (5,5), (4,5)]
    # reproduction and death test
    # arr = [(4,4), (4,6), (6,4)]
    filename = "out"
    extension = ".png"
    imgNum = 0
    map = Map(20,15)
    # # try:
    # #     map.cells = arr
    # # except ValueError as ve:
    # #     exit()
    # map.cells = arr

    print(map.dimension)
    print(map.cells)
    map.draw(filename + str(imgNum) + extension)
    imgNum += 1
    map.update()
    map.draw(filename + str(imgNum) + extension)
    # print(map.cellsInBounds(arr))
