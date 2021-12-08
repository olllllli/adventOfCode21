from typing import List
import math


class LanternSchool:
    def __init__(self, initial: List[int]):
        # self.fish = list(map(lambda n: int(n), initial))
        self.fishCounts = [0 for _ in range(9)]
        for fish in initial:
            self.fishCounts[int(fish)] += 1

    def __repr__(self) -> str:
        return f"LanternSchool({self.fishCounts})"

    # p1
    # def nextDay(self):
    #     for i in range(len(self.fish)):
    #         if self.fish[i] == 0:
    #             self.fish[i] = 6
    #             self.fish.append(8)
    #         else:
    #             self.fish[i] -= 1

    # def nextWeek(self):
    #     for i in range(len(self.fish)):
    #         if self.fish[i] < 7:
    #             reproduceDay = self.fish[i]
    #             self.fish.append(8 - (6 - reproduceDay))
    #         else:
    #             self.fish[i] -= 7

    # p2
    def nextDay(self):
        # just shuffle the counts down, and ofcourse add all the 0 fishes onto 8
        fishies0 = self.fishCounts[0]
        for day in range(8):
            self.fishCounts[day] = self.fishCounts[day + 1]
        self.fishCounts[8] = fishies0
        self.fishCounts[6] += fishies0

    def nextWeek(self):
        # first store count of all the non breeders
        fishies8 = self.fishCounts[8] # -> fishies1
        fishies7 = self.fishCounts[7] # -> fishies0
        self.fishCounts[8] = 0
        self.fishCounts[7] = 0

        # now reproduce all the others
        for day in range(7):
            # day 0 -> 0, but add a fish that will be on 8 - (6 - 0)
            newFishies = self.fishCounts[day]
            self.fishCounts[8 - (6 - day)] += newFishies

        # now add back the non breeders in their new age
        self.fishCounts[1] = fishies8
        self.fishCounts[0] = fishies7
    
    @property
    def size(self) -> int:
        # return len(self.fish)
        return sum(self.fishCounts)

fishies: LanternSchool = None
with open("input") as f:
    for line in f:
        fishies = LanternSchool(line.strip("\n").split(","))


days = 256
day = 0
for _ in range(days):
    print(f"After Day {day}: {fishies.size}")
    print(fishies)
    fishies.nextDay()
    day += 1

# for _ in range(math.floor(days / 7)):
#     print(f"After Day {day}: {fishies.size}")
#     # print(fishies)
#     fishies.nextWeek()
#     day += 7

# for _ in range(days % 7):
#     # print(f"After Day {day}: {fishies.size}")
#     # print(fishies)
#     fishies.nextDay()
#     day += 1

print(fishies.size)
