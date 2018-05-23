from unittest import TestCase
from GeneticAlgo import Population
from GeneticAlgo import Individual

class TestPopulation(TestCase):
    def test_pick_individual(self):
        my_population = Population(population_size=25, individual_size=9, fitness_function='compute_test_fitness')
        self.assertEqual(len(my_population.population), 25)
        self.assertEqual(len(my_population.population.get().get_genome()), 9)
        picked_individual = my_population.pick_individual()
        self.assertTrue(isinstance(picked_individual,Individual))

        my_other_population = Population(population_size=2, individual_size=7, fitness_function='compute_fitness')
        self.assertEqual(len(my_other_population.population), 2)
        self.assertEqual(len(my_other_population.population.get().get_genome()), 7)
        picked_individual = my_other_population.pick_individual()
        self.assertTrue(isinstance(picked_individual, Individual))

    def test_get_best_individual(self):
        my_population = Population(population_size=25, individual_size=9, fitness_function='compute_test_fitness')
        found_best = my_population.get_best_individual()
        best_individual = None
        best_fitness = 0
        for individual in my_population.population.queue:
            if individual.fitness > best_fitness:
                best_individual = individual
        self.assertEqual(found_best,best_individual)


    def test_genetic_algorithm(self):
        my_population = Population(population_size=100, individual_size=7, fitness_function='compute_test_fitness')

        best_guy = my_population.genetic_algorithm(threshold= 2 * 9999000)
        self.assertTrue(best_guy.fitness >= 2 * 9999000, str(best_guy.fitness))

    def test_real_genetic_algorithm(self):
        my_population = Population(population_size=4, individual_size=7, fitness_function='compute_fitness')
        best_guy = my_population.genetic_algorithm(threshold=1024)
        self.assertTrue(best_guy.fitness >= 1024, str(best_guy.fitness))

