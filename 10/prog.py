# bracket stack, a stack that keeps the bracket behaviour
from typing import List


class Stacket:
    parenth = {"(": ")", "[": "]", "{": "}", "<": ">"}
    openers = list(parenth.keys())
    closers = list(parenth.values())

    def __init__(self) -> None:
        self.stack = []

    def __repr__(self) -> str:
        return f"Stacket( \"{','.join(self.stack)}\" )"
    
    def push(self, item) -> str:
        if item in self.openers:
            self.stack.append(item)
            return None
        elif item in self.closers:
            # check if closes the most recent opener
            recentOpener = self.stack[-1]
            if self.parenth[recentOpener] != item:
                # doesnt
                return self.parenth[recentOpener]
            else:
                # does
                self.stack.pop()
                return None

    def getClosing(self) -> List[str]:
        rev = reversed(self.stack)
        return list(map(lambda n: self.parenth[n], rev))

# points = {")": 3, "]": 57, "}": 1197, ">": 25137}  # p1
# total = 0  # p1
scores = []  # p2
points = {")": 1, "]": 2, "}": 3, ">": 4}  # p2

with open("input") as f:
    # go through each line
    for line in f:
        bs = Stacket()
        corrupt = False
        # go through each parenthesis
        for parenth in list(line.rstrip("\n")):
            success = bs.push(parenth)
            # check if it wasnt valid
            if success is not None:
                # total += points[parenth]  # p1
                corrupt = True
                break
        
        # check if it was corrupt
        if corrupt: 
            continue  # skip

        # else calculate the score of the remaining closers (p2)
        score = 0
        closers = bs.getClosing()
        for closer in closers:
            score *= 5
            score += points[closer]
        scores.append(score)

# print(total)  # p1

# p2
scores.sort()
median = scores[len(scores) // 2]
print(median)