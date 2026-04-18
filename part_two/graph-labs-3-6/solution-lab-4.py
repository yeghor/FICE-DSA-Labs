from graph_engine import GraphEngine

from typing import List, Dict, Tuple, Set
import numpy as np
from numpy.typing import NDArray
from string import Template
import matplotlib.pyplot as plt

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

    def _dfs_paths_search(
        self, length: int, adjacency_matrix: NDArray
    ) -> List[List[int]]:
        paths = []

        for i in range(adjacency_matrix.shape[0]):
            self._dfs_paths_search_by_last_vertice(
                last_vertice=i,
                paths=paths,
                path=[i],
                adjacency_matrix=adjacency_matrix,
                curr_path_lengh=1,
                full_path_length=length,
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
        """Time complexity is O(n^length)"""

        correct_adjacency_matrix = self._get_adjacency_matrix(directed)

        paths = self._dfs_paths_search(
            length=length, adjacency_matrix=correct_adjacency_matrix
        )
        n_paths = self._get_paths_number_by_length(correct_adjacency_matrix, length)

        return n_paths, paths

    def get_reachability_matrix(self, directed: bool = True) -> NDArray:
        reachability_matrix = self._get_adjacency_matrix(directed)

        # logical OR
        reachability_matrix: NDArray = reachability_matrix.astype(int) | np.identity(
            reachability_matrix.shape[0]
        ).astype(int)

        n_vertices = reachability_matrix.shape[0]

        for k in range(n_vertices):
            for i in range(n_vertices):
                for j in range(n_vertices):
                    # logical or & and
                    reachability_matrix[i, j] = reachability_matrix[i, j] | (
                        reachability_matrix[i, k] & reachability_matrix[k, j]
                    )

        return reachability_matrix

    def get_strong_connectivity_matrix(self, directed: bool = True) -> NDArray:
        adjacency_matrix = self._get_adjacency_matrix(directed)

        return adjacency_matrix & adjacency_matrix.T

    def _dfs_connectivity_components(
        self, vertex: int, seen: Set, adjacency_matrix: NDArray
    ) -> None:
        """Mutates seen and stores output in it"""

        for next_vertex, conn in enumerate(adjacency_matrix[vertex]):
            if conn == 0 or next_vertex in seen or next_vertex == vertex:
                continue

            seen.add(next_vertex)
            self._dfs_connectivity_components(next_vertex, seen, adjacency_matrix)

    def get_strong_connectivity_components(self) -> Dict[int, Tuple[int]]:
        """Only for non-directed graph"""

        adjacency_matrix = self._get_adjacency_matrix(False)

        connectivity_components = {}
        components_seen = set()

        component_idx = 1

        for start_vertex in range(adjacency_matrix.shape[0]):
            if start_vertex in components_seen:
                continue

            component = set([start_vertex])
            self._dfs_connectivity_components(start_vertex, component, adjacency_matrix)
            components_seen.update(component)

            connectivity_components[component_idx] = tuple(component)
            component_idx += 1

        return connectivity_components

    def plot_condensation_graph(
        self, vertical_margin: int, horizontal_margin: int
    ) -> None:
        """Only for non-directed graph"""

        if not self._validate_margins(vertical_margin, horizontal_margin):
            raise ValueError("Invalid Margins! Must be greater or equal to 0")

        X, Y, VALUES = self._calculate_nodes_coords(vertical_margin, horizontal_margin)
        VERTICES_PREPARED = self._map_vertices_cords(X, Y, VALUES)

        figure, axes = plt.subplots()

        for value, cords in VERTICES_PREPARED.items():
            self._add_vertex_artix(
                cords, self.vertex_radius, value, axes, "#7f9Ef1", 1, True
            )

        connectivity_components = self.get_strong_connectivity_components()
        adjacencty_matrix = np.zeros(
            shape=self._get_adjacency_matrix(directed=False).shape
        )

        for component in connectivity_components.values():
            for i, component_vertex in enumerate(
                sorted(component)[: len(component) - 1]
            ):
                next_vertex = component[i + 1]
                adjacencty_matrix[component_vertex, next_vertex] = 1

        self._plot_node_arrows(axes, VERTICES_PREPARED, adjacencty_matrix, False)

        plot_limits = self._define_plot_limits(VERTICES_PREPARED)

        plt.xlim(plot_limits[0], plot_limits[1])
        plt.ylim(plot_limits[2], plot_limits[3])
        plt.axis("off")
        plt.title(f"Condensation graph of non-directed graph")
        plt.show()


# AI Generated testing for comprehesive and slick terminal results

import sys

class Style:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    BOLD = '\033[1m'
    END = '\033[0m'

def run_test_suite(step_name, koef_formula, directed_default=True):
    print(f"\n{Style.BOLD}{Style.BLUE}=== {step_name} ==={Style.END}")
    
    prompt = f"Graph type for {step_name} [D/u] (default {'directed' if directed_default else 'undirected'}): "
    choice = input(prompt).strip().lower()
    
    if choice in ['u', 'undirected']:
        is_directed = False
    elif choice in ['d', 'directed']:
        is_directed = True
    else:
        is_directed = directed_default

    ge = GraphEngineExtended(
        koef_template=Template(koef_formula),
        node_radius=100,
    )

    print(f"{Style.GREEN}▶ Running computations...{Style.END}")
    
    results = [
        ("Graph Powers", ge.get_vertices_powers(directed=is_directed)),
        ("Is Homogeneous", ge.is_homogeneous(directed=is_directed)),
        ("Isolated Vertices", ge.get_isolated_vertices(directed=is_directed)),
        ("Hanging Vertices", ge.get_hanging_vertices(directed=is_directed)),
    ]

    for label, value in results:
        print(f"  {Style.BOLD}✓ {label:18}:{Style.END} {value}")

    if is_directed:
        print(f"  {Style.BOLD}✓ Half-Powers Exit  :{Style.END} {ge.get_halfpowers_exits()}")
        print(f"  {Style.BOLD}✓ Half-Powers Entry :{Style.END} {ge.get_halfpowers_entry()}")

    components = ge.get_strong_connectivity_components()
    print(f"  {Style.BOLD}✓ SCC Components    :{Style.END} {len(components)} groups found")

    print(f"{Style.GREEN}▶ Generating plots...{Style.END}")
    ge.plot_condensation_graph(50, 50)
    ge.plot_graph(100, 100, directed=is_directed)

if __name__ == "__main__":
    try:
        run_test_suite(
            "Phase 1: Basic Stats", 
            "1.0 - $first * 0.01 - $second * 0.01 - 0.3",
            directed_default=True
        )

        # Второй этап
        run_test_suite(
            "Phase 2: Deep Analysis", 
            "1.0 - $first * 0.005 - $second * 0.005 - 0.27",
            directed_default=True
        )
        
        print(f"\n{Style.GREEN}{Style.BOLD}Testing completed successfully!{Style.END}")

    except KeyboardInterrupt:
        print(f"\n{Style.BLUE}Testing interrupted by user.{Style.END}")
        sys.exit(0)

# if __name__ == "__main__":
#     directed = input(
#         "Calculate first computations for directed/undirected graph? (directed or undirected): "
#     )

#     if directed == "directed":
#         directed_option = True
#     elif directed == "undirected":
#         directed_option = False

#     ge = GraphEngineExtended(
#         koef_template=Template("1.0 - $first * 0.01 - $second * 0.01 - 0.3"),
#         node_radius=100,
#     )

#     print("For directed graph")
#     print("✓ Graph Powers:", ge.get_vertices_powers(directed=directed_option))
#     print("✓ Half-Powers Exit:", ge.get_halfpowers_exits())
#     print("✓ Half-Powers Entry:", ge.get_halfpowers_entry())
#     print("✓ Is Homogeneous:", ge.is_homogeneous(directed=directed_option))
#     print("✓ Isolated Vertices:", ge.get_isolated_vertices(directed=directed_option))
#     print("✓ Hanging Vertices:", ge.get_hanging_vertices(directed=directed_option))
#     print(ge.get_strong_connectivity_components())
#     print(ge.plot_condensation_graph(50, 50))

#     ge.plot_graph(100, 100, directed=False)

#     directed = input(
#         "Calculate second computations for directed/undirected graph? (directed or undirected): "
#     )

#     if directed == "directed":
#         directed_option = True
#     elif directed == "undirected":
#         directed_option = False

#     ge = GraphEngineExtended(
#         koef_template=Template("1.0 - $first * 0.005 - $second * 0.005 - 0.27"),
#         node_radius=100,
#     )

#     print("✓ Half-Powers Exit:", ge.get_halfpowers_exits())
#     print("✓ Half-Powers Entry:", ge.get_halfpowers_entry())

#     print(ge.get_all_paths_by_length(length=3)[0])
#     print(ge.get_reachability_matrix(directed))
#     print(ge.get_strong_connectivity_matrix(directed))
#     print(ge.get_strong_connectivity_components())
#     print(ge.plot_condensation_graph(50, 50))

#     ge.plot_graph(100, 100, directed=True)
