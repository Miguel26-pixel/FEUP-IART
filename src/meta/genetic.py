from math import floor
from time import time
from typing import List
import random
from utils.routing import Router
from utils.genetic import get_initial_pop, inverse_diff_to_max, log_diff_to_max, selection_ga
from utils.crossover import SA_crossover, crossover
from utils.solution import check_solution
from utils.neighbourhood import neighbour_single_car

class GeneticSolver:
    def __init__(self, problem_info: Router, run_time: int):
        self._problem_info = problem_info
        self._run_time = run_time
        self._pop_size = len(
            problem_info.graph.streets) // problem_info.num_cars // 100
        self._min_pop_size = 100
        self._queen_ratio = 0.4
        self._run_time = run_time
        self._crossover_function = SA_crossover
        self._mutation_chance = 0.2

    def set_pop_size(self, pop_size):
        self._pop_size = pop_size

    def set_min_pop_size(self, min_size):
        self._min_pop_size = min_size

    def set_queen_ratio(self, queen_ratio):
        self._queen_ratio = queen_ratio

    def set_crossover_function(self, crossover_function):
        self._crossover_function = crossover_function

    def set_mutation_chance(self, mutation_chance):
        self._mutation_chance = mutation_chance

    pop_size = property(fset=set_pop_size)
    min_pop_size = property(fset=set_min_pop_size)
    queen_ratio = property(fset=set_queen_ratio)
    crossover_function = property(fset=set_crossover_function)
    mutation_chance = property(fset=set_mutation_chance)

    def get_evals(self, population: List[List[List[int]]]):
        evals = []

        for member in population:
            _, val = check_solution(self._problem_info, member)

            evals.append(val)

        return evals

    def get_best_eval(self, evals: List[int]):
        idx_best = 0
        for idx, val in enumerate(evals):
            if val > evals[idx_best]:
                idx_best = idx

        return idx_best

    def get_worst_eval(self, evals: List[int]):
        idx_worst = 0
        for idx, val in enumerate(evals):
            if val < evals[idx_worst]:
                idx_worst = idx

        return idx_worst

    def genetic_loop(self, population: List[List[List[int]]]):
        evals = self.get_evals(population)
        best_eval = self.get_best_eval(evals)
        generations = 0
        x = [0.5]
        y = [evals[best_eval]]
        y_worst = [evals[self.get_worst_eval(evals)]]

        init_time = time()
        while(time() - init_time < self._run_time):
            if(generations % 100 == 0):
                print(time() - init_time)
                print(evals[best_eval])
                x.append(x[-1]+1)
                y.append(evals[best_eval])
                y_worst.append(evals[self.get_worst_eval(evals)])

            generations += 1
            [parent1, parent2] = selection_ga(
                evals, population, lambda val: inverse_diff_to_max(evals[best_eval], val))

            child = crossover(parent1, parent2,
                              self._problem_info.graph, self._crossover_function)

            random_value = random.uniform(0, 1)

            if random_value < self._mutation_chance:
                child = neighbour_single_car(child, self._problem_info.graph, 0.0)

            removed_member = self.get_worst_eval(evals)
            population[removed_member] = child
            _, evals[removed_member] = check_solution(
                self._problem_info, child)

            if removed_member == best_eval:
                best_eval = self.get_best_eval(evals)
            elif evals[removed_member] > evals[best_eval]:
                best_eval = removed_member
        print(f"DONE! in {time() - init_time} with {generations} generations")

        return evals[best_eval], x, y, y_worst

    def solve(self):
        n_streets = len(self._problem_info.graph.streets)
        queen_num = floor(self._pop_size * self._queen_ratio)

        print("Generating Population...")

        start_time = time()
        population = get_initial_pop(self._problem_info, max(
            self._pop_size, self._min_pop_size), queen_num, n_streets * 2, self._problem_info.time_itinerary * 1.2)

        print(f"Population generated in {time() - start_time} seconds!")

        return self.genetic_loop(population)

# 1290121
# 1354018