# wtf this is insane
# use a tree like structure
class Packet:
    def __init__(self, binStr: str) -> None:
        self.binStr = binStr
        self.version = int(binStr[:3], 2)
        self.type = int(binStr[3:6], 2)

        if self.type == 4:  # is a literal
            self.isLiteral = True
            self.isOperator = False

            self.__value = 0
            self.size = self.__decodeLiteral()
            self.binStr = self.binStr[:self.size]  # chop off unused
        else:  # is a operator
            self.isLiteral = False
            self.isOperator = True

            self.ltid = int(binStr[6], 2)
            self.subpackets = []
            self.__decodeOperator()
            self.binStr = self.binStr[:self.size]  # chop off unused

    # get the value of the packet (will evalutate it if its an operator aswell)  p2
    @property
    def value(self) -> int:
        if self.isLiteral:
            return self.__value
        
        # wasnt a literal, go through the possible operators
        if   self.type == 0:  # sum
            return sum(list(map(lambda sp: sp.value, self.subpackets)))  # sum the subpackets values
        elif self.type == 1:  # product
            total = 1  # multiply all subpackets
            for sp in self.subpackets: 
                total *= sp.value
            return total
        elif self.type == 2:  # minimum
            return min(list(map(lambda sp: sp.value, self.subpackets)))  # minimum of the subpackets values
        elif self.type == 3:  # maximum
            return max(list(map(lambda sp: sp.value, self.subpackets)))  # minimum of the subpackets values
        elif self.type == 5:  # greater than
            return int(self.subpackets[0].value > self.subpackets[1].value)  # find whether first greater than second
        elif self.type == 6:  # less than
            return int(self.subpackets[0].value < self.subpackets[1].value)  # find whether first smaller than second
        elif self.type == 7:  # equal to
            return int(self.subpackets[0].value == self.subpackets[1].value)  # find whether first equal to second

    def __repr__(self) -> str:
        return "Packet(V: {}, T: {}, Value: {}; {})".format(self.version, self.type, self.value, self.binStr)

    # returns the index after the last useful bit to this literal
    def __decodeLiteral(self) -> int:
        literal = self.binStr[6:]
        result = ""
        i = 0
        while True:
            # add the 4 bits
            result += literal[i + 1:i + 5]
            # check if it is the final 4 bits
            if literal[i] == "0":
                break
            i += 5

        # done, convert result to value
        self.__value = int(result, 2)
        return 6 + (i + 5)

    # decodes an operators subpackets, adding them to self.subpackets
    def __decodeOperator(self) -> None:
        if self.ltid == 0:  # the length is the stored length
            subpacketsLen = int(self.binStr[7:22], 2)
            binStr = self.binStr[22:22 + subpacketsLen]  # get the relevant binstr
            while len(binStr) > 0:  # go through the binstr until its no longer
                subpacket = Packet(binStr)
                self.subpackets.append(subpacket)

                # cut off the subpackets length from the binStr
                binStr = binStr[subpacket.size:]
            self.size = 22 + subpacketsLen

        elif self.ltid == 1:  # the length is the total length of the subpackets
            subpacketCount = int(self.binStr[7:18], 2)
            numSubpackets = 0
            binStr = self.binStr[18:]
            self.size = 18
            while numSubpackets < subpacketCount:
                subpacket = Packet(binStr)
                numSubpackets += 1
                self.size += subpacket.size
                self.subpackets.append(subpacket)

                # cut off the subpackets length from the binStr
                binStr = binStr[subpacket.size:]


class MasterPacket:
    def __init__(self, hexStr: str) -> None:
        # convert it to binary string
        self.master = format(int(hexStr, 16), f"0{len(hexStr)*4}b")
        self.head = Packet(self.master)

    # debug printing
    def print(self) -> None:
        print("Master:", self.master)
        self.__printRecursion(self.head, 0)
        
    def __printRecursion(self, p: Packet, indent: int) -> None:
        if p.isLiteral:
            print(" " * ((indent - 1) * 2), "-", p)
        else:
            print(" " * ((indent - 1) * 2), "~", p)
            for sp in p.subpackets:
                self.__printRecursion(sp, indent + 2)

    # p1
    def versionSum(self) -> int:
        # sum the versions recursively
        return self.__versionSumRecursion(self.head)

    def __versionSumRecursion(self, currPacket: Packet) -> int:
        if currPacket.isLiteral:
            return currPacket.version
        elif currPacket.isOperator:
            # sum its subpackets
            total = 0
            total += currPacket.version
            for subPacket in currPacket.subpackets:
                total += self.__versionSumRecursion(subPacket)
            return total

    # p2
    def evaluate(self) -> int:
        return self.head.value

    

file = str(input("input file: "))
mp = None
with open(file) as f:
    mp = MasterPacket(f.read().rstrip("\n"))

# mp.print()
# print(mp.versionSum())  # p1

# p2
# mp.print()
print(mp.evaluate())