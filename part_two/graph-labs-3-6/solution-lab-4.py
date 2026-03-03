from graph_engine.ge_triangular import GraphEngine

from typing import List, Dict, Tuple
from string import Template

GraphPowers = Dict[int, int]


class GraphEngineExtended(GraphEngine):
    @staticmethod
    def sort_graph_powers(powers: GraphPowers) -> GraphPowers:
        return dict(sorted(powers.items(), key=lambda item: item[0], reverse=False))


    def get_vertices_powers(self, directed: bool = True) -> GraphPowers:
        """Since we store our graph in adjacency matrix, best time complexity would be O(n^2)"""

        powers: GraphPowers = {}
        correct_adjacency_matrix = self._DIRECTED_ADJACENCY_MATRIX if directed else self._UNDIRECTED_ADJANCENCY_MATRIX

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

        correct_adjacency_matrix = self._DIRECTED_ADJACENCY_MATRIX if directed else self._UNDIRECTED_ADJANCENCY_MATRIX

        for row in range(correct_adjacency_matrix.shape[0]):
            if int(sum(correct_adjacency_matrix[row, :])) == 0 and any(correct_adjacency_matrix[:, row]) != 0:
                hanging_vertices.append(row)

        return hanging_vertices

    def get_isolated_vertices(self, directed: bool = True) -> List[int]:
        """Uses vertices_powers method"""

        isolated_vertices = []

        correct_adjacency_matrix = self._DIRECTED_ADJACENCY_MATRIX if directed else self._UNDIRECTED_ADJANCENCY_MATRIX

        for row in range(correct_adjacency_matrix.shape[0]):
            # Directed and not directed matrices will work the same
            if int(sum(correct_adjacency_matrix[row, :]) + sum(correct_adjacency_matrix[:, row])) == 0:
                isolated_vertices.append(row)

        return isolated_vertices


if __name__ == "__main__":
    ge = GraphEngineExtended(
        koef_template=Template("1.0 - $first * 0.01 - $second * 0.01 - 0.3"),
        node_radius=100,
    )
    print("✓ Graph Powers:", ge.get_vertices_powers())
    print("✓ Half-Powers Exit:", ge.get_halfpowers_exits())
    print("✓ Half-Powers Entry:", ge.get_halfpowers_entry())
    print("✓ Is Homogeneous:", ge.is_homogeneous())
    print("✓ Isolated Vertices:", ge.get_isolated_vertices())
    print("✓ Hanging Vertices:", ge.get_hanging_vertices())
    ge.plot_graph(100, 100, directed=True)