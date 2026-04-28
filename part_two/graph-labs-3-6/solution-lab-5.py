from graph_engine import GraphEngine

from typing import *
import numpy as np
from numpy.typing import NDArray
from string import Template
import matplotlib.pyplot as plt
import random

import time

# Compatible with DFS
PathItem = int


# BFS
BFSPathItem = List[PathItem]
BFSPath = List[List[BFSPathItem]]


# DFS
DFSPath = List[PathItem]


class GraphEngineTraversal(GraphEngine):
    def __init__(self, koef_template, node_radius = 30, logs_delay: float = 0.3):
        super().__init__(koef_template, node_radius)

        self._logs_delay = logs_delay


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

    def _find_start_vertices(self, adjacency_matrix: NDArray) -> List[int]:
        adjacency_matrix_sum = np.sum(adjacency_matrix, axis=1)  # 1d array
        return np.nonzero(adjacency_matrix_sum)[0].tolist()

    def _find_start_vertex(self, adjacency_matrix: NDArray) -> int:
        return self._find_start_vertices(adjacency_matrix)[0]

    def _dfs(self, adjacency_matrix: NDArray, vertex: int, visited: Set, path: DFSPath) -> None:
        if vertex in visited:
            return

        input(f"DFS: Visited {vertex} vertex # ")
        time.sleep(self._logs_delay)

        path.append(vertex)
        visited.add(vertex)

        for next_vertex, value in enumerate(adjacency_matrix[vertex]):
            if value == 0 or next_vertex == vertex:
                continue

            self._dfs(adjacency_matrix, next_vertex, visited, path)


    def _get_dfs(self, adjacency_matrix: NDArray) -> List[DFSPath]:
        print(F"\nDFS START\n")

        start_vertex = self._find_start_vertex(adjacency_matrix)

        dfs_traversal: List[DFSPath] = []

        input(f"Started path №1 (from {start_vertex}th vertex) # ")
        time.sleep(self._logs_delay)


        dfs_path: DFSPath = []
        seen = set()
        self._dfs(adjacency_matrix, start_vertex, seen, dfs_path)

        dfs_traversal.append(dfs_path)
        time.sleep(self._logs_delay)

        print(f"Finished path №1 \n Path -> {dfs_path} \n\n")

        n_path = 2

        if len(dfs_path) != len(adjacency_matrix[0]):
            for i, new_start_vertex in enumerate(range(len(adjacency_matrix[0]))):
                if len(dfs_path) >= len(adjacency_matrix[0]):
                    break

                if new_start_vertex == start_vertex or new_start_vertex in seen:
                    continue

                input(f"Started path №{n_path} (from {new_start_vertex}th vertex) # ") # To exclude zero indexed value and already done first path
                time.sleep(self._logs_delay)

                dfs_path: List[DFSPath] = []
                self._dfs(adjacency_matrix, new_start_vertex, seen, dfs_path)

                if dfs_path:
                    dfs_traversal.append(dfs_path)

                print(f"Finished path №{n_path} \n Path -> {dfs_path} \n\n")
                n_path += 1

        print(f"Full DFS Traversal:")
        for i, path in enumerate(dfs_traversal):
            print(f"Component №{i+1}: {path}")

        print(F"\nDFS END\n\n")

        return dfs_traversal

    def _get_bfs(self, directed: bool = True) -> List[BFSPath]:
        print(F"\nBFS START\n")

        adjacency_matrix = self._get_adjacency_matrix(directed)
        start_vertices = self._find_start_vertices(adjacency_matrix)

        bfs_traversal = []
        seen = set()

        for i, start_vertex in enumerate(start_vertices):
            if start_vertex in seen:
                continue

            if len(seen) == len(adjacency_matrix[0]):
                break

            input(f"Started path №{i+1} (from {start_vertex}th vertex) # ")
            time.sleep(self._logs_delay)

            path: List[Tuple[int, int]] = []
            queue: List[Tuple[int, int]] = [[1, start_vertex]] # bfs step -> vertex
            seen.add(start_vertex)

            while queue:
                queue_vertex = queue.pop()

                curr_step = queue_vertex[0]
                vertex = queue_vertex[1]

                input(F"BFS: Visited {vertex} vertex. Current BFS distance: {curr_step} # ")
                time.sleep(self._logs_delay)

                while curr_step > len(path):
                    path.append([])

                path[curr_step-1].append(vertex)

                for next_vertex in np.nonzero(adjacency_matrix[queue_vertex[1]])[0].tolist():
                    if next_vertex not in seen:
                        queue.insert(0, (curr_step+1, next_vertex))
                        seen.add(next_vertex)

            bfs_traversal.append(path)

            print(f"Finished path №{i+1} \n Path -> {path} \n\n")

        print(f"Full BFS Traversal:")
        for i, path in enumerate(bfs_traversal):
            print(f"Layer №{i+1}: {path}")

        print(F"\nBFS END\n\n")

        return bfs_traversal


    def plot_dfs(self, vertical_margin: int, horizontal_margin: int, directed: bool = True) -> None:
        adjacency_matrix = self._get_adjacency_matrix(directed=directed)
        dfs_traversal = self._get_dfs(adjacency_matrix)

        VERTICES_PREPARED = self._get_prepared_vertices(vertical_margin, horizontal_margin)

        opacities = self._compute_dfs_opacities(n_vertex=len(adjacency_matrix[0]))

        figure, axes = plt.subplots()

        for outer_order, (dfs, color) in enumerate(zip(dfs_traversal, self._generate_hex_colors(len(adjacency_matrix[0])))):
            for inner_order, (path_item, opacity) in enumerate(zip(dfs, opacities)):
                self._add_vertex_artix(
                    VERTICES_PREPARED[path_item], self.vertex_radius, f"Vertex: ${path_item}$ \n\n DFS order: ${inner_order+1}_{outer_order+1}$", axes, color, opacity, True, fontsize=10
                )
                        
        self._plot_node_arrows(axes, VERTICES_PREPARED, adjacency_matrix, directed)

        plot_limits = self._define_plot_limits(VERTICES_PREPARED)

        plt.xlim(plot_limits[0], plot_limits[1])
        plt.ylim(plot_limits[2], plot_limits[3])
        plt.axis("off")
        plt.title(
            "DFS Traversal"
        )
        plt.show()


    def plot_bfs(self, vertical_margin: int, horizontal_margin: int, directed: bool = True) -> None:
        bfs_traversal = self._get_bfs(directed)

        VERTICES_PREPARED = self._get_prepared_vertices(vertical_margin, horizontal_margin)
        adjacency_matrix = self._get_adjacency_matrix(directed)   
        # opacities = self._compute_dfs_opacities(n_vertex=len(adjacency_matrix[0]))

        figure, axes = plt.subplots()

        for outer_order, bfs in enumerate(bfs_traversal):
            for inner_order, (step, color) in enumerate(zip(bfs, self._generate_hex_colors(len(bfs)))):
                for vertex in step:
                    self._add_vertex_artix(
                        VERTICES_PREPARED[vertex], self.vertex_radius, f"Vertex: ${vertex}$ \n\n BFS order: ${inner_order+1}_{outer_order+1}$", axes, color, 1.0, True, fontsize=10
                    )                

        self._plot_node_arrows(axes, VERTICES_PREPARED, adjacency_matrix, directed)

        plot_limits = self._define_plot_limits(VERTICES_PREPARED)

        plt.xlim(plot_limits[0], plot_limits[1])
        plt.ylim(plot_limits[2], plot_limits[3])
        plt.axis("off")
        plt.title(
            "BFS Traversal"
        )
        plt.show()

if __name__ == "__main__":
    variant_template = Template("1.0 - $first * 0.02 - $second * 0.005 - 0.25")
    small_density_template = Template("0.6 + $first * 0.02 + $second * 0.01")

    ge = GraphEngineTraversal(
        koef_template=variant_template,
        node_radius=100,
        logs_delay=0.1
    )

    ge.plot_dfs(50, 50)
    ge.plot_bfs(50, 50)