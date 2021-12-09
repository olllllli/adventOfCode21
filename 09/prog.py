from typing import List, Mapping, MutableMapping, Set, Tuple


class Terrain:
    def __init__(self, inp: str) -> None:
        self.map = []
        for row in inp.split("\n"):
            cells = list(row)
            self.map.append(list(map(lambda n: int(n), cells)))
        self.rows = len(self.map)
        self.cols = len(self.map[0])

    def lowPoints(self) -> List[Tuple[int, int, int]]:
        rows = self.rows
        cols = self.cols
        res = []
        for y in range(rows):
            for x in range(cols):
                val = self.map[y][x]
                # check all directions
                notLowPoint = (
                    (x > 0 and self.map[y][x - 1] <= val)
                    or (x < (cols - 1) and self.map[y][x + 1] <= val)
                    or (y > 0 and self.map[y - 1][x] <= val)
                    or (y < (rows - 1) and self.map[y + 1][x] <= val)
                )
                if not notLowPoint:
                    res.append((x, y, val))
        return res

    def basins(self) -> MutableMapping[Tuple[int, int, int], Set[Tuple[int, int]]]: 
        b = {}
        for lp in self.lowPoints():
            seen = set()
            b[lp] = self.createBasin((lp[0], lp[1]), None, seen)
        return b

    def createBasin(self, pos: Tuple[int, int], oldpos: Tuple[int, int], seen: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        # check if the current pos isnt 9, or isnt outside the map, also check its a lower value than before
        x, y = pos
        if x < 0 or y < 0 or x >= self.cols or y >= self.rows:
            return []
        elif self.map[y][x] == 9:
            return []
        elif oldpos is not None and self.map[y][x] < self.map[oldpos[1]][oldpos[0]]:
            return []
        elif (x, y) in seen:
            return []

        # else amalgamate each direction
        seen.add((x, y))
        result = {(x, y)}
        result = result.union(self.createBasin((x, y - 1), pos, seen))  # N
        result = result.union(self.createBasin((x, y + 1), pos, seen))  # S
        result = result.union(self.createBasin((x + 1, y), pos, seen))  # E
        result = result.union(self.createBasin((x - 1, y), pos, seen))  # W
        return result


t: Terrain = None
with open("input") as f:
    t = Terrain(f.read())

# p1
# print(t.lowPoints())
# print(sum(list(map(lambda n: n[2] + 1, t.lowPoints()))))

# p2
basins = t.basins()
# display the basins
# for b in basins:
#     print(b)
#     for y in range(t.rows):
#         curr = []
#         for x in range(t.cols):
#             curr.append('x') if (x, y) in basins[b] else curr.append(str(t.map[y][x]))
#         print("".join(curr))
#     print("")
l = list(basins.items())
l.sort(key=lambda n: len(n[1]), reverse=True)
res = 1
for b in l[0:3]:
    print(b[0], len(b[1]), b[1])
    res *= len(b[1])

print(res)
