from problems import *
import heapq
from collections import deque


##### Queues #####
# First-in-first-out and Last-in-first-out queues, and
# a PriorityQueue, which allows you to keep a collection of items,
# and continually remove from it the item with minimum f(item) score.

FIFOQueue = deque

LIFOQueue = list


class PriorityQueue:
    """A queue in which the item with minimum f(item) is always popped first."""

    def __init__(self, items=(), key=lambda x: x):
        self.key = key
        self.items = []  # a heap of (score, item) pairs
        for item in items:
            self.add(item)

    def add(self, item):
        """Add item to the queuez."""
        pair = (self.key(item), item)
        heapq.heappush(self.items, pair)

    def pop(self):
        """Pop and return the item with min f(item) value."""
        return heapq.heappop(self.items)[1]

    def top(self): return self.items[0][1]

    def __len__(self): return len(self.items)

    def __contains__(self, node):
        """Return True if the key is in PriorityQueue."""
        return any([item == node for _, item in self.items])


def is_cycle(node, k=30):
    "Does this node form a cycle of length k or less?"
    def find_cycle(ancestor, k):
        return (ancestor is not None and k > 0 and
                (ancestor.state == node.state or find_cycle(ancestor.parent, k - 1)))
    return find_cycle(node.parent, k)


def g(n):
    return n.path_cost

def depth_first_graph_search(problem):
    "Search deepest nodes in the search tree first."

    node = Node(problem.initial)
    frontier = LIFOQueue([node])
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            s = child.state
            if not is_cycle(child):
                frontier.append(child)
    return failure
    # create a frontiers queue
     # create a node for initial state and append it to frontiers
    # create a set to keep track of reached/expanded states
    # go through frontiers queue
    # get the node from queue
    # check if it is goal
    # if yes, return the node
            # add node's state to reached/expanded states set
            # expand the node
            # make sure child's state is not reached AND child node is not in the queue


def breadth_first_graph_search(problem):
    "Search shallowest nodes in the search tree first."

    node = Node(problem.initial)
    frontier = FIFOQueue([node])
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            s = child.state
            if not is_cycle(child):
                frontier.appendleft(child)

    return failure
    # create a frontiers queue
    # create a node for initial state and append it to frontiers
    # create a set to keep track of reached/expanded states
    # go through frontiers queue
    # get the node from queue
    # check if it is goal
    # if yes, return the node
    # add node's state to reached/expanded states set
    # expand the node
    # make sure child's state is not reached AND child node is not in the queue


def astar(problem):
    node = Node(problem.initial)
    frontier = PriorityQueue([node], key=lambda n: g(n) + problem.h(n))
    reached = {problem.initial: node}
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.add(child)
    return failure

    # create a frontiers queue
    # Hint: you can use PriorityQueue()
    # create a node for initial state and append it to frontiers
    # create a set to keep track of reached/expanded states
    # go through frontiers queue
    # get the node from queue
    # check if it is goal
    # if yes, return the node
    # add node's state to reached/expanded states set
    # expand the node
    # make sure child's state is not reached AND child node is not in the queue
    # or if child in frontier, check if we have a cheaper solution at this time
    # if cheaper remove old node from frontier and add new one











