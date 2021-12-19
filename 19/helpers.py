from __future__ import annotations
from typing import Dict, List, Set, Tuple

# finds all node in a component, and its distance to those nodes
def findComponent(curr: int, adjDict: Dict[int, List[int]], visitted: Dict[int, int], dist: int) -> Dict[int, int]:
    if curr in visitted:
        return visitted

    visitted[curr] = dist

    for adj in adjDict[curr]:
        if adj in visitted:
            continue
        visitted.update(findComponent(adj, adjDict, visitted, dist + 1))

    return visitted
    
# beacon
class Beacon:
    def __init__(self, c: Tuple[int, int, int]) -> None:
        self.x = int(c[0])
        self.y = int(c[1])
        self.z = int(c[2])

    def __getitem__(self, key: int | str):
        if key == 0 or key == "x": return self.x
        if key == 1 or key == "y": return self.y
        if key == 2 or key == "z": return self.z

    def __setitem__(self, key: int | str, value: int):
        if key == 0 or key == "x": self.x = value
        if key == 1 or key == "y": self.y = value
        if key == 2 or key == "z": self.z = value

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __repr__(self):
        return f"Beacon({self.x},{self.y},{self.z})"

    # remaps a beacons coordinates to a different orientation relative to ('+x', '+y', '+z')
    def remap(self, targetOrientation: Tuple[str, str, str]) -> Tuple[int, int, int]:
        result = Beacon((0, 0, 0))
        for i in range(3):
            value = self[i]
            mapping = targetOrientation[i]
            if   mapping[0] == "-":  result[mapping[1]] = -value
            elif mapping[0] == "+":  result[mapping[1]] = value
        return result

    # subtract two beacons
    def __sub__(self, other: Beacon) -> Tuple[int, int, int]:
        return (self.x - other.x, self.y - other.y, self.z - other.z)

# scanner
class Scanner:
    possOrientations = set([
        ('+x', '-z', '+y'), ('+x', '+y', '+z'), ('+x', '+z', '-y'), ('+x', '-y', '-z'), 
        ('+y', '+z', '+x'), ('+y', '-x', '+z'), ('+y', '-z', '-x'), ('+y', '+x', '-z'), 
        ('+z', '-y', '+x'), ('+z', '+x', '+y'), ('+z', '+y', '-x'), ('+z', '-x', '-y'), 

        ('-x', '+z', '+y'), ('-x', '-y', '+z'), ('-x', '-z', '-y'), ('-x', '+y', '-z'), 
        ('-y', '-z', '+x'), ('-y', '+x', '+z'), ('-y', '+z', '-x'), ('-y', '-x', '-z'),
        ('-z', '+y', '+x'), ('-z', '-x', '+y'), ('-z', '-y', '-x'), ('-z', '+x', '-y')
    ])

    def __init__(self, id: int, beacons: List[str]) -> None:
        self.id = id
        self.beacons: List[Beacon] = []
        for b in beacons:
            self.beacons.append(Beacon(tuple(b.split(","))))

    def __repr__(self) -> str:
        return f"Scanner(id: {self.id})"

    # remaps all the beacons to a new orientation, relative to +x +y +z
    def remap(self, targetOrientation: Tuple[str, str, str]) -> List[Tuple[str, str, str]]:
        remapped = []
        for b in self.beacons:
            remapped.append(b.remap(targetOrientation))
        return remapped

    # assuming self is +x +y +z, returns relative position of other and relative orientation, if enough overlapping beacons
    def overlapping(self, other: Scanner) -> Tuple[Tuple[int, int, int], Tuple[str, str, str]]:
        for o in Scanner.possOrientations:
            otherRemapped = other.remap(o)
            possiblePositions = {}
            for selfBeacon in self.beacons:
                for otherBeacon in otherRemapped:
                    # calculate the candidate position of other if you were to overlap the two beacons
                    pos = selfBeacon - otherBeacon
                    if pos not in possiblePositions:
                        possiblePositions[pos] = 0
                    possiblePositions[pos] += 1

            # check if there was a possible offset position that had >= 12 overlapping beacons
            for pos in possiblePositions:
                if possiblePositions[pos] >= 12:
                    return (pos, o)
        return None