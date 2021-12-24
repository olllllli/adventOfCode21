from typing import Dict, List, Set, Tuple


class ALU:
    def __init__(self) -> None:
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0

    @property
    def state(self) -> Tuple:
        return (self.w, self.x, self.y, self.z)
    
    def get(self, var: str) -> int:
        if var.isnumeric() or var[1:].isnumeric():
            return int(var)
        elif var == "w":
            return self.w
        elif var == "x":
            return self.x
        elif var == "y":
            return self.y
        elif var == "z":
            return self.z

    def set(self, var: str, value: int) -> int:
        value = int(value)
        if var == "w":
            self.w = value
        elif var == "x":
            self.x = value
        elif var == "y":
            self.y = value
        elif var == "z":
            self.z = value

    def execute(self, instruction: str) -> None:
        operators = {"add": self.add, "mul": self.mul, "div": self.div, "mod": self.mod, "eql": self.eql}
        operator, op1, op2 = instruction.split(" ")
        if operator not in operators:
            return
        
        op2 = self.get(op2)
        operators[operator](op1, op2)

    def add(self, op1: str, op2: int) -> None:
        res = self.get(op1) + op2
        self.set(op1, res)

    def mul(self, op1: str, op2: int) -> None:
        res = self.get(op1) * op2
        self.set(op1, res)
    
    def div(self, op1: str, op2: int) -> None:
        res = int(self.get(op1) / op2)
        self.set(op1, res)
    
    def mod(self, op1: str, op2: int) -> None:
        res = self.get(op1) % op2
        self.set(op1, res)
    
    def eql(self, op1: str, op2: int) -> None:
        res = self.get(op1) == op2
        self.set(op1, res)



class MONADProgram:
    def __init__(self, instructions: List[str]) -> None:
        self.inst = instructions
        self.blocks = []
        currBlock = []
        for i in self.inst:
            if "inp" in i:
                self.blocks.append(currBlock)
                currBlock = []
            currBlock.append(i)
        self.blocks.append(currBlock)
        self.blocks = self.blocks[1:]

    # finds the largest input that results in a z = 0
    def solve(self) -> List:
        newStates = {(0, 0, 0, 0): ""}
        # find all the possible states before block 10
        for block in range(10):
            oldStates = newStates
            newStates = {}
            for state in oldStates:
                nextStates = self.possibleStates(oldStates[state], state, block)
                newStates.update(nextStates)

        # calculate all the valid z values that could go into a block that will eventually result in 0
        block = 13
        validZIntoBlock = {}
        ztargetRange = {0}
        while block >= 10:
            res = self.findWorkingZValues(range(0, 26**(14-block)), block, ztargetRange)
            validZIntoBlock[block] = res
            ztargetRange = res
            block -= 1

        # continue with the possible states for each block, but only allowing a next state if its a valid z
        # this will control the possible states from exploding largely
        for block in range(10, 14):
            oldStates = newStates
            newStates = {}
            for state in oldStates:
                if state[3] not in validZIntoBlock[block]:
                    continue
                nextStates = self.possibleStates(oldStates[state], state, block)  
                newStates.update(nextStates)                  

        # after all blocks have been done, filter the states out which have z = 0
        res = list(filter(lambda n: n[0][3] == 0, list(newStates.items())))
        return res

    # returns all possible states after a certain block is executed
    def possibleStates(self, numberSoFar: str, sState: Tuple, block: int) -> Dict:
        states = {}
        # for w in range(1, 10):  # p1
        for w in range(9, 0, -1):  # p2
            state = self.executeBlock(sState, w, block)
            # reset w and x and y in the state to help with recursion size, since it gets reset next block anyway
            state = (0, 0, 0, state[3])
            states[state] = numberSoFar + str(w)
        return states

    # returns a set of z values and their corresponding w value going into this block, 
    # which result in a final z value in targetRange
    def findWorkingZValues(self, zrange: range, block: int, targetRange: Set) -> Set:
        res = set()
        for z in zrange:
            for w in range(1, 10):
                thisResult = self.executeBlock((0, 0, 0, z), w, block)
                if thisResult[3] in targetRange:
                    res.add(z)
        return res
    
    # executes a block
    def executeBlock(self, sState: Tuple, w: int, block: int) -> Tuple:
        alu = self.setupALU(sState)
        alu.w = w
        for instruction in self.blocks[block][1:]:
            alu.execute(instruction)
        return alu.state

    # determine the common instructions per block, 
    # good for figuring out how the algorithm should be solved
    def findCommon(self) -> list:
        commonInstructions = set(enumerate(self.blocks[0]))
        for block in self.blocks[1:]:
            commonInstructions = commonInstructions.intersection(set(enumerate(block)))
        return commonInstructions

    # simplify blocks to pythonic logical statements
    # good for figuring out how the algorithm should be solved
    def simplifyBlocks(self) -> None:
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            inst4 = block[4].split(" ")
            inst5 = block[5].split(" ")
            inst15 = block[15].split(" ")
            # blockStr = f"z = (((prevz / {inst4[2]}) * ((25 * ((((prevz % 26) + {inst5[2]}) == w) == 0)) + 1)) + ((w + {inst15[2]}) * ((((prevz % 26) + {inst5[2]}) == w) == 0)))"
            blockStr = f"((prevz / {inst4[2]}) * (26 if ((prevz % 26) + {inst5[2]} != w) else 1))  +  ((w + {inst15[2]}) if ((prevz % 26) + {inst5[2]} != w) else 0)"
            print(i, blockStr)

    # sets up an alu from a state
    def setupALU(self, state: Tuple) -> ALU:
        alu = ALU()
        alu.w, alu.x, alu.y, alu.z = state 
        return alu

    # runs the instructions with the given input, expects atleast enough inputs
    def execute(self, input: List[int]) -> Tuple:
        alu = ALU()
        inp = 0
        for i in self.inst:
            if "inp" in i:
                op = i.split(" ")[1]
                alu.set(op, input[inp])
                inp += 1
            else:
                alu.execute(i)
        return alu.state

p = None

with open("input") as f:
    instructions = f.read().split("\n")
    p = MONADProgram(instructions)

sol = p.solve()
print(sol)


"""
Solution, all be it horrible:
- The program can be broken down 14 blocks, one for each input. 
  Notice, these blocks are the same except for instruction 5, 6, 16
  in which they have different constants as their second operands. 

- Also notice that only z gets carried over to the next block, 
  w, x and y get over written as 0 or input, before being used in that block.

- From this, we can attack the problem with brute force in two directions, 
    1.  Go forward, block by block, test all 9 inputs for that block, and find every possible
        z value after the block, starting with the z value from the previous block. 
        Then test all these possible z values for the next block. 
        The issue here is the possible z values after the 10th digit, start ballooning to 7 digits or more. 
    2   Go backwards, block by block, noting that we want the final block to end with z = 0. 
        From this, we can get a tight range of 13..21 for the valid z values going into the final block,
        that will result in a final z = 0. 
        Apply this same logic to the 13th block then, we need all posisble z values going in, 
        which result in a z value between 13 and 21 going out. 
        Repeat this going up the blocks. 
        The issue here is that it becomes difficult to find this range, and using a loose but proven
        range also explodes to 7 digits. 

- Hence we use method 2 to find all the valid z values from digit 10 onwards, 
- Then use method 1, and once we get to the 10th digit, only check states which are valid. 
- This means we peak at about 700k possible states at the 10th digit, and get worked back down to 9 possible states at the 14th. 
"""

