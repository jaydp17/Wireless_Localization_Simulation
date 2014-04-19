from grid import *

# globals
NUM_OF_NODES = 100
GRID_SIZE = 750
NODE_RANGE = 250
ERROR_IN_L1_NODES = 10
NUM_L0_NODES = 10


def main():
    grid = Grid(GRID_SIZE, NODE_RANGE)

    for i in range(NUM_OF_NODES):
        x = randint(0, GRID_SIZE)
        y = randint(0, GRID_SIZE)
        node_type = NodeType.OTHER
        if i < NUM_L0_NODES:
            node_type = NodeType.L0
        grid.add_node(Node(x, y, node_type))

    grid.run_neighbour_discovery()
    grid.assign_L1_nodes(ERROR_IN_L1_NODES)

    grid.estimate_other_nodes()

    print("done!")


if __name__ == "__main__":
    main()