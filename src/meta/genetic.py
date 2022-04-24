from math import floor
from time import time
from typing import List
import random
from utils.routing import Router
from utils.genetic import get_initial_pop, inverse_diff_to_max, inverse_diff_to_min, selection_ga
from utils.crossover import SA_crossover, crossover, singlepoint_crossover
from utils.solution import check_solution
from utils.neighbourhood import neighbour_hill_climb_single_car, neighbour_single_car, remove_end_nodes, remove_multiple_nodes, add_multiple_nodes, random_growth

class GeneticSolver:
    def __init__(self, problem_info: Router, max_gen: int):
        self._problem_info = problem_info
        self._max_gen = max_gen
        self._pop_size = len(
            problem_info.graph.streets) // problem_info.num_cars // 3
        self._min_pop_size = 100
        self._queen_ratio = 0.85
        self._crossover_function = [singlepoint_crossover]
        self._mutation_chance = 0.6
        self._poll_rate = 100
        self.meta = True
        self.meta_its = 2
        self.mutation_functions = [remove_end_nodes, random_growth, add_multiple_nodes, remove_multiple_nodes]
        self.meta_functions = [random_growth, add_multiple_nodes, remove_multiple_nodes]

    def set_poll_rate(self, poll_rate):
        self._poll_rate = poll_rate

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
    poll_rate = property(fset=set_poll_rate)

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
        gen_tick = 0
        x = []
        y = []
        y_worst = []

        init_time = time()
        while(self._max_gen > generations):
            if(generations % self._poll_rate == 0):
                print(time() - init_time)
                print(evals[best_eval])
                x.append(gen_tick)
                y.append(evals[best_eval])
                y_worst.append(evals[self.get_worst_eval(evals)])
                gen_tick += 1

            generations += 1
            [parent1, parent2] = selection_ga(
                evals, population, lambda val: inverse_diff_to_max(evals[best_eval], val))

            child = crossover(population[parent1], population[parent2],
                              self._problem_info.graph, self._crossover_function)

            random_value = random.uniform(0, 1)

            if random_value < self._mutation_chance:
                child = neighbour_single_car(child, self._problem_info, 0.0, self.mutation_functions)

            if self.meta:
                for _ in range(self.meta_its):
                    child = neighbour_hill_climb_single_car(child, self._problem_info, 0.0, self.meta_functions)

            removed_member = selection_ga(
                evals, population, lambda val: inverse_diff_to_min(min(evals), val))[0]
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