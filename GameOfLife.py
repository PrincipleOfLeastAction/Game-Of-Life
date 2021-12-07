from PIL import Image, ImageDraw
from map import Map
import numpy as np
import imageio
# from PIL import Image, Imagedraw

class GameOfLife:
    def __init__(self, width, height, numCells=100, scaleFactor=1):
        self.width = width
        self.height = height
        self.numCells = numCells
        self.scaleFactor = scaleFactor

    def main(self, numFrames = 1, draw=True, buildgif=True):
        if (draw):
            map = Map(self.width, self.height)
            np.random.seed(0)
            randomCellsWidthArray = np.random.randint(0,high=self.width - 1, \
                size=self.numCells).tolist()
            randomCellsHeightArray = np.random.randint(0,high=self.height - 1, \
                size=self.numCells).tolist()
            randomCellsArray = list(zip(randomCellsWidthArray, randomCellsHeightArray))
            print(randomCellsArray)
            map.cells = randomCellsArray

        filename = "./img_output/out"
        extension = ".png"

        # for later use in making gif.
        allFilenames = []

        for imgNum in range(numFrames):
            fullFileName = filename + str(imgNum) + extension
            allFilenames.append(fullFileName)
            if (draw):
                map.draw(fullFileName, scaleFactor=self.scaleFactor)
                if (imgNum == (numFrames - 1)):
                    break
                map.update()
        # Signal to Output where we are in the program.
        if draw:
            print("Building Frames Completed.")

        if (buildgif):
            images = []
            # Now turn it into a gif
            for filename in allFilenames:
                images.append(imageio.imread(filename))
            imageio.mimsave("./gif_output/output.gif", images, loop=1, palettesize=2, subrectangles=True)

if __name__ == "__main__":
    # im = Image.new("1", (15,10), color=1)
    # draw = ImageDraw.Draw(im)
    # draw.point([(i,i) for i in range(9)], fill=0)
    # im.save("./output/out.png")

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
    # 240x138 scaled to 1920x1080
    # game = GameOfLife(240, 135, numCells=320, scaleFactor=8)
    game = GameOfLife(64, 36, numCells=800, scaleFactor=30)
    game.main(numFrames=600, draw=True)
