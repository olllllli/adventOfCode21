from typing import Any, List

def cloneArray(arr: List[List[Any]]) -> List[List[Any]]:
    return [ row[:] for row in arr ]

class Image:
    def __init__(self, pixels: str) -> None:
        self.pixels = []
        inp = pixels.split("\n")
        for row in inp:
            pRow = []
            for pixel in row:
                pRow.append( 1 if pixel == "#" else 0 )
            self.pixels.append(pRow)
        
        # important for if 0-># and 511->.,
        # for of the infinite pixels which arnt interacting with a known image pixel
        # they will all just flip and flop between # and . after each enhancement, so keep track of their state
        self.outside = 0
        self.realSize = len(self.pixels)


    def __repr__(self) -> str:
        res = ""
        s = self.padding
        f = self.padding + self.realSize
        for row in self.pixels[s:f]:
            for pixel in row[s:f]:
                res += "#" if pixel else "."
            res += "\n"
        return res

    def enhance(self, algorithm: str) -> None:
        # increase the size and
        self.__increaseSize()
        size = len(self.pixels)
        self.realSize += 2
        newPixels = cloneArray(self.pixels)

        # go through
        for y in range(size):
            for x in range(size):
                resolvedSquare = int(self.__getSquare(x, y), 2)
                resultPixel = int(algorithm[resolvedSquare])
                newPixels[y][x] = resultPixel

        # resolve what the outside should turn to now
        outsideSquare = self.outside * 511
        self.outside = int(algorithm[outsideSquare])

        self.pixels = cloneArray(newPixels)

    @property
    def litPixels(self) -> int:
        return sum([ sum(row) for row in self.pixels ])

    # returns a binary string representing the square around a pixel
    def __getSquare(self, x: int, y: int) -> str:
        res = ""
        for ry in range(-1, 2):
            for rx in range(-1, 2):
                res += str(self.__pixel(x + rx, y + ry))
        return res

    # returns the pixel at this coordinate
    def __pixel(self, x: int, y: int) -> int:
        if x < 0 or x >= self.realSize or y < 0 or y >= self.realSize:
            return self.outside
        else:
            return self.pixels[y][x]

    # increases the stored size of the image
    def __increaseSize(self) -> None:
        oldSize = len(self.pixels)
        newPixel = self.outside
        for row in range(oldSize):
            self.pixels[row] = [newPixel] + self.pixels[row] + [newPixel]
        # add extra rows
        self.pixels = [[ newPixel for _ in range(oldSize + 2) ]] + self.pixels + [[ newPixel for _ in range(oldSize + 2) ]]


enhanceAlgo = None
image = None
with open("input") as f:
    enhanceAlgo, rawImage = f.read().split("\n\n")
    image = Image(rawImage)
    enhanceAlgo = enhanceAlgo.replace("#", "1").replace(".", "0")

enhancements = 50
for _ in range(enhancements):
    image.enhance(enhanceAlgo)

print(image.litPixels)
