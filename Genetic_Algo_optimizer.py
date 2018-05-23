from GeneticAlgo import Population
import cProfile

### launch test
#my_population = cProfile.run('Population(population_size=50, individual_size=7, fitness_function=\'compute_fitness\')', 'restats')
my_population = Population(population_size=50, individual_size=8, fitness_function='compute_fitness')
best_guy = my_population.genetic_algorithm(threshold=2048)

print(best_guy)
