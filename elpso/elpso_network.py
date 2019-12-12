"""Class that represents the network to be evolved."""
import random
import logging
from train import train_and_score
from network import Network
import copy

class ELPSONetwork(Network):
    """Represent a network and let us operate on it.

    Currently only works for an MLP.
    """
    def __init__(self, nn_param_choices=None):
        super().__init__(nn_param_choices)
        self.velocity = {}
        self.pbest = {}

    def create_random(self):
        """Create a random network."""
        for key in self.nn_param_choices:
            self.network[key] = random.uniform(0, len(self.nn_param_choices[key]) - 1)
            v = len(self.nn_param_choices[key]) / 2
            self.velocity[key] = random.uniform(-v, v)
        self.pbest = copy.deepcopy(self.network)
        self.pbest["accuracy"] = 0.

    def converted_network(self):
        converted = {}
        for key in self.network:
            idx = int(round(self.network[key]))
            converted[key] = self.nn_param_choices[key][idx]
        return converted

    def train(self, dataset):
        if self.accuracy == 0.:
            self.accuracy = train_and_score(self.converted_network(), dataset)
            if self.pbest["accuracy"] == 0.:
                self.pbest["accuracy"] = self.accuracy

    def print_network(self):
        """Print out a network."""
        logging.info(self.converted_network())
        logging.info("Network accuracy: %.2f%%" % (self.accuracy * 100))
