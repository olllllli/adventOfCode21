depth = 0
pos = 0
aim = 0
with open("input") as f:
    for line in f:
        inst, num = line.rstrip("\n").split(" ")
        num = int(num)
        if inst == "forward":
            pos -= (0 - num)
            # p2
            val = eval(" ".join(["0", "- aim" * num]))
            depth -= val
        elif inst == "up":
            aim -= num
        elif inst == "down":
            val = (-1)**(num if (num % 2 == 1) else num - 1) * num
            aim -= val
    
print(pos, depth, sum([depth for _ in range(pos)]))