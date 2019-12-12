"""
Class that holds an ELPSO implementation for optimizing a network.

"""
from functools import reduce
from operator import add
import random
from elpso_network import ELPSONetwork
import copy

class ELPSO():

    def __init__(self, nn_param_choices):
        """Create an optimizer.

        Args:
            nn_param_choices (dict): Possible network paremters

        """
        self.nn_param_choices = nn_param_choices
        self.gbest = {}
        self.example_set = []

        # ELPSO constants
        self.example_set_size = 3
        self.w = 0.729
        self.c1 = 2.0
        self.c2 = 2.0

    def create_population(self, count):
        """Create a population of random networks.

        Args:
            count (int): Number of networks to generate, aka the
                size of the population

        Returns:
            (list): Population of network objects

        """
        pop = []
        for _ in range(0, count):
            # Create a random network.
            network = ELPSONetwork(self.nn_param_choices)
            network.create_random()

            # Add the network to our population.
            pop.append(network)

        return pop

    @staticmethod
    def fitness(network):
        """Return the accuracy, which is our fitness function."""
        return network.accuracy

    def grade(self, pop):
        """Find average fitness for a population.

        Args:
            pop (list): The population of networks

        Returns:
            (float): The average accuracy of the population

        """
        summed = reduce(add, (self.fitness(network) for network in pop))
        return summed / float((len(pop)))

    def optimize(self, pop):
        """Evolve a population of networks.

        Args:
            pop (list): A list of network parameters

        Returns:
            (list): The evolved population of networks

        """
        # Get scores for each network.
        graded = [(self.fitness(network), network) for network in pop]

        # Sort on the scores.
        graded = [x[1] for x in sorted(graded, key=lambda x: x[0], reverse=True)]
        self.gbest = copy.deepcopy(graded[0].network)
        self.gbest["accuracy"] = graded[0].accuracy

        for x in pop:
            # Update pbest
            if x.accuracy > x.pbest["accuracy"]:
                x.pbest = copy.deepcopy(x.network)
                x.pbest["accuracy"] = x.accuracy

            # Update the example set according to ELSPO
            if len(self.example_set) == 0:
                 self.example_set.append(copy.deepcopy(self.gbest))
            else:
                better = False
                for example in self.example_set:
                    if example["accuracy"] > self.gbest["accuracy"]:
                        better = True
                        break
                if not better:
                    if len(self.example_set) == self.example_set_size:
                        self.example_set.pop(0) # First in, first out
                    self.example_set.append(copy.deepcopy(self.gbest))
            
            # Update velocity and position according to ELSPO
            example_best = random.choice(self.example_set)
            other_pbest = random.choice(pop).pbest
            for key in self.nn_param_choices:
                x.velocity[key] = 0.729 * x.velocity[key] \
                    + (self.c1 * random.uniform(0, 1) * (other_pbest[key] - x.velocity[key])) \
                    + (self.c2 * random.uniform(0, 1) * (example_best[key] - x.velocity[key]))
                
                # Update position according to velocity
                x.network[key] += x.velocity[key]

                # Wrap the value to be a valid index
                while x.network[key] <= -0.5:
                    x.network[key] += len(self.nn_param_choices[key])
                while x.network[key] >= len(self.nn_param_choices[key]) - 0.5:
                    x.network[key] -= len(self.nn_param_choices[key])

        return pop
