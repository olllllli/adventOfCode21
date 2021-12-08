# i think this is the ant question from ass1

crabs = []
with open("input") as f:
    for line in f:
        for crab in line.rstrip("\n").split(","):
            crabs.append(int(crab))

# p1
# sort the crabs
# scrabs = sorted(crabs)

# # get the middle right crab no need to remove since fuel will be 0
# middle = int(len(scrabs)/2)
# destination = scrabs[middle]

# # calculate fuel for each crab to move to middle
# totalFuel = 0
# for crab in crabs:
#     # print(f"Crab {crab} -> {destination}: {abs(crab - destination)}")
#     totalFuel += abs(crab - destination)

# print(totalFuel)

# part 2, cant use same solution, try brute force
minTotal = 100000000000000000000000000000000
bestCrab = 0
for destination in range(max(crabs) + 1):
    totalFuel = 0
    for crab in crabs:
        distance = abs(crab - destination)
        totalFuel += int(distance * ((1 + distance) / 2)) # arithmetic sum sequence
        # print(f"Crab {crab} -> {destination}: {int(distance * ((1 + distance) / 2))}")

    # print(destination, totalFuel)
    if totalFuel < minTotal:
        bestCrab = destination
        minTotal = totalFuel

print(bestCrab, minTotal)