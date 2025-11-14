import time
import matplotlib.pyplot as plt
from genetic import ga_solve
from constraint import constraint_solve
from annealing import anneal_solve


ga_sizes = [8, 12, 16, 20, 30, 40, 50]
sa_sizes = [8, 12, 16, 20, 30, 40, 50, 100, 200, 300]
constr_sizes = [8, 12, 16, 20, 25, 28]
times_constr = []
times_sa = []
times_ga = []
repeat = 5

for n in constr_sizes:
    sum_time = 0
    for i in range(repeat):
        start = time.time()
        constraint_solve(n)
        sum_time += (time.time() - start)
    times_constr.append(sum_time / repeat)

for n in sa_sizes:
    sum_time = 0
    for i in range(repeat):
        start = time.time()
        anneal_solve(n)
        sum_time += (time.time() - start)
    times_sa.append(sum_time / repeat)

for n in ga_sizes:
    sum_time = 0
    for i in range(repeat):
        start = time.time()
        ga_solve(n)
        sum_time += (time.time() - start)
    times_ga.append(sum_time / repeat)

# --- Plot ---
plt.figure(figsize=(10, 6))
plt.plot(constr_sizes, times_constr, label="Constraint propagation")
plt.plot(sa_sizes, times_sa, label="Simulated Annealing")
plt.plot(ga_sizes, times_ga, label="Genetic Algorithm")
plt.xlabel("Board size N")
plt.ylabel("Time (seconds)")
plt.title("N-Queens Performance Comparison")
plt.legend()
plt.grid(True)
plt.show()
