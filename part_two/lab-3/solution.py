import numpy as np
import matplotlib.pyplot as plt

from typing import Tuple, List

class GraphEngine:
    def __init__(self, node_radius: int = 30):
        self.node_radius = node_radius

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

    def __calculate_nodes_coords(self) -> Tuple[List[int], List[int]]:
        """Returns X, y lists of coords stored in tuple"""

        # Since our graph must have triangulum shape, it's depth is a binary logarithm of number of vertices
        levels = np.ceil(np.log2(self.__VERTICES))
        print(levels)

        for level in range(levels):
            pass

    def __plot_node_arrows(self, X_cords: List[int], y_cords: List[int]) -> None:
        pass

    def plot_graph(self) -> None:
        pass
