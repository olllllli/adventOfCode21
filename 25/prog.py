from typing import List, Tuple


class Cucumbers:
    def __init__(self, map: str) -> None:
        self.map = []
        for row in map.split("\n"):
            self.map.append(list(row))
        self.width = len(self.map[0])
        self.height = len(self.map)

    def __repr__(self) -> str:
        res = []
        for row in self.map:
            res.append("".join(row))
        return "\n".join(res)

    # move a single cucumber, use the data from self.map, and write to map
    def moveCucumber(self, x: int, y: int, map: List[List[str]]) -> Tuple[bool, List[List[str]]]:
        cucumber = self.map[y][x]
        if cucumber == ">":
            nx = (x + 1) % self.width
            ny = y
        elif cucumber == "v":
            nx = x
            ny = (y + 1) % self.height
        else:
            return (False, map)

        nextSpot = self.map[ny][nx]
        if nextSpot == ".":
            map[ny][nx] = cucumber
            map[y][x] = "."
            return (True, map)
        else:
            return (False, map)

    # complete a full movement of all cucumbers
    def step(self) -> bool:
        somethingMoved = False
        map = [ row[:] for row in self.map ]  # deep copy the map
        # do all east first
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == ">":
                    success, map = self.moveCucumber(x, y, map)
                    somethingMoved = success or somethingMoved

        self.map = [ row[:] for row in map ]
        map = [ row[:] for row in self.map ]
        # do all south second
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == "v":
                    success, map = self.moveCucumber(x, y, map)
                    somethingMoved = success or somethingMoved
        self.map = [ row[:] for row in map ]
        return somethingMoved

sf = None
with open("input") as f:
    sf = Cucumbers(f.read())

step = 1
while True:
    if not sf.step():
        break
    step += 1

print(step)