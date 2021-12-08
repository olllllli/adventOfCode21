from typing import List


class BingoBoard:
    def __init__(self, b: str) -> None:
        self.found = [ [False for _ in range(5)] for _ in range(5)]
        self.board: List[List[int]] = []
        self.rows = [0 for _ in range(5)]
        self.cols = [0 for _ in range(5)]
        for row in b.split("\n"):
            self.board.append([ int(row[i:i+2]) for i in range(0, len(row), 3) ])
        
    def __repr__(self) -> str:
        res = "BingoBoard(\n"
        for row in range(5):
            newrow = map(lambda c: f"\033[4m{c[1]:02d}\033[0m" if self.found[row][c[0]] else f"{c[1]:02d}", enumerate(self.board[row]))
            res += " ".join(list(newrow)) + "\n"
        res += ")"
        return res

    def mark(self, num: int) -> None:
        for row in range(5):
            try: 
                col = self.board[row].index(num)
                self.found[row][col] = True
                self.rows[row] += 1
                self.cols[col] += 1
                return
            except:
                continue

    def check(self) -> bool:
        return (5 in self.rows) or (5 in self.cols)

    def score(self, num: int) -> int:
        res = 0
        for row in range(5):
            for col in range(5):
                if not self.found[row][col]:
                    res += self.board[row][col]
        return res * num


# read the file
boards: List[BingoBoard] = []
numbers = []
with open("input", "r") as f:
    inp = f.read().split("\n\n")
    numbers = inp[0].split(",")
    for board in inp[1:]:
        boards.append(BingoBoard(board))
# for board in boards: print(board)

# mark the numbers (part 1)
# for number in numbers:
#     number = int(number)
#     found = False
#     for board in boards:
#         board.mark(number)
#         if board.check():
#             print("win")
#             print(board)
#             print(board.score(number))
#             found = True
#             break
#     if found: break

# part 2 find loser
for number in numbers:
    number = int(number)
    winners = []
    for board in boards:
        board.mark(number)
        if board.check():
            winners.append(board)

    # remove the winners
    for winner in winners:
        if len(boards) == 1:
            # the loser
            print("LOSER!")
            print(winner)
            print(winner.score(number))
        boards.remove(winner)



