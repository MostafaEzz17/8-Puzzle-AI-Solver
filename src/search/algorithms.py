import heapq

from graphviz import Digraph
from collections import deque
from abc import abstractmethod, ABC

from game.state import GameState
from game.utils import string_to_grid
from search.heuristics import Heuristic


# parent abstract class for all search algorithms
class SearchAlgorithm(ABC):
    def __init__(self):
        self.__expanded = set()  # a set of all expanded nodes
        self.__max_depth = 0
        self._frontier = []

    @property
    def expanded(self):
        return self.__expanded

    @property
    def max_depth(self):
        return self.__max_depth

    @max_depth.setter
    def max_depth(self, max_depth):
        self.__max_depth = max_depth

    @abstractmethod
    # appending to the frontier according to the type of search
    def _append_to_frontier(self, state):
        pass

    @abstractmethod
    # popping the frontier according to the type of search
    def _remove_from_frontier(self):
        pass

    def search(self, initial_state: GameState, dot: Digraph):
        self._append_to_frontier(initial_state)
        while self._frontier:
            curr = self._remove_from_frontier()
            if curr.configuration in self.expanded:
                continue
            # add the parent-child edge to the dot object
            if curr.parent:
                dot.edge(string_to_grid(curr.parent.configuration), string_to_grid(curr.configuration))
            self.expanded.add(curr.configuration)
            self.max_depth = max(self.max_depth, curr.depth)
            if curr.is_goal():
                return curr, self.expanded, self.max_depth, dot
            for child in curr.spawn_children():
                if child.configuration not in self.expanded:
                    self._append_to_frontier(child)
        return None, self.expanded, self.max_depth, dot


# a parent class for DFS and BFS
class UninformedSearch(SearchAlgorithm, ABC):
    def __init__(self):
        super().__init__()
        self._frontier = deque()

    def _append_to_frontier(self, state):
        self._frontier.append(state)


class BFS(UninformedSearch):
    def _remove_from_frontier(self):
        # treat frontier as a queue
        return self._frontier.popleft()


class DFS(UninformedSearch):
    def _remove_from_frontier(self):
        # treat frontier as a stack
        return self._frontier.pop()


class AStar(SearchAlgorithm):
    def __init__(self, heuristic: Heuristic):
        self.__heuristic = heuristic
        super().__init__()

    def _append_to_frontier(self, state):
        state.heuristic_cost = self.__heuristic.calculate_cost(state)
        heapq.heappush(self._frontier, state)

    def _remove_from_frontier(self):
        return heapq.heappop(self._frontier)
