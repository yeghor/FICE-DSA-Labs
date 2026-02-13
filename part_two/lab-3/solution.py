import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as plt_patches

from typing import Tuple, List, Dict

class GraphEngine:
    def __map_vertices_cords(self, X: List[List[float]], Y: List[List[float]], VALUES: List[int]) -> Dict[int, Tuple]:
        """
        Maps level shaped cords that returns __calculate_nodes_coords method
        Out: dict, where key is a vertice value and value is a tuple of (x, y) cords
        """
        out = {}

        for X_level, Y_level, VALUES_level in zip(X, Y, VALUES):
            for vertice_data in zip(X_level, Y_level, VALUES_level):
                out[vertice_data[2]] = vertice_data[0], vertice_data[1]

        return out

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
        print(ADJACENCY_MATRIX.shape)
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

    def __calculate_nodes_coords(self, vertical_margin: int, horizontal_margin: int) -> Tuple[List[List[float]], List[List[float]], List[List[float]]]:
        """Returns X, y lists of coords separated by levels that is stored in tuple \n Margins must be validated"""

        # Base case
        if self.__VERTICES == 1:
            return [0], [0]

        X, Y, VALUES = [], [], []

        # Individual level height including vertical margin
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

        current_vertice_value = 0

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
            # If its lower that the current level nodes amount, we limit current level max nodes with maximum nodes allowed on the current level, which is self.__VERTICES - used_nodes
            if self.__VERTICES - used_nodes  < level_n_vertices:
                level_n_vertices = self.__VERTICES - used_nodes

            level_vertices_X_cords, level_vertices_Y_cords, level_vertices_values = [], [], []
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
                level_vertices_values.append(current_vertice_value)

                current_vertice_value += 1

            X.append(level_vertices_X_cords)
            Y.append(level_vertices_Y_cords)
            VALUES.append(level_vertices_values)

            used_nodes += level_n_vertices

            # Update current level number of vertices for next iteration
            last_level_n_vertices = level_n_vertices
            true_level += 1
            # Shift first buffer for next iteration
            level_left_buffer_space -= self.__node_diameter + horizontal_margin * 2

        
        return X, Y, VALUES

    def __plot_node_arrows(self, axes, VERTICES_PREPARED: Dict[int, List[float]]) -> None:
        """
        Note that X_cords and Y_cords must be flattened arrays \n
        Order of coordinates must be left to right starting on level 1 \n
        Find circle dot at specific angle on a boundary - https://youtu.be/aHaFwnqH5CU?si=EgcHxdBHLg2H_qp7
        """

        adjacency_matrix_shape = self.__ADJACENCY_MATRIX.shape

        for i in range(adjacency_matrix_shape[0]):
            for j in range(adjacency_matrix_shape[1]):
                if self.__ADJACENCY_MATRIX[i, j] == 1:
                    # Base case
                    if i == j:
                        continue

                    start_cords, end_cords = VERTICES_PREPARED[i], VERTICES_PREPARED[j]
                    start_x, start_y = start_cords[0], start_cords[1]
                    end_x, end_y = end_cords[0], end_cords[1]

                    X_distance = end_x - start_x
                    Y_distance = end_y - start_y

                    # Usin atan2, instead of atan!
                    # Because distances can be negative
                    # That's why, when we compute angle tan, we can loose directions information
                    # e. g. -1/-1 = 1
                    # Also, atan2 handles edge cases, when y or x distances are equal to zero
                    arrow_angle = math.atan2(Y_distance, X_distance) 

                    circle_start_X = start_x + self.node_radius * math.cos(arrow_angle)
                    circle_start_Y = start_y + self.node_radius * math.sin(arrow_angle)

                    circle_end_X = end_x - self.node_radius * math.cos(arrow_angle)
                    circle_end_Y = end_y - self.node_radius * math.sin(arrow_angle)

                    dx = circle_end_X - circle_start_X
                    dy = circle_end_Y - circle_start_Y

                    if self.__ADJACENCY_MATRIX[j, i] == 1:
                        axes.arrow(circle_start_X, circle_start_Y, dx, dy, length_includes_head=True, head_width=13, head_length=13, linewidth=1)
                        axes.arrow(circle_end_X, circle_end_Y, -dx, -dy, length_includes_head=True, head_width=13, head_length=13, linewidth=0)
                    else:
                        axes.arrow(circle_start_X, circle_start_Y, dx, dy, length_includes_head=True, head_width=13, head_length=13, linewidth=1)


    def plot_graph(self, vertical_margin: int, horizontal_margin: int) -> None:
        X, Y, VALUES = self.__calculate_nodes_coords(vertical_margin, horizontal_margin)
        VERTICES_PREPARED = self.__map_vertices_cords(X, Y, VALUES)

        figure, axes = plt.subplots()
      
        for value, cords in VERTICES_PREPARED.items():
            axes.add_artist(plt_patches.Circle(cords, self.node_radius, fill=False))
            plt.text(cords[0], cords[1], s=value, fontsize="12", ha="center", va="center")

        self.__plot_node_arrows(axes, VERTICES_PREPARED)

        plt.xlim(0, 1500)
        plt.ylim(0, 1000)
        plt.axis("off")
        plt.title(f"{self.__VERTICES} nodes Graph visualization")
        plt.savefig(f"./graph-{self.VERTICES}-nodes.png")
        plt.show()
    

if __name__ == "__main__":
    ge = GraphEngine(node_radius=50) # diameter is 100
    ge.plot_graph(25, 25) # node occupation will be 100x100 square