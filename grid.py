from math import sqrt
from node import *


class Point:
    def __init__(self, x, y):
        """
        Constructor : sets x and y co-ordinates
        @param x: x co-ordinate
        @param y: y co-ordinate
        """
        self.x = x
        self.y = y

    def __eq__(self, other):
        """
        Override method that defines equality
        @rtype : bool
        @param other: other object to compare this object with
        @return: Equal/Not Equal
        """
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class Grid:
    def __init__(self, size, node_range):
        """
        Grid Constructor
        @param size: size x size will be the dimension of the grid
        @param node_range: range up to which a node can sense
        """
        self.size = size
        self.nodes = []
        self.point_to_node = dict()
        self.node_range = node_range

    def add_node(self, node: Node):
        """
        Add a node to the grid
        @param node: node to add
        """
        self.nodes.append(node)
        self.point_to_node[Point(node.actual_x, node.actual_y)] = node

    def run_neighbour_discovery(self):
        """
        Finds the neighbouring nodes of every node
        """
        for a in self.nodes:
            for b in self.nodes:
                if a == b:
                    continue
                d = sqrt(pow(a.actual_x - b.actual_x, 2) + pow(a.actual_y - b.actual_y, 2))
                if d < self.node_range:
                    a.add_neighbour(b)
                    b.add_neighbour(a)

    def assign_L1_nodes(self, error: int):
        """
        If a node is surrounded by more than 3 L0 nodes
        its location can be estimated, with some error
        @param error: error in location
        """
        for i in range(0, len(self.nodes)):
            if len(self.nodes[i].neighbours) >= 3:
                self.nodes[i].set_node_type(NodeType.L1, error)

    @staticmethod
    def __is_valid_candidate_to_estimate(node: Node):
        """
        Checks if a node is valid to run estimation on

        Validation Criteria : A node is valid if it is surrounded
         by at least 3 nodes who know their location
        @param node: 
        @return: 
        """
        i = 0
        for n in node.neighbours:
            if n.type != NodeType.OTHER:
                i += 1
        return i > 3

    def estimate_other_nodes(self):
        """
        Estimates the location of nodes that don't know their location
        """
        for i in range(0, len(self.nodes)):
            if self.nodes[i].type == NodeType.OTHER and Grid.__is_valid_candidate_to_estimate(self.nodes[i]):
                pre_A = []
                pre_C = []
                for node in self.nodes[i].neighbours:
                    if node.type != NodeType.OTHER:
                        pre_A.append((-2 * node.x, -2 * node.y))

                        # may need to introduce error here

                        # calculates d^2 = (x - x1)^2 + (y - y1)^2,
                        # where x1 and y1 are known x and y are to be found
                        dist_btwn_a_b_squared = pow(self.nodes[i].actual_x - node.x, 2) + pow(
                            self.nodes[i].actual_y - node.y, 2)

                        x1_squared = node.x ** 2
                        y1_squared = node.y ** 2
                        pre_C.append(dist_btwn_a_b_squared - x1_squared - y1_squared)
                A = []
                C = []
                j = 0
                while j < len(pre_A) and j + 1 < len(pre_A):
                    A.append([pre_A[j][0] - pre_A[j+1][0], pre_A[j][1] - pre_A[j+1][1]])
                    C.append(pre_C[j] - pre_C[j+1])
                    j += 2

                # estimates co-ordinates for the current node
                self.nodes[i].estimate_coordinates(A, C)

    @staticmethod
    def distance(a: Node, b: Node):
        """
        Uses estimated location to calculate distance
        @param a: node1
        @param b: node2
        @return: distance between node1 and node2
        """
        return sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2))

    @staticmethod
    def distance_square(a: Node, b: Node):
        """
        Uses estimated location to calculate distance squared
        @param a: node1
        @param b: node2
        @return: distance between node1 and node2
        """
        return pow(a.x - b.x, 2) + pow(a.y - b.y, 2)