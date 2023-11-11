from search import *
from problems import *
from collections import Counter

import argparse
import matplotlib.pyplot as plt



plt.rcParams.update({'font.family': "Arial", 'font.size': 10})


class CountCalls:
    """Delegate all attribute gets to the object, and count them in ._counts"""

    def __init__(self, obj):
        self._object = obj
        self._counts = Counter()

    def __getattr__(self, attr):
        "Delegate to the original object, after incrementing a counter."
        self._counts[attr] += 1
        return getattr(self._object, attr)


# draw the map
def draw_map(problem, ax):
    distances_dict = problem.map.distances
    city_coordinates_dict = problem.map.locations

    # draw edges
    for link in distances_dict:
        distance = distances_dict[link]

        b_city = link[0]
        b_coordinates = city_coordinates_dict[b_city]
        e_city = link[1]
        e_coordinates = city_coordinates_dict[e_city]

        ax.plot([b_coordinates[0], e_coordinates[0]], [b_coordinates[1], e_coordinates[1]], marker='o', markersize=5,
                color='k')
        ax.text((b_coordinates[0] + e_coordinates[0]) * 0.5 * 0.98, (b_coordinates[1] + e_coordinates[1]) * 0.5 * 0.98,
                distance, horizontalalignment='left', verticalalignment='top')

    # states
    for city in city_coordinates_dict:
        city_coordinates = city_coordinates_dict[city]
        heuristic_value = problem.h(Node(city))
        # ax.text(city_coordinates[0]*0.98, city_coordinates[1]*0.98, city, horizontalalignment='right', verticalalignment='top', bbox={'facecolor':'gray', 'alpha':0.5})
        ax.text(city_coordinates[0] * 0.98, city_coordinates[1] * 0.98, '{}({})'.format(city, int(heuristic_value)),
                horizontalalignment='right', verticalalignment='top', bbox={'facecolor': 'gray', 'alpha': 0.5})

    # put initial and goal states
    initial_state = problem.initial
    initial_state_coordinates = city_coordinates_dict[initial_state]
    ax.scatter([initial_state_coordinates[0]], [initial_state_coordinates[1]], s=64, c='blue', zorder=100)

    goal_state = problem.goal
    goal_state_coordinates = city_coordinates_dict[goal_state]
    ax.scatter([goal_state_coordinates[0]], [goal_state_coordinates[1]], s=64, c='green', zorder=100)


# draw path
def draw_path(problem, node, ax):
    # get the path
    current_path = path_states(node)

    x = []
    y = []
    for state in current_path:
        temp_coordinates = problem.map.locations[state]
        x.append(temp_coordinates[0])
        y.append(temp_coordinates[1])

    ax.plot(x, y, marker='o', markersize=5, color='red')


parser = argparse.ArgumentParser(description='')
parser.add_argument('--initial_state', type=str, default='A', help='initial state')
parser.add_argument('--goal_state', type=str, default='B', help='goal state')
parser.add_argument('--search_algorithm', type=str, default='breadth_first_graph_search', help='search algorithm')
FLAGS = parser.parse_args()

print('initial_state: {}'.format(FLAGS.initial_state))
print('goal_state: {}'.format(FLAGS.goal_state))
print('search_algorithm: {}'.format(FLAGS.search_algorithm))

# Some specific RouteProblems
romania = Map(
    {('O', 'Z'): 71, ('O', 'S'): 151, ('A', 'Z'): 75, ('A', 'S'): 140, ('A', 'T'): 118,
     ('L', 'T'): 111, ('L', 'M'): 70, ('D', 'M'): 75, ('C', 'D'): 120, ('C', 'R'): 146,
     ('C', 'P'): 138, ('R', 'S'): 80, ('F', 'S'): 99, ('B', 'F'): 211, ('B', 'P'): 101,
     ('B', 'G'): 90, ('B', 'U'): 85, ('H', 'U'): 98, ('E', 'H'): 86, ('U', 'V'): 142,
     ('I', 'V'): 92, ('I', 'N'): 87, ('P', 'R'): 97},
    {'A': (76, 497), 'B': (400, 327), 'C': (246, 285), 'D': (160, 296), 'E': (558, 294),
     'F': (285, 460), 'G': (368, 257), 'H': (548, 355), 'I': (488, 535), 'L': (162, 379),
     'M': (160, 343), 'N': (407, 561), 'O': (117, 580), 'P': (311, 372), 'R': (227, 412),
     'S': (187, 463), 'T': (83, 414), 'U': (471, 363), 'V': (535, 473), 'Z': (92, 539)})

route = RouteProblem(FLAGS.initial_state, FLAGS.goal_state, map=romania)

# wrap the problem with counters for book-keeping
route_problem = CountCalls(route)

# find the solution
if FLAGS.search_algorithm == 'depth_first_graph_search':
    solution_node = depth_first_graph_search(route_problem)
elif FLAGS.search_algorithm == 'breadth_first_graph_search':
    solution_node = breadth_first_graph_search(route_problem)
elif FLAGS.search_algorithm == 'astar':
    solution_node = astar(route_problem)

# collect statisics
counts = route_problem._counts
counts.update(actions_in_solution=len(solution_node), cost_of_solution=solution_node.path_cost)

print('# nodes created: {}'.format(counts['result']))
print('# nodes extended: {}'.format(counts['actions']))
print('# is-goal called: {}'.format(counts['is_goal']))
print('# solution: {}'.format(path_states(solution_node)))
print('# actions in solution: {}'.format(counts['actions_in_solution']))
print('cost of solution: {}'.format(counts['cost_of_solution']))

# create figure and axis
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xticks([])
ax.set_yticks([])
draw_map(route_problem, ax)
draw_path(route_problem, solution_node, ax)

# fig.tight_layout()
# fig_filename = 'romania_map_and_solution__{}.pdf'.format(FLAGS.search_algorithm)
# fig.savefig(fig_filename, dpi=300)

plt.show()

