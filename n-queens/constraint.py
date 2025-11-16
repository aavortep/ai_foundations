from typing import List
import time


def constraint_solve(n: int) -> List[List[int]]:
    # 1 queen per row, domain is the set of valid columns for each queen
    domains = {row: set(range(n)) for row in range(n)}
    solutions = []

    # check constraints for the specific placement
    def is_consistent(assignment: dict, row: int, col: int) -> bool:
        for r, c in assignment.items():
            # if it's the same column or the same diagonal
            if c == col or abs(row - r) == abs(col - c):
                return False
        return True

    # propagate constraints after placing queen at (row, col)
    def forward_check(domains: dict, row: int, col: int) -> dict:
        new_domains = {r: set(cols) for r, cols in domains.items()}
        for r in range(row + 1, n):
            # remove the same column from domains
            if col in new_domains[r]:
                new_domains[r].remove(col)
            diag1 = col + (r - row)
            diag2 = col - (r - row)
            # remove the same diagonals from domains
            if diag1 in new_domains[r]:
                new_domains[r].remove(diag1)
            if diag2 in new_domains[r]:
                new_domains[r].remove(diag2)
            # if domain becomes empty, propagation fails
            if not new_domains[r]:
                return None
        return new_domains

    def backtrack(assignment: dict, domains: dict, row: int) -> None:
        if row == n:  # found valid complete assignment
            solutions.append([assignment[r] for r in range(n)])
            return
        for col in sorted(domains[row]):
            # check current assignment's consistency with each column from current domain of given row
            if is_consistent(assignment, row, col):
                # if it's consistent, remove from next domains inconsistent values
                new_domains = forward_check(domains, row, col)
                # if domains are empty, terminate this branch and choose another consistent column
                if new_domains is not None:
                    # otherwise fix this column value and go to the next row
                    assignment[row] = col
                    backtrack(assignment, new_domains, row + 1)
                    # clear assignment to start over again
                    del assignment[row]
                    if len(solutions) == 1:
                        break

    backtrack({}, domains, 0)
    return solutions


def print_board(solution: List[int]) -> None:
    n = len(solution)
    board = [["."]*n for _ in range(n)]
    for col, row in enumerate(solution):
        board[row][col] = "Q"
    print("\n".join(" ".join(r) for r in board))


if __name__ == "__main__":
    n = int(input("Enter the number of queens: "))

    start = time.time()
    sols = constraint_solve(n)
    end = time.time() - start

    print("\nFound solution:\n")
    print_board(sols[0])
    print(f"\nTime: {end} s")
