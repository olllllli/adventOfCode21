class Reactor:
    def __init__(self) -> None:
        self.onCubes = set()
    
    def changeStateCuboid(self, state: str, ranges: str) -> None:
        xstr, ystr, zstr = ranges.split(",")
        x1, x2 = map(lambda n: int(n), xstr[2:].split(".."))
        y1, y2 = map(lambda n: int(n), ystr[2:].split(".."))
        z1, z2 = map(lambda n: int(n), zstr[2:].split(".."))

        for x in range(max(x1, -50), min(x2, 50) + 1):
            for y in range(max(y1, -50), min(y2, 50) + 1):
                for z in range(max(z1, -50), min(z2, 50) + 1):
                    if state == "on":
                        self.turnOnCube(x, y, z)
                    else:
                        self.turnOffCube(x, y, z)

    def turnOnCube(self, x: int, y: int, z: int) -> None:
        self.onCubes.add((x, y, z))

    def turnOffCube(self, x: int, y: int, z: int) -> None:
        if (x, y, z) in self.onCubes:
            self.onCubes.remove((x, y, z))

    def onCount(self, givenRange: None) -> int:
        if givenRange is None:
            return len(self.onCubes)
        else:
            (x1, x2), (y1, y2), (z1, z2) = givenRange
            return len(list(filter(lambda c: c[0] >= x1 and c[0] <= x2 and c[1] >= y1 and c[1] <= y2 and c[2] >= z1 and c[2] <= z2, self.onCubes)))

r = Reactor()
with open("input") as f:
    for line in f:
        state, givenRange = line.rstrip("\n").split(" ")
        # print(state, givenRange)
        r.changeStateCuboid(state, givenRange)

importantRange = ((-50, 50), (-50, 50), (-50, 50))
print(r.onCount(importantRange))
