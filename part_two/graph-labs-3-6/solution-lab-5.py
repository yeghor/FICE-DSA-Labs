from graph_engine import GraphEngine

from typing import *
import numpy as np
from numpy.typing import NDArray
from string import Template

# Compatible with DFS
PathItem = Tuple[int, Tuple[float, float]]


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

    def _find_start_vertices(self, adjacency_matrix: NDArray) -> int:        
        adjacency_matrix_sum = np.sum(adjacency_matrix, axis=1) # 1d array
        return np.nonzero(adjacency_matrix_sum)[0].tolist()[0]

    def _dfs(self, adjacency_matrix: NDArray, vertex: int, visited: Set, path: List[int]):
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

    def _bfs(self, adjacency_matrix: NDArray, vertex: int, visited: Set, path: List[int]):
        pass

    def plot_dfs(self, directed: bool = True) -> None:
        adjacency_matrix = self._get_adjacency_matrix(directed=directed)
        start_vertex = self._find_start_vertices(adjacency_matrix)

        dfs_path = []
        seen = set()
        self._dfs(adjacency_matrix, start_vertex, seen, dfs_path)

        if len(dfs_path) != len(adjacency_matrix[0]):
            for new_start_vertex in range(len(adjacency_matrix[0])):
                if len(dfs_path) >= len(adjacency_matrix[0]):
                    break
                
                if new_start_vertex == start_vertex:
                    continue

                self._dfs(adjacency_matrix, new_start_vertex, seen, dfs_path)

        print(dfs_path)

    def plot_bfs(self) -> None:
        # start_vertex = self._find_start_vertices()
        # bfs_path = self._bfs(start_vertex=start_vertex)
        pass

if __name__ == "__main__":
    ge = GraphEngineTraversal(
        koef_template=Template("1.0 - $first * 0.01 - $second * 0.005 - 0.15"),
        node_radius=100,
    )

    ge.plot_dfs(directed=True)
    ge.plot_graph(50, 50, directed=True)