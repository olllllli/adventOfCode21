


# read the file
from typing import List


inp: List[str] = []
with open("input") as f:
    inp = f.read().split("\n")

def p1(inp: List[str]) -> int:
    mostcommon: bool = []
    for bit in range(len(inp[0])):
        o = 0
        z = 0
        for num in inp:
            if num[bit] == "1": o += 1
            else: z += 1
        mostcommon.append("1" if o > z else "0")

    gamma = "".join(mostcommon)
    epsilon = "".join(list(map(lambda n: str((int(n) + 1) % 2), mostcommon)))

    return int(gamma, 2) * int(epsilon, 2)


def mostCommon(l: List[str], bit: int) -> str:
    b1 = 0
    b0 = 0
    for num in l:
        if num[bit] == "1": b1 += 1
        else: b0 += 1
    return ("1" if b1 >= b0 else "0")

def p2(inp: List[str]) -> int:
    oxy = inp
    co2 = inp

    for bit in range(len(inp[0])):
        # for oxy
        if len(oxy) > 1:
            mc = mostCommon(oxy, bit)
            oxy = list(filter(lambda n: True if n[bit] == mc else False, oxy))

        # for co2
        if len(co2) > 1:
            lc = str((int(mostCommon(co2, bit)) + 1) % 2)
            co2 = list(filter(lambda n: True if n[bit] == lc else False, co2))
    
    return int(oxy[0], 2) * int(co2[0], 2)
        


print(p2(inp))
