from typing import List, Tuple


class Burrow:
    roomPositions = { "A": 3, "B": 5, "C": 7, "D": 9 }
    energyCosts = { "A": 1, "B": 10, "C": 100, "D": 1000 }
    def __init__(self, rooms: dict, hallway: List[str], startingEnergy: int) -> None:
        self.rooms = rooms
        self.hallway = hallway
        self.energySpent = startingEnergy

    def __repr__(self) -> str:
        b = [
            ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
            ['#', '#', '#', '.', '#', '.', '#', '.', '#', '.', '#', '#', '#'],
            [' ', ' ', '#', '.', '#', '.', '#', '.', '#', '.', '#', ' ', ' '],
            [' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ']
        ]
        for room in self.rooms:
            if len(self.rooms[room]) == 2:
                b[3][self.roomPositions[room]] = self.rooms[room][0]
                b[2][self.roomPositions[room]] = self.rooms[room][1]
            elif len(self.rooms[room]) == 1:
                b[3][self.roomPositions[room]] = self.rooms[room][0]
        for spot in range(11):
            if self.hallway[spot]:
                b[1][1 + spot] = self.hallway[spot]
        res = "\n".join(map(lambda r: "".join(r), b))
        res += f"\nEnergy Spent: {self.energySpent}"
        return res

    def toHashable(self) -> Tuple[Tuple, Tuple, Tuple, Tuple, Tuple]:
        res = []
        mapping = {None: 0, 0: 0, "A": 1, "B": 2, "C": 3, "D": 4}
        for room in self.rooms.values():
            if len(room) == 0:  room = [0, 0]
            elif len(room) == 1: room = room + [0]
            res.append(tuple(map(lambda a: mapping[a], room)))

        res.append(tuple(map(lambda a: mapping[a], self.hallway)))
        return tuple(res)

    def solve(self) -> int:
        global minimumForState
        minimumAlreadyFoundForThisState = minimumForState.get(self.toHashable())
        if minimumAlreadyFoundForThisState and self.energySpent >= minimumAlreadyFoundForThisState:
            return None  # already considered this path
        else:
            minimumForState[self.toHashable()] = self.energySpent
            # return None

        if self.checkSolved():
            print(self)
            # was solved, return this energy spent
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

    def checkSolved(self) -> bool:
        # bottom row
        bottomScore = 0
        topScore = 0
        for room in self.rooms:
            if len(self.rooms[room]) >= 1:
                bottomScore += int(self.rooms[room][0] == room)
            if len(self.rooms[room]) == 2:
                topScore += int(self.rooms[room][1] == room)
        self.bottomSolved = (bottomScore == 4)
        self.topSolved = (topScore == 4)
        return self.bottomSolved and self.topSolved
    
    # returns a copy of everything needed to recreate itself
    def copyState(self) -> Tuple[dict, List[str], int]:
        roomsCopy = {}
        hallwayCopy = self.hallway[:]
        energyCopy = self.energySpent
        for room in self.rooms:
            roomsCopy[room] = self.rooms[room][:]
        return (roomsCopy, hallwayCopy, energyCopy)

    def getPossibleMoves(self) -> List[Tuple[str, str, int]]:
        res: List[Tuple[str, str, int]] = []
        # go through all the possible room to hallway moves
        for room in self.rooms:
            if len(self.rooms[room]) == 0:
                continue  # room empty
            elif len(self.rooms[room]) == 1 and self.rooms[room][0] == room:
                continue  # room already partially solved
            elif len(self.rooms[room]) == 2 and self.rooms[room][0] == room and self.rooms[room][1] == room:
                continue  # room already solved
            amphi = self.rooms[room][-1]
            pos = self.roomPositions[room] - 1
            possibleSpots = [0, 1, 3, 5, 7, 9, 10] # + [self.roomPositions[amphi] - 1]
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
            if amphi is None or len(self.rooms[amphi]) == 2:
                continue  # skip because no amphi in this spot or their room is full
            elif len(self.rooms[amphi]) == 1 and self.rooms[amphi][0] != amphi:
                continue  # cant move into its room if there is a foreigner there still

            dest = self.roomPositions[amphi] - 1
            if spot == dest:  # if its ontop its destination
                res.append(("r", amphi, spot))
            elif spot < dest and not list(filter(None, self.hallway[spot + 1:dest + 1])):
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
        roomExitSpaces = 2 - len(newRooms[room]) - 1
        newEnergy += (hallwaySpaces + roomExitSpaces) * Burrow.energyCosts[amphi]
        return (newRooms, newHallway, newEnergy)

    # returns burrow state after moving from hallwaySpot to room
    def moveToRoom(self, room: str, hallwaySpot: int) -> Tuple[dict, List[str], int]:
        newRooms, newHallway, newEnergy = self.copyState()
        amphi = newHallway[hallwaySpot]
        newHallway[hallwaySpot] = None
        newRooms[room].append(amphi)

        hallwaySpaces = abs(Burrow.roomPositions[room] - (hallwaySpot + 1))
        roomEntrySpaces = 2 - len(newRooms[room]) + 1
        newEnergy += (hallwaySpaces + roomEntrySpaces) * Burrow.energyCosts[amphi]
        return (newRooms, newHallway, newEnergy)

global minimumForState
minimumForState = {}

b = None
with open("input") as f:
    inp = f.read().split("\n")
    rooms = {}
    for room in ["A", "B", "C", "D"]:
        pos = Burrow.roomPositions[room]
        rooms[room] = [inp[3][pos], inp[2][pos]]
    b = Burrow(rooms, [ None for _ in range(11) ], 0)

print(b.solve())
# print(minimumForState)