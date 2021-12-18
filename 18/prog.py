import math
from typing import Any, Tuple

class SnailfishNumber:
    def __init__(self, num: str) -> None:
        # check whether its a normal number or not
        if "[" in num:
            num = num[1:-1]
            comma = self.__findMiddle(num)
            self.left = SnailfishNumber(num[:comma])
            self.right = SnailfishNumber(num[comma + 1:])
            self.isRegular = False
        else:
            self.isRegular = True
            self.value = int(num)

    # debug
    def display(self, depth=0) -> None:
        if self.isRegular:
            print("  " * depth, f"-{self.value}")
        else:
            self.right.display(depth + 1)
            print("  " * depth, "~G")
            self.left.display(depth + 1)

    # reduce the number
    def reduce(self) -> None:
        while True:
            # check if there is an explosive sfn
            explosive = self.findExplosive()
            if explosive:
                # find where to place its values
                _, closestRight = self.findClosestOnRight(explosive, False)
                _, closestLeft = self.findClosestOnLeft(explosive, False)
                if closestRight is not None:
                    closestRight.value += explosive.right.value
                if closestLeft is not None:
                    closestLeft.value += explosive.left.value

                # now delete the explosive one
                del explosive.left
                del explosive.right
                explosive.isRegular = True
                explosive.value = 0
                continue
            else:
                # no explosive pair, now check if theres a splitable regular
                splitted = self.findSplittable()
                if not splitted:
                    # neither a explosive pair or splittable regular, break
                    break

    # finds an explosive sfn, and returns it, or None if none were found
    def findExplosive(self, depth=0) -> Any:
        if self.isRegular:  # shouldnt ever really be the case
            return None

        # check whether we have reached the problem pair
        if self.left.isRegular and self.right.isRegular:
            if depth >= 4:
                return self
            else:
                # there is no explosive pair
                return None

        # figure out which branch you want to go down
        # btw favour left
        lHeight = self.left.height
        rHeight = self.right.height
        if lHeight >= rHeight:
            return self.left.findExplosive(depth + 1)
        else:
            return self.right.findExplosive(depth + 1)

    # gets the regular straight after the regular of the explosive
    # returns (seenExplosive, SnailfishNumber | None)
    def findClosestOnRight(self, explosive, seenExplosive: bool) -> Tuple[bool, Any]:
        # go left to right
        if not self.isRegular:  # check if its in either branch
            seenExplosive, found = self.left.findClosestOnRight(explosive, seenExplosive)
            if found is not None:
                return (seenExplosive, found)
    
            seenExplosive, found = self.right.findClosestOnRight(explosive, seenExplosive)
            if found is not None:
                return (seenExplosive, found)

        # wasnt a regular, or wasnt in either branch, check if current regular is the solution
        if self.isRegular and seenExplosive:
            # will be the first regular after seen explosive
            return (seenExplosive, self)

        # check whether this might be the explosive
        if self == explosive:
            seenExplosive = True

        # wasnt regular or hadnt seen explosive
        return (seenExplosive, None)

    # gets the regular straight before the regular of the explosive
    # returns (seenExplosive, SnailfishNumber | None)
    def findClosestOnLeft(self, explosive, seenExplosive: bool) -> Tuple[bool, Any]:
        # go right to left
        if not self.isRegular:  # check if its in either branch
            seenExplosive, found = self.right.findClosestOnLeft(explosive, seenExplosive)
            if found is not None:
                return (seenExplosive, found)

            seenExplosive, found = self.left.findClosestOnLeft(explosive, seenExplosive)
            if found is not None:
                return (seenExplosive, found)

        # wasnt a regular, or wasnt in either branch, check if current regular is the solution
        if self.isRegular and seenExplosive:
            # will be the first regular after seen explosive
            return (seenExplosive, self)

        # check whether this might be the explosive
        if self == explosive:
            seenExplosive = True

        # wasnt regular or hadnt seen explosive
        return (seenExplosive, None)

    # finds the first splittable and splits it
    # returns True if found, False if not
    def findSplittable(self) -> bool:
        if self.isRegular and self.value > 9:
            # must be the first
            left = math.floor(self.value / 2)
            right = math.ceil(self.value / 2)
            
            # delete all this sfn regular attributes
            self.isRegular = False
            del self.value

            # create the new sfn from this
            self.left = SnailfishNumber(str(left))
            self.right = SnailfishNumber(str(right))
            return True
        elif self.isRegular and self.value <= 9:
            return False  # not splittable
        
        # now go left first
        if self.left.findSplittable():
            # has already found a splittable
            return True
        else:
            # now go right, if this returns False then there was no splittable on the right either
            return self.right.findSplittable()

    # other methods
    @property
    def height(self) -> int:
        if self.isRegular:
            return 0
        else:
            return max(self.left.height, self.right.height) + 1

    @property
    def magnitude(self) -> int:
        if self.isRegular:
            return self.value
        else:
            return (3 * self.left.magnitude) + (2 * self.right.magnitude)

    # returns the string version
    def __str__(self) -> str:
        if self.isRegular:
            return str(self.value)
        else:
            return f"[{str(self.left)},{str(self.right)}]"

    # overload addition
    def __add__(self, other) -> Any:
        result = SnailfishNumber(f"[{str(self)},{str(other)}]")
        result.reduce()
        return result

    # finds the index of the main seperator comma
    def __findMiddle(self, num: str) -> int:
        brackets = 0
        for i in range(len(num)):
            c = num[i]
            if c == "[":
                brackets += 1
            elif c == "]":
                brackets -= 1
            elif c == "," and brackets == 0:
                return i
        # wasnt found, raise exception
        raise ValueError("No seperating comma at base level")


# actual main loop
# sfn = None  # p1
sfns = []  # p2
with open("input") as f:
    for line in f:
        # if sfn is None:  # p1
        #     sfn = SnailfishNumber(line.rstrip("\n"))
        # else:
        #     sfn += SnailfishNumber(line.rstrip("\n"))
        sfns.append(SnailfishNumber(line.rstrip("\n")))  # p2

# print(str(sfn))
# print(sfn.magnitude)  # p1

# p2
largestM = 0
for sfn1 in sfns:
    for sfn2 in sfns:
        if sfn1 == sfn2:
            continue
        magnitude = (sfn1 + sfn2).magnitude
        largestM = max(largestM, magnitude)

print(largestM)