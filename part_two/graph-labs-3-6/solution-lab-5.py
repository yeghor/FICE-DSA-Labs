from graph_engine import GraphEngine

from typing import *
import numpy as np
from numpy.typing import NDArray
from string import Template
import matplotlib.pyplot as plt
import random

# Compatible with DFS
PathItem = int


# BFS
BFSPathItem = List[PathItem]

# Each outer Dict key stands for step in BFS
BFSPath = Dict[int, BFSPathItem]


# DFS
DFSPath = List[PathItem]


class GraphEngineTraversal(GraphEngine):
    @staticmethod
    def _compute_dfs_opacities(n_vertex: int) -> List[float]:
        """Returns evenly computed opacities for path length"""

        return np.linspace(0.1, 1, n_vertex).tolist()[::-1]

    @staticmethod
    def _compute_bfs_opacities(n_steps: int) -> List[float]:
        """Retuerns opacities for each step"""

        return np.linspace(0.1, 1, n_steps).tolist()[::-1]

    @staticmethod
    def _generate_hex_colors(n_colors: int) -> Generator[None, None, str]:
        for _ in range(n_colors):
            # https://stackoverflow.com/questions/13998901/generating-a-random-hex-color-in-python
            yield "#" + "%06x" % random.randint(0, 0xFFFFFF)

    def _find_start_vertices(self, adjacency_matrix: NDArray) -> int:
        adjacency_matrix_sum = np.sum(adjacency_matrix, axis=1)  # 1d array
        return np.nonzero(adjacency_matrix_sum)[0].tolist()[0]

    def _dfs(self, adjacency_matrix: NDArray, vertex: int, visited: Set, path: DFSPath):
        if vertex in visited:
            return

        path.append(vertex)
        visited.add(vertex)

        for next_vertex, value in enumerate(adjacency_matrix[vertex]):
            if value == 0 or next_vertex == vertex:
                continue

            if vertex == 1 and next_vertex == 10:
                print(vertex, next_vertex)
                print(value)

            self._dfs(adjacency_matrix, next_vertex, visited, path)

    def _bfs(
        self, adjacency_matrix: NDArray, vertex: int, visited: Set, path: List[int]
    ):
        pass

    def _get_dfs(self, adjacency_matrix: NDArray) -> List[DFSPath]:
        start_vertex = self._find_start_vertices(adjacency_matrix)

        all_dfs_paths: List[DFSPath] = []

        dfs_path: DFSPath = []
        seen = set()
        self._dfs(adjacency_matrix, start_vertex, seen, dfs_path)

        all_dfs_paths.append(dfs_path)

        if len(dfs_path) != len(adjacency_matrix[0]):
            for new_start_vertex in range(len(adjacency_matrix[0])):
                if len(dfs_path) >= len(adjacency_matrix[0]):
                    break

                if new_start_vertex == start_vertex:
                    continue

                dfs_path: List[DFSPath] = []
                self._dfs(adjacency_matrix, new_start_vertex, seen, dfs_path)
                all_dfs_paths.append(dfs_path)

        return all_dfs_paths

    def plot_dfs(self, vertical_margin: int, horizontal_margin: int, directed: bool = True) -> None:
        adjacency_matrix = self._get_adjacency_matrix(directed=directed)
        dfs_paths = self._get_dfs(adjacency_matrix)
        print(dfs_paths)
        VERTICES_PREPARED = self._get_prepared_vertices(vertical_margin, horizontal_margin)

        opacities = self._compute_dfs_opacities(n_vertex=len(adjacency_matrix[0]))

        figure, axes = plt.subplots()

        for dfs, color in zip(dfs_paths, self._generate_hex_colors(len(adjacency_matrix[0]))):
            for path_item, opacity in zip(dfs, opacities):
                self._add_vertex_artix(
                    VERTICES_PREPARED[path_item], self.vertex_radius, path_item, axes, color, opacity, True
                )
                        
        self._plot_node_arrows(axes, VERTICES_PREPARED, adjacency_matrix, directed)

        plot_limits = self._define_plot_limits(VERTICES_PREPARED)

        plt.xlim(plot_limits[0], plot_limits[1])
        plt.ylim(plot_limits[2], plot_limits[3])
        plt.axis("off")
        plt.title(
            f"{self._VERTICES} nodes {"directed" if directed else "not directed"} graph"
        )
        plt.show()


    def plot_bfs(self) -> None:
        # start_vertex = self._find_start_vertices()
        # bfs_path = self._bfs(start_vertex=start_vertex)
        pass


if __name__ == "__main__":
    ge = GraphEngineTraversal(
        koef_template=Template("1.0 - $first * 0.01 - $second * 0.005 - 0.15"),
        node_radius=100,
    )

    ge.plot_dfs(50, 50)
