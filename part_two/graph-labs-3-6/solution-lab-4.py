from graph_engine.ge_triangular import GraphEngine

from typing import List, Dict
from string import Template

GraphPowers = Dict[int, int]


class GraphEngineExtended(GraphEngine):
    def vertices_powers(self, directed: bool = True) -> GraphPowers:
        """Since we store our graph in adjacency matrix, best time complexity would be O(n^2)"""

        powers: GraphPowers = {}

        for row in range(self._ADJACENCY_MATRIX.shape[0]):
            if directed:
                powers[row] = int(sum(self._ADJACENCY_MATRIX[row, :]))
            else:
                possible_powers = powers.setdefault(row, 0)
                powers[row] = possible_powers + int(sum(self._ADJACENCY_MATRIX[row, :]))

                # for not-directed graph cases, since we have only one adjacency matrix
                # that suits only for directed graph
                # So we manually add no specified links
                for idx, refers in enumerate(self._ADJACENCY_MATRIX[:, row]):
                    if refers == 1 and idx != row and self._ADJACENCY_MATRIX[row][idx] == 0:
                        row_powers = powers.setdefault(row, 0)

                        powers[row] = row_powers + 1

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

    def isolated_vertices(self) -> List[int]:
        """Uses vertices_powers method"""
        
        isolated_vertices = []

        for row in range(len(self._ADJACENCY_MATRIX)):
            if int(sum(self._ADJACENCY_MATRIX[row])) != 0:
                continue
                
            isolated = True

            for refers in self._ADJACENCY_MATRIX[:, row]:
                if refers == 1:
                    isolated = False
                    break
            
            if isolated:
                isolated_vertices.append(row)
            
        return isolated_vertices

if __name__ == "__main__":
    ge = GraphEngineExtended(
        koef_template=Template("1.0 - $first * 0.01 - $second * 0.01 - 0.3"),
        node_radius=100,
    )
    print(ge.isolated_vertices())
    ge.plot_graph(100, 100, directed=True)
    
