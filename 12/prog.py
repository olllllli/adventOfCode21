# class Stack:
#     def __init__(self) -> None:
#         self.s = []

#     def __len__(self) -> int:
#         return len(self.s)

#     def __repr__(self) -> str:
#         return str(self.s)

#     def push(self, item) -> None:
#         self.s.append(item)
    
#     def pop(self) -> Any:
#         return self.s.pop()

from typing import List, Set


class CaveSystem:
    def __init__(self, adjacencies: List[str]) -> None:
        self.caves = {}  # adjacency list
        for pair in adjacencies:
            c1, c2 = pair.split("-")
            # add the caves
            if c1 not in self.caves:
                self.caves[c1] = set()
            if c2 not in self.caves:
                self.caves[c2] = set()
            # connect the caves
            self.caves[c1].add(c2)
            self.caves[c2].add(c1)
        for cave in self.caves:
            self.caves[cave] = set(sorted(list(self.caves[cave])))

    # p1
    # def countPaths(self, curr: str, seen: List[str]) -> int:
    #     # if its already in seen, skip
    #     if curr in seen and curr.islower():
    #         return 0
        
    #     # if its the end, return 1
    #     if curr == "end":
    #         print(",".join(seen))
    #         return 1

    #     # else sum its children
    #     total = 0
    #     newSeen = [curr]
    #     newSeen.extend(seen)
    #     for neighbour in self.caves[curr]:
    #         total += self.countPaths(neighbour, newSeen)
        
    #     return total

    # p2
    def countPaths(self) -> int:
        paths = set()
        for cave in sorted(self.caves.keys()):
            if cave.islower() and cave != "start" and cave != "end":
                self.countPathsRecursive("start", [], cave, paths)

        return len(paths)

    def countPathsRecursive(self, curr: str, seen: List[str], specialSmall: str, paths: Set[str]) -> None:
        # if its already in seen, skip
        if (curr != specialSmall and curr.islower() and curr in seen) or (curr == specialSmall and seen.count(curr) >= 2):
            return
        
        # if its the end, return 1
        if curr == "end":
            # print(",".join(reversed(seen)))
            paths.add(",".join(reversed(seen)))
            return

        # else sum its children
        newSeen = [curr]
        newSeen.extend(seen)
        for neighbour in self.caves[curr]:
            self.countPathsRecursive(neighbour, newSeen, specialSmall, paths)




# read the file
adjacencies = []
with open("input") as f:
    for line in f:
        adjacencies.append(line.rstrip("\n"))

cs = CaveSystem(adjacencies)
print(cs.countPaths())