class Octopie:
    def __init__(self, grid) -> None:
        self.grid = []
        for row in grid.split("\n"):
            self.grid.append(list(map(lambda n: int(n), list(row))))
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.flashes = 0

    def __repr__(self) -> str:
        res = ""
        for row in self.grid:
            for col in row:
                res += str(col)
            res += "\n"
        return res
        
    def step(self) -> bool:
        self.alreadyFlashed = set()
        for y in range(self.rows):
            for x in range(self.cols):
                self.increase(x, y)
        if len(self.alreadyFlashed) == (self.rows * self.cols): # p2 check if all were flashed
            return True 
    
        self.alreadyFlashed = set()
        return False

    def increase(self, x, y) -> None:
        maxRow = self.rows - 1
        maxCol = self.cols - 1

        # check if out of bounds or already flashed
        if x < 0 or y < 0 or x > maxCol or y > maxRow:
            return
        elif (x, y) in self.alreadyFlashed:
            return

        # else increase
        self.grid[y][x] += 1

        # check if needs to flash
        if self.grid[y][x] > 9:
            self.grid[y][x] = 0
            self.flashes += 1
            self.alreadyFlashed.add((x, y))
            # increase all adjacent
            self.increase(x - 1, y - 1)
            self.increase(x - 1, y)
            self.increase(x - 1, y + 1)
            self.increase(x, y + 1)
            self.increase(x + 1, y + 1)
            self.increase(x + 1, y)
            self.increase(x + 1, y - 1)
            self.increase(x, y - 1)

with open("input") as f:
    inp = f.read()
    o = Octopie(inp)
    print(o)
    for i in range(100000):
        res = o.step()
        if res:
            print(i + 1)
            break
    print(o)
    print(o.flashes)