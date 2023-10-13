import random

# Set random seed
random.seed(42)

Individual = list
Population = list[Individual]

class Item:
    def __init__(self, value, weight) -> None:
        self.value = value
        self.weight = weight

class Knapsack:

    def __init__(self, items: list[Item], capacity: int, iterations: int, num_population: int) -> None:
        self.items: Item = items
        self.capacity = capacity
        self.total_value = 0
        self.best_individual: Individual = []
        self.iterations = iterations
        self.num_population = num_population
        self.n = len(items)

    def solve(self) -> Population:
        initial_population = self.generate_initial_population()
        print(f'Initial population: {initial_population}')
        eval_initial_population = [(individual, self.fitness(individual)) for individual in initial_population]
        i = 0
        while i < self.iterations:
            print(f'Iteration {i}')
            parent1, parent2 = self.selection(eval_initial_population)
            child = self.crossover(parent1, parent2)
            child = self.mutation(child)
            eval_initial_population = self.select_new_population(eval_initial_population, child)
            print("\tNew population:")
            for sublist in eval_initial_population:
                print("\t\t", sublist)
            i += 1
        self.total_value = eval_initial_population[0][1]
        self.best_individual = eval_initial_population[0][0]
        self.print_solution()
        
    def generate_initial_population(self) -> Population:
        def generate_individual() -> Individual:
            individual = []
            for _ in range(self.n):
                individual.append(random.randint(0, 1))
            return individual

        return [generate_individual() for _ in range(self.num_population)]
    
    def selection(self, population: Population) -> Individual:
        selected = random.sample(population, 2)
        print(f'\tSelected: {selected}')
        return selected[0][0], selected[1][0]

    def crossover(self, parent1: Individual, parent2: Individual) -> Individual:
        point = random.randint(0, self.n)
        child = parent1[:point] + parent2[point:]
        print(f'\tPoint: {point}')
        print(f'\tChild: {child}')
        return child
    
    def mutation(self, individual: Individual) -> Individual:
        prob = 0.1
        for i in range(self.n):
            if random.random() <= prob:
                individual[i] = 1 - individual[i]
        print(f'\tMutated: {individual}')
        return individual
    
    def fitness(self, individual: Individual) -> int:
        value = 0
        weight = 0
        for i in range(self.n):
            if individual[i] == 1:
                value += self.items[i].value
                weight += self.items[i].weight
        if weight > self.capacity:
            return 0
        else:
            return value

    def select_new_population(self, new_population: Population, child: Individual) -> Population:
        new_population.append((child, self.fitness(child)))
        new_population.sort(key=lambda x: x[1], reverse=True)
        new_population = new_population[:self.num_population]
        print(f'\tDescarted: {new_population[-1]}')
        print(f'\tFitness: {new_population[0][1]}')
        return new_population
    
    def print_solution(self) -> None:
        print(f'Total value: {self.total_value}')
        print(f'Best individual: {self.best_individual}')
        print(f'Weigth: {sum([self.items[i].weight for i in range(self.n) if self.best_individual[i] == 1])}/{self.capacity}')


# values = [
#     360, 83, 59, 130, 431, 67, 230, 52, 93, 125, 670, 892, 600, 38, 48, 147,
#     78, 256, 63, 17, 120, 164, 432, 35, 92, 110, 22, 42, 50, 323, 514, 28,
#     87, 73, 78, 15, 26, 78, 210, 36, 85, 189, 274, 43, 33, 10, 19, 389, 276,
#     312
# ]

# weights = [
#     7, 0, 30, 22, 80, 94, 11, 81, 70, 64, 59, 18, 0, 36, 3, 8, 15, 42, 9, 0,
#     42, 47, 52, 32, 26, 48, 55, 6, 29, 84, 2, 4, 18, 56, 7, 29, 93, 44, 71,
#     3, 86, 66, 31, 65, 0, 79, 20, 65, 52, 13
# ]
values = [
    4, 2, 2, 1, 10
]
weights = [
    12, 1, 2, 1, 4
]

items = [Item(values[i], weights[i]) for i in range(len(values))]

knapsack = Knapsack(items=items, capacity=10, iterations=100, num_population=10)
knapsack.solve()