from graph_engine import GraphEngine

from typing import List, Dict, Tuple, Set
import numpy as np
from numpy.typing import NDArray
from string import Template

GraphPowers = Dict[int, int]


class GraphEngineExtended(GraphEngine):
    @staticmethod
    def sort_graph_powers(powers: GraphPowers) -> GraphPowers:
        return dict(sorted(powers.items(), key=lambda item: item[0], reverse=False))

    def _get_adjacency_matrix(self, directed: bool) -> NDArray:
        return (
            self._DIRECTED_ADJACENCY_MATRIX
            if directed
            else self._UNDIRECTED_ADJANCENCY_MATRIX
        )

    def get_vertices_powers(self, directed: bool = True) -> GraphPowers:
        """Since we store our graph in adjacency matrix, best time complexity would be O(n^2)"""

        powers: GraphPowers = {}
        correct_adjacency_matrix = self._get_adjacency_matrix(directed)

        for row in range(correct_adjacency_matrix.shape[0]):
            powers[row] = int(sum(correct_adjacency_matrix[row, :]))

        return self.sort_graph_powers(powers=powers)

    def get_halfpowers_exits(self) -> GraphPowers:
        """Only for directed graph"""

        powers: GraphPowers = {}

        for row in range(self._DIRECTED_ADJACENCY_MATRIX.shape[0]):
            powers[row] = int(sum(self._DIRECTED_ADJACENCY_MATRIX[row, :]))

        return self.sort_graph_powers(powers=powers)

    def get_halfpowers_entry(self) -> GraphPowers:
        """Only for directed graph"""

        powers: GraphPowers = {}

        for row in range(self._DIRECTED_ADJACENCY_MATRIX.shape[0]):
            powers[row] = int(sum(self._DIRECTED_ADJACENCY_MATRIX[:, row]))

        return self.sort_graph_powers(powers=powers)

    def is_homogeneous(self, directed: bool = True) -> Tuple[bool, int]:
        """
        Returns boolean flag whether the graph is homogeneous and graph's power
        If graph isn't homogeneous, graph's power equals -1
        """

        powers = self.get_vertices_powers(directed=directed)

        homogeneous = all(power == powers[0] for power in powers)

        return homogeneous, powers[0] if homogeneous else -1

    def get_hanging_vertices(self, directed: bool = True) -> List[int]:
        """Uses vertices_powers method"""

        hanging_vertices = []

        correct_adjacency_matrix = self._get_adjacency_matrix(directed)

        for row in range(correct_adjacency_matrix.shape[0]):
            if (
                int(sum(correct_adjacency_matrix[row, :])) == 0
                and any(correct_adjacency_matrix[:, row]) != 0
            ):
                hanging_vertices.append(row)

        return hanging_vertices

    def get_isolated_vertices(self, directed: bool = True) -> List[int]:
        """Uses vertices_powers method"""

        isolated_vertices = []

        correct_adjacency_matrix = self._get_adjacency_matrix(directed)

        for row in range(correct_adjacency_matrix.shape[0]):
            # Directed and not directed matrices will work the same
            if (
                int(
                    sum(correct_adjacency_matrix[row, :])
                    + sum(correct_adjacency_matrix[:, row])
                )
                == 0
            ):
                isolated_vertices.append(row)

        return isolated_vertices

    def _dfs_paths_search_by_last_vertice(
        self,
        last_vertice: int,
        paths: List,
        path: List,
        adjacency_matrix: NDArray,
        curr_path_lengh: int,
        full_path_length: int,
    ) -> None:
        if curr_path_lengh > full_path_length:
            paths.append(
                tuple(path[:])
            )  # Adding a copy of path to prevent mutating inside paths list
            return

        for i in range(adjacency_matrix.shape[0]):
            if adjacency_matrix[last_vertice][i] == 0:
                continue

            path.append(int(i))
            self._dfs_paths_search_by_last_vertice(
                i, paths, path, adjacency_matrix, len(path), full_path_length
            )
            del path[-1]

    def _dfs_paths_search(self, length: int, adjacency_matrix: NDArray) -> List[List[int]]:
        paths = []

        for i in range(adjacency_matrix.shape[0]):
            self._dfs_paths_search_by_last_vertice(
                last_vertice=i,
                paths=paths,
                path=[i],
                adjacency_matrix=adjacency_matrix,
                curr_path_lengh=1,
                full_path_length=length
            )
        
        return paths

    def _get_paths_number_by_length(
        self, adjacency_matrix: NDArray, full_path_length: int
    ) -> int:
        if full_path_length <= 1:
            return int(np.sum((adjacency_matrix)))

        powered_adjacency_matrix = np.copy(adjacency_matrix)

        for _ in range(full_path_length - 1):
            powered_adjacency_matrix = powered_adjacency_matrix @ adjacency_matrix

        return np.sum(powered_adjacency_matrix)

    def get_all_paths_by_length(
        self, length: int, directed: bool = True
    ) -> Tuple[int, List[Tuple[int]]]:
        correct_adjacency_matrix = self._get_adjacency_matrix(directed)

        paths = self._dfs_paths_search(length=length, adjacency_matrix=correct_adjacency_matrix)
        n_paths = self._get_paths_number_by_length(correct_adjacency_matrix, length)

        return n_paths, paths

    def get_reachability_matrix(self, directed: bool = True) -> NDArray:
        reachability_matrix = self._get_adjacency_matrix(directed)

        # logical OR operation
        reachability_matrix: NDArray = reachability_matrix | np.identity(reachability_matrix.shape[0])

        n_vertices = reachability_matrix.shape[0]

        for k in range(n_vertices):
            for i in range(n_vertices):
                for j in range(n_vertices):
                    reachability_matrix[i, j] = reachability_matrix[i, j] or (reachability_matrix[i, k] and reachability_matrix[k, j])

        return reachability_matrix

    def get_strong_connectivity_matrix(self) -> NDArray:
        pass

    def get_strong_connectivity_components(self) -> List[int]:
        pass

    def plot_condensation_graph(self) -> None:
        pass

if __name__ == "__main__":
    directed = input(
        "Calculate first computations for directed/undirected graph? (directed or undirected): "
    )

    if directed == "directed":
        directed_option = True
    elif directed == "undirected":
        directed_option = False

    ge = GraphEngineExtended(
        koef_template=Template("1.0 - $first * 0.01 - $second * 0.01 - 0.3"),
        node_radius=100,
    )

    print("For directed graph")
    print("✓ Graph Powers:", ge.get_vertices_powers(directed=directed_option))
    print("✓ Half-Powers Exit:", ge.get_halfpowers_exits())
    print("✓ Half-Powers Entry:", ge.get_halfpowers_entry())
    print("✓ Is Homogeneous:", ge.is_homogeneous(directed=directed_option))
    print("✓ Isolated Vertices:", ge.get_isolated_vertices(directed=directed_option))
    print("✓ Hanging Vertices:", ge.get_hanging_vertices(directed=directed_option))
    ge.plot_graph(100, 100, directed=directed_option)

    directed = input(
        "Calculate second computations for directed/undirected graph? (directed or undirected): "
    )

    if directed == "directed":
        directed_option = True
    elif directed == "undirected":
        directed_option = False

    ge = GraphEngineExtended(
        koef_template=Template("1.0 - $first * 0.005 - $second * 0.005 - 0.27"),
        node_radius=100,
    )

    print("✓ Half-Powers Exit:", ge.get_halfpowers_exits())
    print("✓ Half-Powers Entry:", ge.get_halfpowers_entry())

    ge.get_all_paths_by_length(length=3)

    ge.plot_graph(100, 100, directed=True)
