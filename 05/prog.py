from typing import List, Tuple


class Line:
    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)

    def __repr__(self) -> str:
        return f"Line(({self.x1},{self.y1}) -> ({self.x2},{self.y2}))"

    @property
    def points(self) -> Tuple[int, int, int, int]:
        return self.x1, self.y1, self.x2, self.y2
    
    def draw(self, grid: List[List[int]]) -> List[List[int]]:
        # print(f"Drawing line {self}")
        num = self.y2 - self.y1
        den = self.x2 - self.x1
        
        if den == 0: # straight up and down
            for y in range(abs(num) + 1):
                ny = (self.y1 if num > 0 else self.y2) + y # determine whether y1 or y2 is higher
                grid[ny][self.x1] += 1
        elif num == 0: # straight left and right
            for x in range(abs(den) + 1):
                nx = (self.x1 if den > 0 else self.x2) + x # determine whether x1 or x2 is lefter
                grid[self.y1][nx] += 1
        else: # diagonal
            for n in range(abs(den) + 1):
                if num > 0 and den > 0: # SE
                    grid[self.y1 + n][self.x1 + n] += 1
                elif num < 0 and den < 0: # NW
                    grid[self.y1 - n][self.x1 - n] += 1
                elif num < 0 and den > 0: # NE
                    grid[self.y1 - n][self.x1 + n] += 1
                elif num > 0 and den < 0: # SW
                    grid[self.y1 + n][self.x1 - n] += 1
        
        return grid



# get all the input
lines: List[Line] = []
with open("./input", "r") as f:
    for line in f:
        start, finish = line.rstrip("\n").split(" -> ")
        sx, sy = start.split(",")
        fx, fy = finish.split(",")
        lines.append(Line(sx, sy, fx, fy))

# get max
largest = 0
for line in lines:
    maxAttr = max(line.points)
    if maxAttr > largest: largest = maxAttr

# create grid
grid = [ [0 for _ in range(largest + 1)] for _ in range(largest + 1) ]

# paint grid
for line in lines:
    # for row in grid: print("".join(map(lambda n: str(n) if n > 0 else '.', row)))
    grid = line.draw(grid)

# print grid
for row in grid: print("".join(map(lambda n: str(n) if n > 0 else '.', row)))

# count the values > 1
total = 0
for row in grid:
    for col in row:
        if col > 1:
            total += 1

print(f"Total: {total}")

