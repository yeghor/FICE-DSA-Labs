from graph_engine.ge_triangular import GraphEngine

from typing import List, Dict
from string import Template

GraphPowers = Dict[int, int]


class GraphEngineExtended(GraphEngine):
    def vertices_powers(self, directed: bool = True) -> GraphPowers:
        """Since we store our graph in adjacency matrix, best time complexity would be O(n^2)"""

        powers: GraphPowers = {}
        correct_adjacency_matrix = self._DIRECTED_ADJACENCY_MATRIX if directed else self._UNDIRECTED_ADJANCENCY_MATRIX

        for row in range(correct_adjacency_matrix.shape[0]):
            powers[row] = int(sum(correct_adjacency_matrix[row, :]))

        return dict(sorted(powers.items(), key=lambda item: item[0], reverse=False))

    def halfpowers_entry(self) -> any:
        pass

    def halfpowers_exits(self) -> any:
        pass

    def halfpowers_exits(self) -> any:
        pass

    def is_homogeneous(self) -> bool:
        pass

    def hanging_vertices(self) -> List[int]:
        """Uses vertices_powers method"""
        pass

    def isolated_vertices(self, directed: bool = True) -> List[int]:
        """Uses vertices_powers method"""

        isolated_vertices = []

        correct_adjacency_matrix = self._DIRECTED_ADJACENCY_MATRIX if directed else self._UNDIRECTED_ADJANCENCY_MATRIX

        for row in range(len(self._DIRECTED_ADJACENCY_MATRIX)):
            # Directed and not directed matrices will work the same
            if int(sum(correct_adjacency_matrix[row, :]) + sum(correct_adjacency_matrix[:, row])) == 0:
                isolated_vertices.append(row)

        return isolated_vertices


if __name__ == "__main__":
    ge = GraphEngineExtended(
        koef_template=Template("1.0 - $first * 0.01 - $second * 0.01 - 0.3"),
        node_radius=100,
    )
    print(ge.vertices_powers(directed=True))
    print(ge.isolated_vertices(directed=True))
    ge.plot_graph(100, 100, directed=True)

    print(ge.vertices_powers(directed=False))
    print(ge.isolated_vertices(directed=False))
    ge.plot_graph(100, 100, directed=False)