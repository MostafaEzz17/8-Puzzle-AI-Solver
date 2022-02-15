class StatsFile(object):
    def __init__(self, file_name):
        self.file_name = file_name
        with open(self.file_name, 'w') as file:
            file.write("")

    # used to print the total stats at the end of the file.
    def write(self, msg):
        with open(self.file_name, 'a') as file:
            file.write(msg + "\n")


# turns the given string to a grid-like format
def string_to_grid(config: str):
    grid = ''
    for i in range(0, 3):
        for j in range(0, 3):
            grid += config[3 * i + j % 3]
        grid += '\n'
    return grid


def generate_dot_graph(dot, expanded, goal, threshold=20000):
    color = goal
    while color:
        dot.node(string_to_grid(color.configuration), style='filled', fillcolor='lightgreen')
        color = color.parent
    if len(expanded) < threshold:
        dot.render('game/expanded_nodes.gv', view=True)
    else:
        with open('game/expanded_nodes.gv', 'w') as f:
            print(dot.source, file=f)
