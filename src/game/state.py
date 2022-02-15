class GameState:
    def __init__(self, configuration: str, parent=None, movement_cost=0, heuristic_cost=0, depth=0):
        self.__configuration = configuration  # string representing the board configuration
        self.__parent = parent  # this state's parent state
        self.__movement_cost = movement_cost  # the cost from the initial state to this state
        self.__heuristic_cost = heuristic_cost  # the estimated cost to the goal
        self.__depth = depth  # the depth of the node in the search tree

    # custom less_than function to be used in priority queue
    def __lt__(self, other):
        return self.movement_cost + self.heuristic_cost < other.movement_cost + other.heuristic_cost

    @property
    def configuration(self):
        return self.__configuration

    @property
    def parent(self):
        return self.__parent

    @property
    def movement_cost(self):
        return self.__movement_cost

    @property
    def heuristic_cost(self):
        return self.__heuristic_cost

    @heuristic_cost.setter
    def heuristic_cost(self, heuristic_cost):
        self.__heuristic_cost = heuristic_cost

    @property
    def depth(self):
        return self.__depth

    # check if the goal condition is met
    def is_goal(self):
        return self.__configuration == "012345678"

    @staticmethod
    # check if the blank tile can be swapped with the given tile
    def __is_legal_move(blank_pos, blank_dest):
        x_blank = blank_pos % 3
        y_blank = int(blank_pos / 3)
        x_dest = blank_dest % 3
        y_dest = int(blank_dest / 3)
        return 0 <= blank_dest < 9 and (x_blank == x_dest or y_blank == y_dest)

    @staticmethod
    def __swap(st, index1, index2):
        return st[0:min(index1, index2)] + st[max(index1, index2)] + st[min(index1, index2) + 1:max(index1, index2)] + \
               st[min(index1, index2)] + st[max(index1, index2) + 1:]

    # returns all the states that are reachable from this state
    def spawn_children(self):
        children = []
        configuration = self.__configuration
        blank = configuration.find('0')
        moves = [-1, 1, -3, 3]
        for move in moves:
            if self.__is_legal_move(blank, blank + move):
                children.append(
                    GameState(configuration=self.__swap(self.__configuration, blank, blank + move), parent=self,
                              movement_cost=self.__movement_cost + 1, depth=self.depth + 1)
                )
        return children
