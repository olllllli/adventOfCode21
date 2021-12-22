from __future__ import annotations
from typing import List, Tuple

# represent a 3d polyhedron, starts off as a simple rectanglular prism
class Polyhedron:
    def __init__(self, state: str, xrange: Tuple[int, int], yrange: Tuple[int, int], zrange: Tuple[int, int]) -> None:
        self.x1, self.x2 = xrange  # only relevant for simple Polyhedrons, also relevant when adding a simple polyhedron to this
        self.y1, self.y2 = yrange
        self.z1, self.z2 = zrange
        self.state = 1 if state == "on" else 0  # relevant only if simple
        self.subPolys: List[Polyhedron] = []

    def __repr__(self) -> str:
        if self.isSimple:
            return f"Polyhedron(({self.x1},{self.y1},{self.z1}), ({self.x2},{self.y2},{self.z2}): {self.state})"
        return "Polyhedron()"

    @property
    def isSimple(self) -> bool:
        return not self.subPolys

    @property
    def onCubes(self) -> int:
        if self.isSimple:
            if self.state == 1:
                return (abs(self.x2 - self.x1) + 1) * (abs(self.y2 - self.y1) + 1) * (abs(self.z2 - self.z1) + 1)
            else:
                return 0
        else:
            total = 0
            for sub in self.subPolys:
                total += sub.onCubes
            return total

    # turns off a range by subdividing or turning itself off
    def turnOff(self, xrange: Tuple[int, int], yrange: Tuple[int, int], zrange: Tuple[int, int]) -> None:
        if not self.overlaps(xrange, yrange, zrange):
            return  # skip because it doesnt even overlap

        # isnt simple, goto each subpoly instead
        if not self.isSimple:
            for sub in self.subPolys:
                sub.turnOff(xrange, yrange, zrange)
            return

        # if it was entirely encompassed, just keep it simple and turn off (this protects from infinite recursion)
        if self.x1 >= xrange[0] and self.x2 <= xrange[1] and self.y1 >= yrange[0] and self.y2 <= yrange[1] and self.z1 >= zrange[0] and self.z2 <= zrange[1]:
            self.state = 0
            return
        
        # it is a simple shape and has overlap. Then, for each axis, there are three ways it can overlap
        # either: range entirely inside self, range entirely encompasses self, range is abit in and hangs abit out
        # divide it on these overlaps, and create on subpolys for every subdivide,
        # then pass over again and turn off using the range, this will make sure the ones which need to be off will be
        xsubdivides = self.__subdivide((self.x1, self.x2), xrange)
        ysubdivides = self.__subdivide((self.y1, self.y2), yrange)
        zsubdivides = self.__subdivide((self.z1, self.z2), zrange)
        for xsub in xsubdivides:
            for ysub in ysubdivides:
                for zsub in zsubdivides:
                    # create a polyhedron for this subdivide
                    self.subPolys.append(Polyhedron("on", xsub, ysub, zsub))

        # now turn off the necessary subpolygon
        for sub in self.subPolys:
            sub.turnOff(xrange, yrange, zrange)

    # turns on a range
    def turnOn(self, xrange: Tuple[int, int], yrange: Tuple[int, int], zrange: Tuple[int, int]) -> None:
        # turn off the overlapping part, so the lights dont get counted twice
        self.turnOff(xrange, yrange, zrange)
        # then create a new simple poly for the on range
        self.subPolys.append(Polyhedron("on", xrange, yrange, zrange))

    # assumes it overlaps in some way, doesnt overhang 
    def __subdivide(self, range1: Tuple[int, int], range2: Tuple[int, int]) -> List[Tuple[int, int]]:
        # double check it overlaps
        if range2[1] < range1[0] or range2[0] > range1[1]:
            return []

        if range1[0] < range2[0] and range1[1] > range2[1]:
            # range2 starts in middle of range1 and ends in middle of range1, return 3 different ranges then
            return [ (range1[0], range2[0] - 1), (range2[0], range2[1]), (range2[1] + 1, range1[1]) ]
        elif range1[0] < range2[0] and range1[1] <= range2[1]:
            # range2 starts in middle of range1 and ends on or to the right, return 2 different ranges
            return [ (range1[0], range2[0] - 1), (range2[0], range1[1]) ]
        elif range1[0] >= range2[0] and range1[1] > range2[1]:
            # range2 starts left of or on range1, and ends inside range1, return 2 different ranges, no overhang
            return [ (range1[0], range2[1]), (range2[1] + 1, range1[1]) ]
        elif range1[0] >= range2[0] and range1[1] <= range2[1]:
            # range2 starts and finishes outside or on of range1, just return range1 so no overhang
            return [ range1 ]
        else:
            # unsure what could cause this and dont really care to find out
            return []

    def overlaps(self, xrange: Tuple[int, int], yrange: Tuple[int, int], zrange: Tuple[int, int]) -> bool:
        if self.state == 0 and self.isSimple:  # off state and simple, never overlaps
            return False
        elif self.isSimple:
            xNotOverlap = xrange[1] < self.x1 or xrange[0] > self.x2
            yNotOverlap = yrange[1] < self.y1 or yrange[0] > self.y2
            zNotOverlap = zrange[1] < self.z1 or zrange[0] > self.z2
            if xNotOverlap or yNotOverlap or zNotOverlap:
                return False  # one of the axis dont overlap so the whole shape doesnt overlap
            else:
                return True
        else:
            # go through all its subPolys
            for sub in self.subPolys:
                if sub.overlaps(xrange, yrange, zrange):
                    return True
            return False


class Reactor:
    def __init__(self) -> None:
        self.mainPoly = None
    
    def changeState(self, state: str, ranges: str) -> None:
        xstr, ystr, zstr = ranges.split(",")
        x1, x2 = map(lambda n: int(n), xstr[2:].split(".."))
        y1, y2 = map(lambda n: int(n), ystr[2:].split(".."))
        z1, z2 = map(lambda n: int(n), zstr[2:].split(".."))

        if self.mainPoly is None:
            self.mainPoly = Polyhedron(state, (x1, x2), (y1, y2), (z1, z2))
        else:
            if state == "on":
                self.mainPoly.turnOn((x1, x2), (y1, y2), (z1, z2))
            else:
                self.mainPoly.turnOff((x1, x2), (y1, y2), (z1, z2))

    def onCount(self) -> int:
        # removed p1 logic 
        # before just had a set of points and would count between the -50 and 50 range
        # addition and subtraction would just remove and add points, very slow very bad
        return self.mainPoly.onCubes


r = Reactor()
with open("input") as f:
    for line in f:
        state, givenRange = line.rstrip("\n").split(" ")
        r.changeState(state, givenRange)

print(r.onCount())
