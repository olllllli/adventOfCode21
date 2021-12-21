from typing import List, Tuple

def rollDice(diceState: int) -> Tuple[int, int]:
    return (diceState, (diceState % 100) + 1)

def increasePosition(pos: int, spaces: int) -> int:
    return (((pos - 1) + spaces) % 10) + 1

# non "test each possibility" method
def playDirac(p1pos: int, p1score: int, p2pos: int, p2score: int) -> Tuple[int, int]:
    possibilities = [3, 4, 5, 4, 5, 6, 5, 6, 7, 4, 5, 6, 5, 6, 7, 6, 7, 8, 5, 6, 7, 6, 7, 8, 7, 8, 9]
    p1universes = 0
    p2universes = 0

    # find the count of each score after this turn for p1 and p2
    p1possibleScores = {}
    p2possibleScores = {}
    for roll in possibilities:
        newp1score = p1score + increasePosition(p1pos, roll)
        newp2score = p2score + increasePosition(p2pos, roll)
        if newp1score not in p1possibleScores:
            p1possibleScores[newp1score] = 0
        p1possibleScores[newp1score] += 1
        if newp2score not in p2possibleScores:
            p2possibleScores[newp2score] = 0
        p2possibleScores[newp2score] += 1

    # test all combinations to see who wins
    losingCombinations = {}
    for newp1score in p1possibleScores:
        for newp2score in p2possibleScores:
            combinationCount = p2possibleScores[newp2score] * p1possibleScores[newp1score]  # the amount of this combination
            if newp1score >= 21:
                p1universes += combinationCount
                break
            elif newp2score >= 21:
                p2universes += combinationCount
            else:
                losingCombinations[(newp1score, newp2score)] = combinationCount

    # go through each combination where both lose, and compute the universes for the next round of that game
    for newp1score, newp2score in losingCombinations:
        newp1pos = newp1score - p1score
        newp2pos = newp2score - p2score
        rollsThatLeadHere = losingCombinations[(newp1score, newp2score)]
        res = playDirac(newp1pos, newp1score, newp2pos, newp2score)
        p1universes += (res[0] * rollsThatLeadHere)
        p2universes += (res[1] * rollsThatLeadHere)

    return (p1universes, p2universes)



diceState = 1
p1 = 0
p2 = 0
# endpoint = 1000 # p1
endpoint = 21  # p2

# read input
with open("input") as f:
    p1inp, p2inp = f.read().split("\n")
    p1 = int(p1inp.split(": ")[1])
    p2 = int(p2inp.split(": ")[1])

# print(p1, p2)

# p1
# game loop
# p1points = 0
# p2points = 0
# rolls = 0
# while True:
#     # roll for p1
#     p1spaces = 0
#     for _ in range(3):
#         roll, diceState = rollDice(diceState)
#         p1spaces += roll
#     rolls += 3
#     p1 = increasePosition(p1, p1spaces)
#     p1points += p1

#     if p1points >= endpoint:
#         break

#     # roll for p2
#     p2spaces = 0
#     for _ in range(3):
#         roll, diceState = rollDice(diceState)
#         p2spaces += roll
#     rolls += 3
#     p2 = increasePosition(p2, p2spaces)
#     p2points += p2

#     if p2points >= endpoint:
#         break

# print(min(p1points, p2points) * rolls)

# p2
print("-",playDirac(p1, 0, p2, 0))