import random
import math
import time
from typing import List, Optional, Tuple


# number of attacking queen pairs; perm is a permutation where index=column, value=row
def energy(perm: List[int]) -> int:
    n = len(perm)
    attacks = 0
    for i in range(n):
        for j in range(i + 1, n):
            # if queens are on the same diagonal
            if abs(perm[i] - perm[j]) == abs(i - j):
                attacks += 1
    return attacks


# swap two columns
def swap_positions(perm: List[int], i: int, j: int) -> None:
    perm[i], perm[j] = perm[j], perm[i]


def simulated_annealing_n_queens(n: int, max_iters: int, init_temp: float, alpha: float) -> Tuple[Optional[List[int]], int, dict]:
    # initial random permutation
    perm = list(range(n))
    random.shuffle(perm)

    current_energy = energy(perm)
    best_perm = perm.copy()
    best_energy = current_energy

    temp = init_temp
    start_time = time.time()

    for it in range(1, max_iters + 1):
        if current_energy == 0:
            print(f"Found solution at iteration {it-1}")
            break

        # neighbor is a permutation with two swaped columns
        i, j = random.sample(range(n), 2)  # choose random columns for swaping
        swap_positions(perm, i, j)
        new_energy = energy(perm)

        delta = new_energy - current_energy

        # accept if better or with probability exp(-delta/temp)
        if delta <= 0 or random.random() < math.exp(-delta / temp):
            current_energy = new_energy
            if new_energy < best_energy:
                best_energy = new_energy
                best_perm = perm.copy()
        else:
            # revert to the previous state
            swap_positions(perm, i, j)

        # cool down
        temp *= alpha
        # avoid temperature underflow to zero
        if temp < 1e-12:
            temp = 1e-12

        print(f"iter {it:7d} temp {temp:.6e} current_energy {current_energy} best {best_energy}")

    end_time = time.time()
    elapsed = end_time - start_time

    solution = best_perm if best_energy == 0 else None
    stats = {
        "iterations": it,
        "elapsed_time": elapsed,
        "best_energy": best_energy,
        "final_temp": temp
    }

    return solution, best_energy, stats


def print_board(perm: List[int]) -> None:
    n = len(perm)
    board = [["."]*n for _ in range(n)]
    for col, row in enumerate(perm):
        board[row][col] = "Q"
    print("\n".join(" ".join(r) for r in board))


if __name__ == "__main__":
    N = int(input("Enter the number of queens: "))
    max_iters = 200000
    init_temp = 1.0  # initial temperature
    alpha = 0.9995  # coefficient for cooling the temperature

    sol, e, stats = simulated_annealing_n_queens(N, max_iters, init_temp, alpha)

    if sol is not None:
        print(f"\nSolution for N={N} (energy={e}):")
        print_board(sol)
    else:
        print(f"\nNo exact solution found for N={N}. Best energy: {e}")
        print("\nStats:", stats)
