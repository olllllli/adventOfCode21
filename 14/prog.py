from typing import List

class Polymerizer:
    def __init__(self, template: str, rules: List[str]) -> None:
        self.rules = {}
        self.letters = {}
        for rule in rules:
            pair, result = rule.split(" -> ")
            # store count of each pair for p2, and the resultant pairs
            self.rules[pair] = [result, 0, (pair[0] + result, result + pair[1])]
        
        # count the amount of pairs in the initial template
        for i in range(len(template) - 1):
            pair = template[i] + template[i + 1]
            if self.rules.get(pair):
                self.rules[pair][1] += 1

        # count the amount of letters in initial template
        letterCounts = []
        for letter in set(list(template)):
            letterCounts.append((letter, list(template).count(letter)))
        self.letters = dict(letterCounts)

    # p1 neive solution
    # def __str__(self) -> str:
    #     return "".join(list(map(lambda t: t[0], self.template)))

    # def step(self):
    #     new = self.template
    #     # go through the letters
    #     i = 0
    #     while i < len(new) - 1:
    #         # check if the pair starting at i is a insertion rule
    #         pair = new[i] + new[i + 1]
    #         if pair in self.rules:
    #             # insert it and increase i to skip over the inserted one
    #             new.insert(i + 1, self.rules[pair])
    #             i += 1
    #         i += 1
    #     self.template = new

    # p2 superior solution
    # since insertion between a pair doesn't effect other pairs, 
    # only need to know counts of each pair and the counts of the letters
    def step(self):
        pairDeltas = dict(list(map(lambda p: (p, 0), self.rules.keys())))
        for pair in self.rules:
            oldCount = self.rules[pair][1]

            # subtract the old amount of that pair
            pairDeltas[pair] -= oldCount

            # add the old amount of that pair to the two resultant pairs
            lResult = self.rules[pair][2][0]
            rResult = self.rules[pair][2][1]
            pairDeltas[lResult] += oldCount
            pairDeltas[rResult] += oldCount

            # add the old amount to the count of the inserted letter
            insertedLetter = self.rules[pair][0]
            if insertedLetter not in self.letters:
                self.letters[insertedLetter] = 0
            self.letters[insertedLetter] += oldCount
        
        # add all the deltas
        for pair in self.rules:
            self.rules[pair][1] += pairDeltas[pair]

            






template = None
rules = []
with open("input") as f:
    inp = f.read().split("\n")
    template = inp[0]
    rules = inp[2:]

# do the steps
steps = 40
p = Polymerizer(template, rules)
for i in range(steps):
    print(i)
    p.step()

# count the occurances of each p1
# letters = []
# for letter in set(p.template):
#     letters.append(p.template.count(letter))
# letters.sort()

# count occurances p2
letters = list(p.letters.values())
letters.sort()

# subtract smallest from largest
print(letters[-1] - letters[0])
