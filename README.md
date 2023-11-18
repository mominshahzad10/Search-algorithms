Search Algorithms Analysis in Routing Problems

Overview

This project conducts an in-depth analysis of various search algorithms applied to routing problems, using a map of Romania as the test environment. The primary objective is to understand the performance of these algorithms in terms of memory usage, computation time, and path efficiency. The analysis is carried out using Python, with a focus on depth-first graph search, breadth-first graph search, and A* algorithms.

Key Features:

Algorithm Implementation: Implements depth-first graph search, breadth-first graph search, and A* search algorithms in Python.
Performance Metrics: Evaluates the algorithms based on the number of nodes created, number of nodes extended, calls to the is-goal function, and total path cost.
Route Search Analysis: Uses a Romania map graph model to analyze the performance of each algorithm in routing from one city to another.
Detailed Output: Generates detailed output including the solution path, number of actions in the solution, and the cost of the solution.
Technical Details

Python Scripts: Includes search.py, route_search.py, and problems.py for executing and analyzing the search algorithms.
Graph-Based Approach: Utilizes a graph representation of the Romania map with heuristic values based on airline-distance for A* algorithm.
Command Line Interface: Offers a CLI for running experiments with different initial and goal states, and search algorithms.
Project Goals

To compare and contrast the efficiency of different search algorithms in routing problems.
To understand the trade-offs between memory usage, computation time, and path optimality in search algorithms.
To provide a framework for further exploration and analysis of search algorithms in practical routing scenarios.

Example command to run an experiment:
python route_search.py --initial_state A --goal_state B --search_algorithm depth_first_graph_search

Future Enhancements:

Integration of more complex algorithms like Dijkstra's and Bellman-Ford.
Expansion of the graph model to include real-world maps and larger datasets.
Development of a visual interface to display the path and performance metrics.
