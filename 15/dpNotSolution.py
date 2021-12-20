# woa dp problem from 3121
from typing import List, Tuple

def weirdMod(num, m):
    if num < m:
        return num
    else:
        return 1

class Cavern:
    def __init__(self, cavern: List[str]) -> None:
        self.cavern = [ [ 0 for _ in range(len(cavern) * 5) ] for _ in range(len(cavern) * 5) ]
        self.size = len(self.cavern)
        # for row in cavern:  # p1
        #     self.cavern.append(list(map(lambda n: int(n), list(row))))

        # p2 i hate this
        ogSize = len(cavern)
        for row in range(5):
            for col in range(5):
                # make each cell
                for y in range(ogSize):
                    for x in range(ogSize):
                        celly = y + (row * ogSize)
                        cellx = x + (col * ogSize)
                        if row > 0:
                            # grab value from above
                            self.cavern[celly][cellx] = weirdMod(self.cavern[celly - ogSize][cellx] + 1, 10)
                        elif col > 0:
                            # grab from left since top row
                            self.cavern[celly][cellx] = weirdMod(self.cavern[celly][cellx - ogSize] + 1, 10)
                        else:
                            # grab from original cavern
                            self.cavern[celly][cellx] = int(cavern[y][x])

    def lowestTotalRisk(self) -> int:
        paths = [ [ None for _ in range(self.size) ] for _ in range(self.size) ]
        # calculate the lowest path to each cell, starting at top left
        # since the lowest path to a cell depends on the lowest path to the cell above or to the left of it
        for y in range(self.size):
            for x in range(self.size):
                currCell = self.cavern[y][x]
                # check if theres a cell to the left and above
                if x > 0 and y > 0:
                    paths[y][x] = currCell + min(paths[y - 1][x], paths[y][x - 1])
                elif x > 0:
                    paths[y][x] = currCell + paths[y][x - 1]
                elif y > 0:
                    paths[y][x] = currCell + paths[y - 1][x]
                else:
                    paths[y][x] = currCell # 0  # "the starting position is never entered, so its risk is not counted"
        # return the path to bottom right
        self.paths = paths
        return paths[-1][-1]

    # debug
    def printLTRPath(self) -> None:
        start = (self.size - 1, self.size - 1)
        self.ltrpath = self.cavern
        for y in range(self.size):
            for x in range(self.size):
                self.ltrpath[y][x] = [self.ltrpath[y][x], False]
        self.printLTRPathRecurse(start)

        total = 0
        # now print
        for y in range(self.size):
            row = ""
            for x in range(self.size):
                if self.ltrpath[y][x][1]:
                    total += self.ltrpath[y][x][0]
                    row += '\033[4m' + str(self.ltrpath[y][x][0]) + '\033[0m'
                else:
                    row += str(self.ltrpath[y][x][0])
            print(row)
        print(total)

    def printLTRPathRecurse(self, pos: Tuple[int, int]) -> None:
        x, y = pos
        self.ltrpath[y][x][1] = True
        if x > 0 and y > 0:
            if self.paths[y - 1][x] < self.paths[y][x - 1]: 
                self.printLTRPathRecurse((x, y - 1))
            else:
                self.printLTRPathRecurse((x - 1, y))
        elif x > 0:
            self.printLTRPathRecurse((x - 1, y))
        elif y > 0:
            self.printLTRPathRecurse((x, y - 1))
        else:
            return

c = None
with open("input") as f:
    inp = f.read().split("\n")
    c = Cavern(inp)

print(c.lowestTotalRisk())
print(c.cavern[-1][-1])
