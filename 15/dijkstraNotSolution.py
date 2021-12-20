# woa dp problem from 3121
from typing import List, Tuple
import heapq

def weirdMod(num, m):
    if num < m:
        return num
    else:
        return 1

# super dirty item for the heap
class Item:
    def __init__(self, x: int, y: int, value: int) -> None:
        self.x = x
        self.y = y
        self.value = value
    
    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __gt__(self, other) -> bool:
        return self.value > other.value

    def __lt__(self, other) -> bool:
        return self.value < other.value

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
        paths = [ [ 100000000 for _ in range(self.size) ] for _ in range(self.size) ]
        visitted = [ [ False for _ in range(self.size) ] for _ in range(self.size) ]
        paths[0][0] = 0
        x, y = 0, 0
        destx = self.size - 1
        desty = self.size - 1

        weights = []

        # dijkstra algorithm with pqueue
        while True:
            tpr = paths[y][x]
            # check each unvisitted direction
            if y > 0 and not visitted[y - 1][x]: # n
                paths[y - 1][x] = min(paths[y - 1][x], tpr + self.cavern[y - 1][x])
            if x > 0 and not visitted[y][x - 1]: # w
                paths[y][x - 1] = min(paths[y][x - 1], tpr + self.cavern[y][x - 1])
            if y < (self.size - 1) and not visitted[y + 1][x]: # s
                paths[y + 1][x] = min(paths[y + 1][x], tpr + self.cavern[y + 1][x])
            if x < (self.size - 1) and not visitted[y][x + 1]:
                paths[y][x + 1] = min(paths[y][x + 1], tpr + self.cavern[y][x + 1])  
            
            # mark curr as visitted now
            visitted[y][x] = True

            if visitted[desty][destx]:
                # have reached the destination, finish
                break
            
            # still need to do more, find smallest node now and go from there
            smallest = 100000000000
            smallestx = 0
            smallesty = 0
            for nexty in range(self.size):
                for nextx in range(self.size):
                    if not visitted[nexty][nextx] and paths[nexty][nextx] < smallest:
                        smallest = paths[nexty][nextx]
                        smallestx = nextx
                        smallesty = nexty
            x = smallestx
            y = smallesty
        
        # for row in paths:
        #     print(row)
        # for row in visitted:
        #     print(row)

        return paths[-1][-1]


c = None
with open("input") as f:
    inp = f.read().split("\n")
    c = Cavern(inp)

print(c.lowestTotalRisk())