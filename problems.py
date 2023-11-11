import math
from collections import defaultdict


##### Problems and Nodes #####
# We start by defining the abstract class for a Problem;
# specific problem domains will subclass this. To make it
# easier for algorithms that use a heuristic evaluation function,
# Problem has a default h function (uniformly zero), and
# subclasses can define their own default h function.
class Problem(object):
    """The abstract class for a formal problem. A new domain subclasses this,
    overriding `actions` and `results`, and perhaps other methods.
    The default heuristic is 0 and the default action cost is 1 for all states.
    When yiou create an instance of a subclass, specify `initial`, and `goal` states
    (or give an `is_goal` method) and perhaps other keyword args for the subclass."""

    def __init__(self, initial=None, goal=None, **kwds):
        self.__dict__.update(initial=initial, goal=goal, **kwds)

    def actions(self, state):        raise NotImplementedError

    def result(self, state, action): raise NotImplementedError

    def is_goal(self, state):        return state == self.goal

    def action_cost(self, s, a, s1): return 1

    def h(self, node):               return 0

    def __str__(self):
        return '{}({!r}, {!r})'.format(
            type(self).__name__, self.initial, self.goal)


# We also define a Node in a search tree, and some functions
# on nodes: expand to generate successors; path_actions and
# path_states to recover aspects of the path from the node.
class Node:
    "A Node in a search tree."

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.__dict__.update(state=state, parent=parent, action=action, path_cost=path_cost)

    def __repr__(self): return '<{}>'.format(self.state)

    def __len__(self): return 0 if self.parent is None else (1 + len(self.parent))

    def __lt__(self, other): return self.path_cost < other.path_cost


failure = Node('failure', path_cost=math.inf)  # Indicates an algorithm couldn't find a solution.
cutoff = Node('cutoff', path_cost=math.inf)  # Indicates iterative deepening search was cut off.


def expand(problem, node):
    "Expand a node, generating the children nodes."
    s = node.state
    for action in problem.actions(s):
        s1 = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s1)
        yield Node(s1, node, action, cost)


def path_actions(node):
    "The sequence of actions to get to this node."
    if node.parent is None:
        return []
    return path_actions(node.parent) + [node.action]


def path_states(node):
    "The sequence of states to get to this node."
    if node in (cutoff, failure, None):
        return []
    return path_states(node.parent) + [node.state]


##### Route Finding Problems #####
# In a RouteProblem, the states are names of "cities" (or other locations),
# like 'A' for Arad. The actions are also city names; 'Z' is the action
# to move to city 'Z'. The layout of cities is given by a separate data
# structure, a Map, which is a graph where there are vertexes (cities),
# links between vertexes, distances (costs) of those links (if not
# specified, the default is 1 for every link), and optionally the 2D (x, y)
# location of each city can be specified. A RouteProblem takes this Map
# as input and allows actions to move between linked cities. The default
# heuristic is straight-line distance to the goal, or is uniformly zero
# if locations were not given.

class RouteProblem(Problem):
    """A problem to find a route between locations on a `Map`.
    Create a problem with RouteProblem(start, goal, map=Map(...)}).
    States are the vertexes in the Map graph; actions are destination states."""

    def actions(self, state):
        """The places neighboring `state`."""
        return self.map.neighbors[state]

    def result(self, state, action):
        """Go to the `action` place, if the map says that is possible."""
        return action if action in self.map.neighbors[state] else state

    def action_cost(self, s, action, s1):
        """The distance (cost) to go from s to s1."""
        return self.map.distances[s, s1]

    def g(self, node):
        "cost of the path from initial state to current state"
        return node.path_cost

    def h(self, node):
        "Straight-line distance between state and the goal."
        locs = self.map.locations
        return straight_line_distance(locs[node.state], locs[self.goal])


def straight_line_distance(A, B):
    "Straight-line distance between two points."
    return sum(abs(a - b) ** 2 for (a, b) in zip(A, B)) ** 0.5


class Map:
    """A map of places in a 2D world: a graph with vertexes and links between them.
    In `Map(links, locations)`, `links` can be either [(v1, v2)...] pairs,
    or a {(v1, v2): distance...} dict. Optional `locations` can be {v1: (x, y)}
    If `directed=False` then for every (v1, v2) link, we add a (v2, v1) link."""

    def __init__(self, links, locations=None, directed=False):
        if not hasattr(links, 'items'):  # Distances are 1 by default
            links = {link: 1 for link in links}
        if not directed:
            for (v1, v2) in list(links):
                links[v2, v1] = links[v1, v2]
        self.distances = links
        self.neighbors = multimap(links)
        self.locations = locations or defaultdict(lambda: (0, 0))


def multimap(pairs) -> dict:
    "Given (key, val) pairs, make a dict of {key: [val,...]}."
    result = defaultdict(list)
    for key, val in pairs:
        result[key].append(val)

    for state in result:
        result[state] = sorted(result[state], reverse=True)

    return result