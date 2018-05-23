import random
import collections
from tester import Tester_For_2048
from multiprocessing.dummy import Pool as ThreadPool
from operator import methodcaller


# Priority queue implementation
class Random_queue:
    def __init__(self):
        self.queue = []
        self.item_dict = []  # this entry contains the possible values an item covers
        self.total_priority = 0
        self.highest_priority = 0
        self.best_individual = None

    def push(self, priority, state):
        # each item is made up solely of the 'state' value
        insertion_spot = len(self.queue)
        self.queue.append(state)
        self.item_dict.append([self.total_priority, self.total_priority + priority, insertion_spot])
        self.total_priority += priority
        if priority > self.highest_priority:
            self.best_individual = state
            self.highest_priority = priority

    def get(self):
        # randomly picking an element, but uses the priority to set odds of picking each
        pick = random.randint(0, self.total_priority)
        for item in self.item_dict:
            if pick in range(item[0],item[1]):
                item_to_return = self.queue[item[2]]
                return item_to_return

    def __len__(self):
        return len(self.queue)


class Test_Algo:
    def __init__(self):
        self.base_value = 2

    def unit_fitness(self, individual):
        multiplier = int(individual.get_genome())
        return self.base_value * multiplier


class Individual(object):
    def __init__(self, genome):
        self.genome = genome
        self.fitness = 0

    def get_genome(self):
        mateable_genome = ''
        for gene in self.genome:
            mateable_genome += str(gene)
        return mateable_genome

    def set_fitness(self, fitness):
        self.fitness = fitness

    def compute_test_fitness(self):
        test = Test_Algo()
        self.fitness = test.unit_fitness(individual=self)
        return self.fitness

    def compute_fitness(self):
        my_2048 = Tester_For_2048(config=self.genome)
        self.fitness = my_2048.test_2048()
        return self.fitness

    def reproduce(self, mate):
        male_genome = self.get_genome()
        female_genome = mate.get_genome()
        crossover_point = random.randint(1, len(male_genome) - 1)
        offspring = male_genome[0:crossover_point] + female_genome[crossover_point:]
        return offspring

    def mutate(self,odds=0.01):
        # odds are between 0 and 1,
        # they correspond to the percentage of chance of mutation for each gene independently
        # if at least one mutation occurs, the function returns True
        mutated = False
        new_genome = []
        for gene in self.genome:
            my_random = random.randint(0,10000)
            if my_random < 10000 * odds:
                # the mutation will happen
                mutated = True
                new_value = random.randint(0,9)
                while new_value == gene:
                    new_value = random.randint(0,9)
                new_genome.append(new_value)
            else:
                new_genome.append(gene)
        self.genome = new_genome
        return mutated


class Population(object):
    def __init__(self, population_size, individual_size, individuals=None, fitness_function=None):

        self.population = Random_queue()
        if fitness_function is None:
            self.selected_function = 'compute_test_fitness'
        else:
            self.selected_function = fitness_function

        if individuals is not None:
            for individual in individuals:
                self.population.push(individual.fitness, individual)
        else:
            fitnessless_individuals = []
            for individual in range(0, population_size):
                genome = []
                for gene in range(0, individual_size):
                    curr_gene = random.randint(0, 9)
                    genome.append(curr_gene)
                new_guy = Individual(genome)
                fitnessless_individuals.append(new_guy)

            pool = ThreadPool(2)  # will use all cores of my laptop
            fitness_results = pool.map(methodcaller(self.selected_function), fitnessless_individuals)

            pool.close()
            pool.join()
            # Now that all fitness scores have been computed and set, let's add the individuals to the populuation
            increment = 0
            for individual in fitnessless_individuals:
                self.population.push(individual.fitness, individual)
                increment += 1

    def pick_individual(self):
        return self.population.get()

    def get_best_individual(self):
        return self.population.best_individual

    def genetic_algorithm(self, threshold):
        generation = 0
        while True:
            new_population = Random_queue()
            fitnessless_individuals = []
            print('New generation : ' + str(generation) + ' about to start')
            for increment in range(0, len(self.population.queue)):
                # now is the time to choose the individuals that deserve it!
                # better fitness score equals better chances of reproducing
                male = self.pick_individual()
                female = self.pick_individual()
                while (str(female.get_genome()) == str(male.get_genome())):  # in case we get the same individual twice
                    female = self.pick_individual()

                offspring_genome = male.reproduce(female)

                list_like_genome = []
                for gene in offspring_genome:
                    list_like_genome.append(int(gene))
                offspring = Individual(list_like_genome)
                offspring.mutate()
                fitnessless_individuals.append(offspring)

            pool = ThreadPool(2)  # will use all cores of my laptop
            fitness_results = pool.map(methodcaller(self.selected_function), fitnessless_individuals)

            pool.close()
            pool.join()
            # Now that all fitness scores have been computed and set, let's add the individuals to the populuation
            increment = 0
            for individual in fitnessless_individuals:
                new_population.push(individual.fitness, individual)
                increment += 1

            self.population = new_population

            if self.get_best_individual().fitness > threshold:
                return self.get_best_individual()
            generation += 1

