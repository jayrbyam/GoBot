from dlgo.agent.base import Agent
from dlgo.goboard import Move
from dlgo.gotypes import Point
from dlgo.utils import point_from_coords

class Human(Agent):
    def __init__(self):
        self.move = None

    def select_move(self, game_state):
        result = Move.play(point_from_coords(self.move))
        self.move = None
        return result