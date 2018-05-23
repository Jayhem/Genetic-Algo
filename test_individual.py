from unittest import TestCase
from GeneticAlgo import Individual
import collections


class TestIndividual(TestCase):

    def test_get_genome(self):
        test_subject = Individual([0, 1, 2, 5, 6, 7, 2, 0])
        self.assertEqual(test_subject.get_genome(), '01256720')

    def test_set_fitness(self):
        test_subject = Individual([0, 1, 2, 5, 6, 7, 2, 0])
        test_subject.set_fitness(1024)
        self.assertEqual(test_subject.fitness, 1024)

    def test_reproduce(self):
        test_subject = Individual([0, 1, 2, 5, 6, 7, 2, 0])
        test_subject2 = Individual([9, 9, 9, 9, 9, 9, 9, 9])
        item_counter = collections.Counter()
        for increment in range(0, 100):
            offspring = test_subject.reproduce(test_subject2)
            self.assertEqual(len(test_subject.get_genome()),len(offspring))
            item_counter[offspring] += 1

        # Verify if distribution is proper
        self.assertTrue( len( item_counter ) > 6 )
        most_common = item_counter.most_common()
        self.assertTrue( most_common[0][1] > 10 )

    def test_compute_test_fitness(self):
        test_subject = Individual([0, 1, 2, 5, 6, 7, 2, 0])
        self.assertEqual(test_subject.compute_test_fitness(),2513440)

    def test_compute_fitness(self):
        test_subject = Individual([0, 1, 2, 5, 6, 7, 2, 0])
        self.assertTrue(test_subject.compute_fitness() > 128)

    def test_mutate(self):
        test_subject = Individual([0,0,0,0,0,0,0])
        before = test_subject.get_genome()
        test_subject.mutate(odds = .95)
        after = test_subject.get_genome()
        self.assertNotEqual(before,after)
