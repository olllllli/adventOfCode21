from typing import List

def listAnd(l1: List[str], l2: List[str]) -> List[str]:
    res = []
    for i in range(len(l1)):
        if l1[i] == "#" or l2[i] == "#":
            res.append("#")
        else:
            res.append(".")
    return res

def gridColToRow(grid: List[List[str]], col: int) -> List[str]:
    res = []
    for y in range(len(grid)):
        res.append(grid[y][col])
    return res

def gridColPop(grid: List[List[str]]) -> List[List[str]]:
    for y in range(len(grid)):
        grid[y].pop()
    return grid

class Paper:
    def __init__(self, inp: List[str]) -> None:
        # find the largest size
        dots = []
        largestx = 0
        largesty = 0
        for entry in inp:
            x, y = entry.split(",")
            dots.append((int(x), int(y)))
            if int(x) > largestx: largestx = int(x)
            if int(y) > largesty: largesty = int(y)

        # create grid and paint dots
        self.page = [ [ "." for _ in range(largestx + 1) ] for _ in range(largesty + 1) ]
        for dot in dots:
            self.page[dot[1]][dot[0]] = "#"

        self.rows = len(self.page)
        self.cols = len(self.page[0])

    def __repr__(self) -> str:
        res = ""
        for row in self.page:
            res += "".join(row)
            res += "\n"
        return res

    def fold(self, axis: str, pos: int) -> None:
        if axis == "y":
            for i in range(self.rows - pos - 1):
                row = self.page[self.rows - i - 1]
                self.page[i] = listAnd(self.page[i], row)
                self.page.pop()
            self.page.pop()
            self.rows = len(self.page)

        elif axis == "x":
            for i in range(self.cols - pos - 1):
                col = gridColToRow(self.page, self.cols - i - 1)
                result = listAnd(gridColToRow(self.page, i), col)
                for y in range(self.rows): 
                    self.page[y][i] = result[y]
                gridColPop(self.page)
            gridColPop(self.page)
            self.cols = len(self.page[0])

    def dots(self) -> int:
        count = 0
        for row in self.page:
            count += row.count("#")
        return count


dots = None
folds = None
with open("input") as f:
    inp = f.read().split("\n")
    emptyLine = inp.index("")
    dots = inp[:emptyLine]
    folds = inp[emptyLine+1:]

p = Paper(dots)
for f in folds:
    axis, pos = (f.split(" ")[2]).split("=")
    p.fold(axis, int(pos))

print(p)
print(p.dots())