from math import sqrt
from abc import ABC, abstractmethod

from game.state import GameState


# parent abstract class for heuristics
class Heuristic(ABC):

    @staticmethod
    @abstractmethod
    def _calculate_cell_cost(x_cell, y_cell, x_goal, y_goal):
        pass

    # loop over all cells calculating the heuristic cost according to the child class
    def calculate_cost(self, state: GameState):
        config = state.configuration
        heuristic_cost = 0
        for index in range(0, len(config)):
            if config[index] != '0':
                # current cell coordinates
                x_cell = index % 3
                y_cell = int(index / 3)
                # coordinates of current cell at the goal state
                x_goal = int(config[index]) % 3
                y_goal = int(int(config[index]) / 3)
                heuristic_cost += self._calculate_cell_cost(x_cell, y_cell, x_goal, y_goal)
        return heuristic_cost


class EuclideanHeuristic(Heuristic):
    @staticmethod
    def _calculate_cell_cost(x_cell, y_cell, x_goal, y_goal):
        return sqrt((x_cell - x_goal) ** 2 + (y_cell - y_goal) ** 2)


class ManhattanHeuristic(Heuristic):
    @staticmethod
    def _calculate_cell_cost(x_cell, y_cell, x_goal, y_goal):
        return abs(x_cell - x_goal) + abs(y_cell - y_goal)
