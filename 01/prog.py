inp = []
with open("input") as f:
    for line in f:
        inp.append(int(line.rstrip("\n")))

# p1
# print(len(list(filter(lambda b: b, list(map(lambda x: inp[x[0] - 1] <= x[1], list(enumerate(inp))[1:]))))))

# p2
print(len(list(filter(lambda b: b, list(map(lambda x: sum(inp[x[0] - 1:x[0] + 2]) < sum(inp[x[0]:x[0] + 3]), list(enumerate(inp))[1:-2]))))))