import numpy as np
import matplotlib.pyplot as plt

from typing import Tuple, List

class GraphEngine:
    def __init__(self, node_radius: int = 30):
        self.__node_radius = node_radius
        self.__node_diameter = node_radius * 2

        self.__n_1, self.__n_2 = 1, 4 # Group number
        self.__n_3, self.__n_4 = 1, 4 # Variant number

        np.random.seed(int(f"{self.__n_1}{self.__n_2}{self.__n_3}{self.__n_4}")) # Random seed to make results reproducable 

        self.__VERTICES = 17

        ADJACENCY_MATRIX = np.random.uniform(0.0, 2.0, (self.__VERTICES, self.__VERTICES)) # Random graph adjacency matrix in range [0, 2]
        K = 1.0 - self.__n_3 * 0.02 - self.__n_4 * 0.005 - 0.25 # Computing K by given formula
        ADJACENCY_MATRIX *= K # Scalar multiplying
        BOOLEAN_ROUNDED_ADJACENCY_MATRIX = ADJACENCY_MATRIX > 1.0 # Creating boolean matrix whether element larger or 
        self.__ADJACENCY_MATRIX = BOOLEAN_ROUNDED_ADJACENCY_MATRIX.astype(int) # Converting boolean matrix to integer matrix

    @property
    def ADJACENCY_MATRIX(self) -> np.array:
        return self.__ADJACENCY_MATRIX

    @property
    def VERTICES(self) -> int:
        return self.__VERTICES

    @property
    def node_diameter(self) -> int:
        return self.__node_diameter

    @property
    def node_radius(self) -> int:
        return self.__node_radius

    @node_radius.setter
    def node_radius(self, val: int) -> None:
        if not isinstance(val, int):
            raise ValueError("Node radius must be an integer!")
        
        self.__node_radius = val
        self.__node_diameter = val * 2

    def __validate_margins(vertical_margin: int, horizontal_margin: int) -> bool:
        """The function checks if given margins are valid regarding to node radius"""
        raise Exception("Not implemented yet")

    def __calculate_nodes_coords(self, vertical_margin: int, horizontal_margin: int) -> Tuple[List[List[int | float]], List[List[int | float]]]:
        """Returns X, y lists of coords separated by levels that is stored in tuple \n Margins must be validated"""

        # Base case
        if self.__VERTICES == 1:
            return [0], [0]

        X, Y = [], []

        # Individual lehel height including vertical margin
        level_height = self.__node_diameter + vertical_margin * 2

        # Since our graph must have triangulum shape, it's depth is a ceil of binary logarithm of number of vertices
        levels = int(np.ceil(np.log2(self.__VERTICES)))

        # Compute last level number of vertices
        last_level_n_vertices = (levels * 2) - 1
        # Based on last level number of vertices compute it's length
        last_level_length = (last_level_n_vertices * self.__node_diameter) + (last_level_n_vertices * horizontal_margin) * 2
        # Compute graph center based on last level length
        graph_x_center = int(np.ceil(last_level_length / 2))


        # -1 Is a base case, because first level must have only one node
        last_level_n_vertices = -1
        # Compute buffer for first level (that contains only one node)
        # This buffer will help to easily compute nodes X coordinates
        # At each iteration we will reduce the buffer to make our nodes positioned it a triangle shape
        level_left_buffer_space = graph_x_center - self.__node_radius - vertical_margin

        # We store used nodes to track whether we will went out of self.__VERTICES number of all graph nodes limit on last level
        used_nodes = 0

        # In this loop, level is inverted, e.g. levels=7; level=6 the true level is 2
        true_level = 1
        for level in range(levels, 0, -1):
            # OY Boundaries
            level_high_boundary = level_height * level
            level_low_boundary = level_high_boundary - level_height

            # Number of level vertices
            level_n_vertices = last_level_n_vertices + 2

            # This condition is only true on last level
            # self.__VERTICES - used_nodes is a maximum nodes that engine can draw on the current level
            # If its lower that current level nodes amount, we limit current level max nodes with maximum nodes allowed on the current level, which is self.__VERTICES - used_nodes
            if self.__VERTICES - used_nodes  < level_n_vertices:
                level_n_vertices = self.__VERTICES - used_nodes

            level_vertices_X_cords, level_vertices_Y_cords = [], []
            # Second buffer that is placed right after the level_left_buffer_space
            # When node is placed, the buffer is shifting to the next node start
            level_occupation_after_buffer = 0
            for _ in range(1, level_n_vertices + 1):
                # Compute space that the node will occupy
                vertice_space_occupation = horizontal_margin * 2 + self.__node_diameter
                # Compute vertice X coordinate via buffers and vertice space occupation
                vertice_X = level_left_buffer_space + level_occupation_after_buffer + vertice_space_occupation / 2
                # Shifting level (second) buffer
                level_occupation_after_buffer += vertice_space_occupation

                # Node's Y coordinate is and arithmetic mean of low and high OY boundaries
                vertice_Y = (level_low_boundary + level_high_boundary) // 2

                level_vertices_X_cords.append(vertice_X)
                level_vertices_Y_cords.append(vertice_Y)


            X.append(level_vertices_X_cords)
            Y.append(level_vertices_Y_cords)

            used_nodes += level_n_vertices

            # Update current level number of vertices for next iteration
            last_level_n_vertices = level_n_vertices
            true_level += 1
            # Shift first buffer for next iteration
            level_left_buffer_space -= self.__node_diameter + horizontal_margin * 2

        
        return X, Y

    def __plot_node_arrows(self, X_cords: List[int], y_cords: List[int]) -> None:
        raise Exception("Not implemented yet, will use matplotlib FancyArrowPatch feature")

    def plot_graph(self, vertical_margin: int, horizontal_margin: int) -> None:
        X, Y = self.__calculate_nodes_coords(vertical_margin, horizontal_margin)

        print(f"X coords: {X}")
        print(f"Y coords: {Y}")

if __name__ == "__main__":
    ge = GraphEngine(node_radius=50) # diameter is 100
    ge.plot_graph(25, 25) # node occupation will be 100x100 square