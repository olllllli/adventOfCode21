from typing import List, Tuple
import math


def decreaseMagnitute(n: int) -> int:
    if n > 0:
        return n - 1
    elif n < 0:
        return n + 1
    else:
        return n

class ProbeTrajectorySolver:
    # targetarea like "target area: x=20..30, y=-10..-5"
    def __init__(self, targetarea: str) -> None:
        targetx, targety = targetarea[13:].split(", ")
        targetx = targetx[2:].split("..")
        targety = targety[2:].split("..")
        # extract the target bounds
        self.x1 = int(targetx[0])
        self.x2 = int(targetx[1])
        self.y1 = int(targety[0])
        self.y2 = int(targety[1])
        self.calculatedTrajectories = []

    def __repr__(self) -> str:
        return f"PTS(Target: ({self.x1}, {self.y1}), ({self.x2}, {self.y2}))"

    def getTrajectories(self) -> List[Tuple[int, int]]:
        # get the testing ranges, so we can brute force within bounds
        # find the minimum x value (2x1 <= minx(1 + minx))  (solved for minx by wolfram alpha)
        minx = math.ceil(0.5 * (math.sqrt((8 * self.x1) + 1) - 1))
        # since any positive y will touch 0 again, test up to abs(self.y1), since after that itll skip entirely
        for y in range(self.y1, abs(self.y1) + 1):
            for x in range(minx, self.x2 + 1):  # test for all x values
                if self.testTrajectory(x, y)[0]:
                    self.calculatedTrajectories.append((x, y))

        return self.calculatedTrajectories

    # returns whether it landed in, and also the max y and max x it reached
    def testTrajectory(self, dx: int, dy: int) -> Tuple[bool, int, int]:
        x = 0
        y = 0
        maxX = -1000000
        maxY = -1000000
        
        # iterate through the steps
        onTarget = False
        while x <= self.x2 and y >= self.y1:  # while not beyond the box
            maxX = max(x, maxX)
            maxY = max(y, maxY)
            if self.inTarget(x, y):
                onTarget = True
                break
            # else move the probe to its next position
            x += dx
            y += dy
            dx = decreaseMagnitute(dx)
            dy -= 1

        return (onTarget, maxX, maxY)

    # check whether inside target
    def inTarget(self, x: int, y: int) -> bool:
        return x >= self.x1 and x <= self.x2 and y >= self.y1 and y <= self.y2

    # p1
    def highestTrajectory(self):
        maxY = -10000000
        for x, y in self.calculatedTrajectories:
            maxY = max(self.testTrajectory(x, y)[2], maxY)

        return maxY


pts = None
with open("input") as f:
    pts = ProbeTrajectorySolver(f.read())

print(pts)
traj = pts.getTrajectories()
print(pts.highestTrajectory())  # p1
print(len(set(traj)))  # p2