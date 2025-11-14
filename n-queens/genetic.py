import random
import time
from typing import List, Tuple

# get the number of non-attacking pairs
def fitness(individual: List[int]) -> int:
    n = len(individual)
    attacks = 0
    for i in range(n):
        for j in range(i + 1, n):
            # if queens are on the same diagonal or in the same row
            if abs(individual[i] - individual[j]) == abs(i - j) or individual[i] == individual[j]:
                attacks += 1
    max_pairs = n * (n - 1) // 2
    return max_pairs - attacks

# generate population without repetiting values in the same individual (no queens in the same row)
def initial_population(pop_size: int, n: int) -> List[List[int]]:
    pop = []  # population
    base = list(range(n))
    for _ in range(pop_size):
        ind = base[:]  # individual
        random.shuffle(ind)
        pop.append(ind)
    return pop

# select individual with best fitness among k random individuals
def tournament_selection(pop: List[List[int]], fits: List[int], k: int = 3) -> List[int]:
    selected_idx = random.sample(range(len(pop)), k)
    selected_idx.sort(key=lambda i: fits[i], reverse=True)
    return pop[selected_idx[0]][:]

def crossover(parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
    n = len(parent1)
    cross_point = random.randrange(1, n)
    child1 = parent1[:cross_point] + parent2[cross_point:]
    child2 = parent2[:cross_point] + parent1[cross_point:]
    return child1, child2

def mutation(ind: List[int], mutation_rate: float) -> None:
    if random.random() < mutation_rate:
        n = len(ind)
        i = random.randrange(n)  # position to mutate
        new_pos = random.randrange(n)
        # new value should not be the same as previous
        while new_pos == i:
            new_pos = random.randrange(n)
        ind[i] = new_pos

# make new population using crossovers and mutations
def evolve(pop: List[List[int]], pop_size: int, mutation_rate: float, tournament_k: int) -> List[List[int]]:
    fits = [fitness(ind) for ind in pop]
    new_pop = []
    # keep best individual
    best_idx = max(range(len(pop)), key=lambda i: fits[i])
    best_ind = pop[best_idx][:]
    new_pop.append(best_ind)
    while len(new_pop) < pop_size:
        p1 = tournament_selection(pop, fits, tournament_k)
        p2 = tournament_selection(pop, fits, tournament_k)
        c1, c2 = crossover(p1, p2)
        mutation(c1, mutation_rate)
        mutation(c2, mutation_rate)
        new_pop.append(c1)
        if len(new_pop) < pop_size:
            new_pop.append(c2)
    return new_pop

# if solution is not found, the returned value is the best found
def ga_solve(n: int,
             pop_size: int = 200,
             mutation_rate: float = 0.3,
             tournament_k: int = 3,
             max_generations: int = 1000,
             verbose: bool = False) -> Tuple[List[int], int, int]:
    pop = initial_population(pop_size, n)
    max_fit = n * (n - 1) // 2
    start = time.time()
    for gen in range(1, max_generations + 1):
        fits = [fitness(ind) for ind in pop]
        best_idx = max(range(len(pop)), key=lambda i: fits[i])
        best_fit = fits[best_idx]
        best_ind = pop[best_idx][:]
        if gen % 50 == 0 and verbose:
            print(f"Gen {gen:4d} best fitness {best_fit}/{max_fit}")
        if best_fit == max_fit:
            print(f"SOLVED in generation {gen} (time {time.time()-start:.2f}s)")
            return best_ind, gen, best_fit
        pop = evolve(pop, pop_size, mutation_rate, tournament_k)
    # finished without perfect solution, return best found
    fits = [fitness(ind) for ind in pop]
    best_idx = max(range(len(pop)), key=lambda i: fits[i])
    best_fit = fits[best_idx]
    best_ind = pop[best_idx][:]
    if verbose:
        print(f"Finished {max_generations} generations. Best fitness {best_fit}/{max_fit} (time {time.time()-start:.2f}s)")
    return best_ind, max_generations, best_fit

def print_board(solution: List[int]) -> None:
    n = len(solution)
    board = [["."]*n for _ in range(n)]
    for col, row in enumerate(solution):
        board[row][col] = "Q"
    print("\n".join(" ".join(r) for r in board))

if __name__ == "__main__":
    N = int(input("Enter the number of queens: "))
    POP_SIZE = 200  # population size
    MUT_RATE = 0.3  # probability for mutation
    TOURN_K = 3  # size of selection for the tournament
    MAX_GEN = 1000  # maximum number of generations

    solution, generation, fit = ga_solve(N, POP_SIZE, MUT_RATE, TOURN_K, MAX_GEN, True)
    print("\nSolution (column:row indices):")
    print(list(enumerate(solution)))
    print("\nBoard:")
    print_board(solution)
