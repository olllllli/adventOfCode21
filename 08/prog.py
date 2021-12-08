from typing import List, Set

# uniquely identifies the mapping for each number
def getMapping(input: List[Set[str]]) -> dict:
    # create the map
    mapping = dict([ (i, set()) for i in range(10) ])

    # sort the input by size
    # and uniquely identify the 1, 4, 7, 8
    size5 = []
    size6 = []
    for item in input:
        if   len(item) == 2: mapping[1] = item
        elif len(item) == 3: mapping[7] = item
        elif len(item) == 4: mapping[4] = item
        elif len(item) == 5: size5.append(item)
        elif len(item) == 6: size6.append(item)
        elif len(item) == 7: mapping[8] = item

    # identify 3
    mapping[3] = list(filter(lambda n: len(n.union(mapping[1])) == 5, size5))[0]  # |size5 UNION {1}| == 5
    size5.remove(mapping[3])
    # identify 2
    mapping[2] = list(filter(lambda n: len(n.union(mapping[4])) == 7, size5))[0]  # |size5 UNION {4}| == 7
    size5.remove(mapping[2])
    # identify 5
    mapping[5] = size5[0] # left over size 5

    # identify 6
    mapping[6] = list(filter(lambda n: len(n.union(mapping[7])) == 7, size6))[0]  # |size6 UNION {7}| == 7
    size6.remove(mapping[6])
    # identify 9
    mapping[9] = list(filter(lambda n: len(n - mapping[3]) == 1, size6))[0]  # |size6 - {3}| == 1
    size6.remove(mapping[9])
    # identify 0
    mapping[0] = size6[0]

    return mapping

# translates a set into its number
def translate(mapping: dict, digit: Set[str]) -> int:
    for num in mapping:
        if mapping[num] == digit:
            return num


    
# p1
# counts = [ 0 for _ in range(10) ]
# p2
results = []
with open("input") as f:
    for line in f:
        inp, out = line.rstrip("\n").split(" | ")
        mapping = getMapping(list(map(lambda n: set(n), inp.split(" "))))

        # p1
        # for digit in out.split(" "):
        #     counts[translate(mapping, set(digit))] += 1

        # p2
        result = 0
        digits = list(map(lambda n: set(n), out.split(" ")))
        
        # translate each digit
        result += translate(mapping, digits[0]) * 1000
        result += translate(mapping, digits[1]) * 100
        result += translate(mapping, digits[2]) * 10
        result += translate(mapping, digits[3]) * 1
        results.append(result)

# p1
# for i in range(10):
#     print(f"{i}: {counts[i]}")

# p2
print(sum(results))
