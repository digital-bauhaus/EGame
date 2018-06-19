from game.individuals.dot import Dot

from random import choice, uniform
from copy import copy

import numpy as np

class Breeder:
    def __init__(self, parent):
        self.parent = parent

    def breed(self, population):
        """
        this function gets called by the EGame on one population
        it gets a population consisting of individuals
        each individual has certain statistics and traits
        """
        # return self.breed_copy_dead_example(population)
        return self.breed_example_with_ga(population)

    def initialize_population(self, num_individuals, color):
        """
        this function gets calles by EGame before the first frame
        it gets the number of individuals which have to be generated
        also, it gets the color of the population
        """
        return self.initialize_population_example(num_individuals, color)

    
    def initialize_population_example(self, num_individuals, color):
        """
        example initializer
        creates individuals with random traits
        """
        population = []
        for _ in range(num_individuals):
            population.append(Dot(self.parent, color=color))
        return population


    def breed_copy_dead_example(self, population):
        """
        example breeding function
        simply copy dead individuals traits to a new individual
        """
        population_cpy = copy(population)

        dead = []
        alive = []
        for individual in population_cpy:
            if individual.dead:
                dead.append(individual)
            else:
                alive.append(individual)

        if len(alive) == 0:
            print("END OF BREED")
            return None
        for _ in range(len(dead)):
            dead_individual = choice(dead)
            alive_individual = choice(alive)

            new_individual = Dot(self.parent,
                                 color=dead_individual.color,
                                 position=alive_individual._position,
                                 dna=dead_individual.get_dna())
            population_cpy.append(new_individual)
        for dead_individual in dead:
            population_cpy.remove(dead_individual)
        return population_cpy


    def breed_example_with_ga(self, population):
        """
        application of a basic genetic algorithm for breeding
        """
        population_cpy = copy(population)
        dead = []
        alive = []
        for individual in population_cpy:
            if individual.dead:
                dead.append(individual)
            else:
                alive.append(individual)

        for _ in range(len(dead)):
            # get the position where the child should be inserted on the field
            where = choice(alive)._position
            color = alive[0].color

            selected = self.select_example(population_cpy)
            parent1 = selected[0]
            parent2 = selected[1]
            child1, child2 = self.crossover_example(copy(parent1), copy(parent2))
            child1 = self.tweak_example(child1)
            child2 = self.tweak_example(child2)
            score_child1 = self.assess_individual_fitness_example(child1)
            score_child2 = self.assess_individual_fitness_example(child2)
            if score_child1 > score_child2:
                new_individual = Dot(self.parent, color=color, position=where, dna=child1.get_dna())
            else:
                new_individual = Dot(self.parent, color=color, position=where, dna=child2.get_dna())
            population_cpy.append(new_individual)
        for dead_individual in dead:
            population_cpy.remove(dead_individual)
        return population_cpy


    def tweak_example(self, individual):
        """
        we want to increase the trait to seek food and increase armor
        """

        dna = individual.get_dna()
        increase = uniform(0, 0.1)

        perc = dna[0]
        des = dna[1]
        abil = dna[2]

        perc = self.mutate_dna(
            dna=perc, increase_value=increase, increase=3)
        des = self.mutate_dna(
            dna=des, increase_value=increase, increase=3)
        abil = self.mutate_dna(
            dna=abil, increase_value=increase, increase=2)

        dna = [perc, des, abil]
        individual.dna_to_traits(dna)
        return individual

    def mutate_dna(self, dna, increase_value, increase):
        # select some other dna to be decreased
        choices = [i for i in range(len(dna))]
        choices.remove(increase)
        decreased = False
        while not decreased:
            decrease = choice(choices)
            if dna[decrease] - increase_value >= 0.0:
                dna[decrease] -= increase_value
                decreased = True
            else:
                choices.remove(decrease)
            if len(choices) == 0:
                break
        # if we were able to reduce the value for the other dna -> increase the desired dna
        if decreased:
            # increase the value
            dna[increase] += increase_value if dna[increase] <= 1.0 else 1.0
        # otherwise we cannot do anything
        return dna


    def crossover_example(self, solution_a, solution_b):
        """
        crossover of two individuals
        """
        dna_a = solution_a.get_dna()
        dna_b = solution_b.get_dna()
        for i in range(len(dna_a)):
            if uniform(0, 1) < 0.5:
                tmp = dna_a[i]
                dna_a[i] = dna_b[i]
                dna_b[i] = tmp
        solution_a.dna_to_traits(dna_a)
        solution_b.dna_to_traits(dna_b)
        return solution_a, solution_b

    def select_example(self, population):
        """
        example select
        """
        fitness_array = np.empty([len(population)])
        for i in range(len(population)):
            score = self.assess_individual_fitness_example(population[i])
            fitness_array[i] = score
        
        # span value range
        for i in range(1, len(fitness_array)):
            fitness_array[i] = fitness_array[i] + fitness_array[i - 1]
        
        parents = self.selectParentSUS(population, fitness_array, 2)
        return parents

    def selectParentSUS(self, population, fitness_array, count):
        """
        Stochastic uniform sampling
        """
        individual_indices = []
        # build the offset = random number between 0 and f_l / n
        offset = uniform(0, fitness_array[-1] / count)
        # repeat for all selections (n)
        for _ in range(count):
            index = 0
            # increment the index until we reached the offset
            while fitness_array[index] < offset:
                index += 1
            # increment the offset to the next target
            offset = offset + fitness_array[-1] / count
            individual_indices.append(population[index])
        # return all selected individual indices
        return np.array(individual_indices)

    def assess_individual_fitness_example(self, individual):
        """
        example fitness assessment of an individual
        """
        # get statistics of individual
        # refer to Statistic class
        # what parameter are stored in a statistic object
        statistic = individual.statistic
        # get dna of individual
        # multi dimensional array
        # perception_dna_array = [0][x]
        #   food =               [0][0]
        #   poison =             [0][1]
        #   health_potion =      [0][2]
        #   opponent =           [0][3]
        #   corpse =             [0][4]
        #   predator =           [0][5]
        # desires_dna_array =    [1][x]
        #   seek_food =          [1][0]
        #   dodge_poison =       [1][1]
        #   seek_potion =        [1][2]
        #   seek_opponents =     [1][3]
        #   seek_corpse =        [1][4]
        #   dodge_predators =    [1][5]
        # abilities_dna_array =  [2][x]
        #   armor_ability =      [2][0]
        #   speed =              [2][1]
        #   strength =           [2][2]
        #   poison_resistance =  [2][3]
        #   toxicity =           [2][4]
        dna = individual.get_dna()
        score = dna[0][3] + dna[1][3] + dna[2][2] + \
            statistic.enemies_attacked + statistic.consumed_corpses + statistic.opponents_seen
        return score
