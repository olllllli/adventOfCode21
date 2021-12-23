from typing import List, Tuple


class Burrow:
    roomPositions = { "A": 3, "B": 5, "C": 7, "D": 9 }
    energyCosts = { "A": 1, "B": 10, "C": 100, "D": 1000 }
    def __init__(self, rooms: dict, hallway: List[str], startingEnergy: int) -> None:
        self.rooms = rooms
        self.hallway = hallway
        self.energySpent = startingEnergy

    # for a nice display
    def __repr__(self) -> str:
        b = [
            ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
            ['#', '#', '#', '.', '#', '.', '#', '.', '#', '.', '#', '#', '#'],
            [' ', ' ', '#', '.', '#', '.', '#', '.', '#', '.', '#', ' ', ' '],
            [' ', ' ', '#', '.', '#', '.', '#', '.', '#', '.', '#', ' ', ' '],
            [' ', ' ', '#', '.', '#', '.', '#', '.', '#', '.', '#', ' ', ' '],
            [' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ']
        ]
        for room in self.rooms:
            for level in range(len(self.rooms[room])):
                b[5 - level][self.roomPositions[room]] = self.rooms[room][level]
        for spot in range(11):
            if self.hallway[spot]:
                b[1][1 + spot] = self.hallway[spot]
        res = "\n".join(map(lambda r: "".join(r), b))
        res += f"\nEnergy Spent: {self.energySpent}"
        return res

    # converts it to a hashable, for the memoization (effectively just everything goes to a tuple)
    def toHashable(self) -> Tuple[Tuple, Tuple, Tuple, Tuple, Tuple]:
        res = []
        mapping = {None: 0, "A": 1, "B": 2, "C": 3, "D": 4}
        for room in self.rooms.values():
            copiedRoom = room[:]
            for _ in range(4 - len(copiedRoom)):
                copiedRoom.append(None)
            res.append(tuple(map(lambda a: mapping[a], copiedRoom)))

        res.append(tuple(map(lambda a: mapping[a], self.hallway)))
        return tuple(res)

    # solves the problem
    # goes through each possible move, creates a new burrow from the resultant state, and call solve on it
    # using global dictionary storing minimum for every burrow state, 
    # will return if its already been to that burrow state for less cost. 
    # Also will return of there are no possible moves, or it was solved. 
    def solve(self) -> int:
        # check whether been to this burrow for less cost
        global minimumForState
        minimumAlreadyFoundForThisState = minimumForState.get(self.toHashable())
        if minimumAlreadyFoundForThisState and self.energySpent >= minimumAlreadyFoundForThisState:
            return None  # already considered this path
        else:
            minimumForState[self.toHashable()] = self.energySpent
            # return None

        if self.checkSolved():
            # was solved, return this energy spent
            print(self)
            return self.energySpent

        possibleMoves = self.getPossibleMoves()
        if not possibleMoves:
            # there are no more legal moves, this is a deadend rabbithole
            return None

        # else find the minimum cost of a rabbithole
        minimumCost = 100000000
        for move in possibleMoves:
            if move[0] == "r":
                nextState = self.moveToRoom(move[1], move[2])
            else:
                nextState = self.moveToHallway(move[1], move[2])

            nextBurrow = Burrow(*nextState)
            nextCost = nextBurrow.solve()
            if nextCost is not None:
                minimumCost = min(minimumCost, nextCost)

        return minimumCost

    # returns whether its in a solved state
    def checkSolved(self) -> bool:
        # check each room
        for room in self.rooms:
            if len(self.rooms[room]) < 4:
                return False  # not enough in room
            elif list(filter(lambda a: a != room, self.rooms[room])):
                return False  # still a non belonger in here
        return True
    
    # returns a copy of everything needed to recreate itself
    def copyState(self) -> Tuple[dict, List[str], int]:
        roomsCopy = {}
        hallwayCopy = self.hallway[:]
        energyCopy = self.energySpent
        for room in self.rooms:
            roomsCopy[room] = self.rooms[room][:]
        return (roomsCopy, hallwayCopy, energyCopy)

    # returns every legal move, ("r" | "h", room, hallwaySpot)
    def getPossibleMoves(self) -> List[Tuple[str, str, int]]:
        res: List[Tuple[str, str, int]] = []
        # go through all the possible room to hallway moves
        for room in self.rooms:
            if not self.rooms[room]:
                continue  # room empty
            elif not list(filter(lambda a: a != room, self.rooms[room])):
                continue  # room already partially solved or fully solved (ie there are no foreigners here)
            amphi = self.rooms[room][-1]
            pos = self.roomPositions[room] - 1
            possibleSpots = [0, 1, 3, 5, 7, 9, 10]

            # go left
            for spot in range(pos, -1, -1):
                if self.hallway[spot]:
                    break  # cant go any further because a amphi in the way
                elif spot in possibleSpots:
                    res.append(("h", room, spot))
            # go right
            for spot in range(pos, 11):
                if self.hallway[spot]:
                    break
                elif spot in possibleSpots and ("h", room, spot) not in res:
                    res.append(("h", room, spot))

        # go through all possible hallway to room
        for spot in range(11):
            amphi = self.hallway[spot]
            if amphi is None or len(self.rooms[amphi]) == 4:
                continue  # skip because no amphi in this spot or their room is full
            elif list(filter(lambda a: a != amphi, self.rooms[amphi])):
                continue  # cant move into its room if there is a foreigner there still

            dest = self.roomPositions[amphi] - 1
            if spot < dest and not list(filter(None, self.hallway[spot + 1:dest + 1])):
                # needs to go right and there are no obstructions
                res.append(("r", amphi, spot))
            elif spot > dest and not list(filter(None, self.hallway[dest:spot])):
                # needs to go left and there are no obstructions
                res.append(("r", amphi, spot))
        return res

    # returns burrow state after moving from room to hallwaySpot
    def moveToHallway(self, room: str, hallwaySpot: int) -> Tuple[dict, List[str], int]:
        newRooms, newHallway, newEnergy = self.copyState()

        amphi = newRooms[room].pop()
        newHallway[hallwaySpot] = amphi

        hallwaySpaces = abs(Burrow.roomPositions[room] - (hallwaySpot + 1)) + 1
        roomExitSpaces = 4 - len(newRooms[room]) - 1
        newEnergy += (hallwaySpaces + roomExitSpaces) * Burrow.energyCosts[amphi]
        return (newRooms, newHallway, newEnergy)

    # returns burrow state after moving from hallwaySpot to room
    def moveToRoom(self, room: str, hallwaySpot: int) -> Tuple[dict, List[str], int]:
        newRooms, newHallway, newEnergy = self.copyState()

        amphi = newHallway[hallwaySpot]
        newHallway[hallwaySpot] = None
        newRooms[room].append(amphi)

        hallwaySpaces = abs(Burrow.roomPositions[room] - (hallwaySpot + 1))
        roomEntrySpaces = 4 - len(newRooms[room]) + 1
        newEnergy += (hallwaySpaces + roomEntrySpaces) * Burrow.energyCosts[amphi]
        return (newRooms, newHallway, newEnergy)

# this is scary
global minimumForState
minimumForState = {}

# read the input
b = None
with open("inputp2") as f:
    inp = f.read().split("\n")
    rooms = {}
    for room in ["A", "B", "C", "D"]:
        pos = Burrow.roomPositions[room]
        roomContents = []
        for level in range(0, 4):
            roomContents.append(inp[5 - level][pos])
        rooms[room] = roomContents
    b = Burrow(rooms, [ None for _ in range(11) ], 0)

# solve the burrow
print(b.solve())