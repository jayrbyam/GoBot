"""Class that represents the network to be evolved."""
import random
from network import Network

class GeneticNetwork(Network):

    def create_random(self):
        """Create a random network."""
        for key in self.nn_param_choices:
            self.network[key] = random.choice(self.nn_param_choices[key])
