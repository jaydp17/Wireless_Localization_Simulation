from random import randint
import numpy as np


class NodeType:
    L0 = 0      # Nodes that know their exact location
    L1 = 1      # Because there are 3 or more L0 nodes nearby, the location this kind of nodes can be estimated
    OTHER = 2   # All other nodes


class Node:
    def __init__(self, x: int, y: int, node_type: NodeType):
        """
        Node constructior
        @param x: x co-ordinate
        @param y: y co-ordinate
        @param node_type: Type of node
        """
        self.actual_x = x
        self.actual_y = y
        self.type = node_type
        self.neighbours = set()
        if self.type == NodeType.L0 or self.type == NodeType.L1:
            self.x = x
            self.y = y
        else:
            self.x = None
            self.y = None

    def __lt__(self, other) -> bool:
        """
            Override method to check less than element
            @param other: the other object to compare with
            @return: less than or not
            """
        if hasattr(other, 'actual_x'):
            return self.actual_x < other.actual_x

    def __repr__(self) -> str:
        """
        defines how this object should be printed
        @return: string to print
        """
        msg = "Other"
        if self.type == NodeType.L0:
            msg = "L0"
        elif self.type == NodeType.L1:
            msg = "L1"
        return '[{}:{}] => {}, ({}:{})'.format(self.actual_x, self.actual_y, msg, self.x, self.y)

    def add_neighbour(self, node):
        """
        Add a neighbour
        @param node: node to add as a neighbour
        """
        self.neighbours.add(node)

    def set_node_type(self, node_type: NodeType, error: int=0):
        """
        Change Node type
        @param node_type: new node type
        @param error: if it's L1 some error can be introduced
        """
        if node_type == NodeType.L0:
            self.x = self.actual_x
            self.y = self.actual_y
        elif node_type == NodeType.L1:
            self.x = self.actual_x + randint(-error, error)
            self.y = self.actual_y + randint(-error, error)
        elif node_type == NodeType.OTHER:
            self.x = None
            self.y = None

    def estimate_coordinates(self, A: 'matrixA', C: 'matrixC') -> None:
        """
        Estimates co-ordinates of the current node
        @param A: matrix A
        @param C: matrix C
        """
        U, s, V = np.linalg.svd(A, full_matrices=False)
        U_trans = U.transpose()
        D0_inv = np.diag(s)
        x = np.dot(V, np.dot(D0_inv, np.dot(U_trans, C)))
        assert np.allclose(A, np.dot(U, np.dot(np.diag(s), V)))
        self.x, self.y = x

    @staticmethod
    def __sigma_to_d0_inv(sigma, t):
        """
        helper method to convert sigma to D0^-1
        @param sigma: sigma got from SVD
        @param t: some small threshold
        @return: array of D0^-1
        """
        d0_inv = []
        for si in sigma:
            d0_inv.append((1.0 / float(si)) if si > t else 0)
        return d0_inv