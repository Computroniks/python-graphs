#SPDX-FileCopyrightText: 2022 Matthew Nickson <mnickson@sidingsmedia.com>
#SPDX-License-Identifier: MIT

from typing import Union


class NonDirectedError(Exception):
    """
    NonDirectedError The graph is not directed

    An attempt was made to add a directed edge to an undirected graph.
    """

    def __init__(
            self,
            message: str = ""
        ) -> None:
        """
        __init__ Create instance of NonDirectedError

        :param message: Message to output in traceback, defaults to
            "Directed edge cannot be added to an undirected graph"
        :type message: str, optional
        """

        if message == "":
            self._message = "Directed edge cannot be added to an " 
            self._message += "undirected graph"
        else:
            self._message = message
        super().__init__(self._message)


class AlreadyPopulatedError(Exception):
    """
    AlreadyPopulatedError There is already and edge present

    An edge was already present when another edge was being added
    """

    def __init__(
            self,
            source: int = None,
            dest: int = None,
            cost: int = None,
            message: str = "",
        ) -> None:
        """
        __init__ Create instance of exception

        :param source: ID of source node, defaults to None
        :type source: int, optional
        :param dest: ID of destination node, defaults to None
        :type dest: int, optional
        :param cost: Cost of edge, defaults to None
        :type cost: int, optional
        :param message: Message to display, defaults to "An edge was
            already present when another edge was being added."
        :type message: str, optional
        """

        if message == "":
            self._message = "An edge was already present when another "
            self._message += "edge was being added."
        else:
            self._message = message

        self._source = source
        self._dest = dest
        self._cost = cost

        super().__init__(message)

    def __str__(self) -> str:
        message = ""
        message += self._message
        message += f" Trying to add edge between {self._source}, {self._dest}"
        message += f" with cost {self._cost}. First delete this edge before"
        message += "  adding a new one"

        return message


class IllegalArgumentError(ValueError):
    """
    IllegalArgumentError The argument passed is invalid
    """

    pass


class Graph:
    """
    Weighted graph

    A weighted graph using an adjacency matrix to represent
    associations. The graph may optionally be weighted.
    """
    
    def __init__(self, directed: bool = False) -> None:
        """
        __init__ Create instance of Graph

        Graph can be either weighted or weighted directed.

        :param directed: Should the graph be directed, defaults to False
        :type directed: bool, optional
        """

        self._directed = directed

        # The actuall adjacency matrix. For a directed graph, the Y axis
        # is the source, and the X axis the destination.
        self._matrix: list[list[int]] = [[None]]
        
        # A list of all nodes we have. In the same order as the
        # adjacency matrix. Each node has an index beginning at 0. This
        # means that it most cases, the value and index of the node will
        # be the same. This cannot be relied upon in cases where a node
        # has been deleted.
        self._nodes: list[int] = []

        # Array of edges. Edges are represented by a tuple containing
        # the origin node ID, the destination node ID and the cost.
        self._edges: list[tuple[int, int, int]] = []
        
    @property
    def x(self) -> int:
        """
        x The width of the first element in the adjacency matrix

        :rtype: int
        """
        
        if self.y < 1:
            return 0
        else:
            return len(self._matrix[0])

    @property
    def y(self) -> int:
        """
        y The height of the adjacency matrix

        :rtype: int
        """
    
        return len(self._matrix)
    
    @property
    def nodes(self) -> list[int]:
        """
        nodes List of all nodes
        
        A list of all of the nodes currently present in the graph.
        :note: The order of the nodes is in the same order as the
        adjacency matrix

        :rtype: list[int]
        """
        
        return self._nodes

    @property
    def ncount(self) -> int:
        """ 
        count Number of nodes in graph
        
        :rtype: int
        """
        
        return len(self._nodes)

    @property
    def directed(self) -> bool:
        """
        directed Is the graph directed?

        :rtype: bool
        """

        return self._directed

    @property
    def ecount(self) -> int:
        """
        ecount Number of edges present in the graph

        :rtype: int
        """

        return len(self._edges)

    def __str__(self) -> str:
        """
        __str__ Generate a string representation of the graph
        
        Generates a pretty print representation of the adjacency matrix
        ideal for printing to the console.

        :rtype: str
        """

        result = ""

        # Header row
        result += "".ljust(3) + " "
        for i in range(self.x):
            result += str(i).ljust(3) + " "
        result += "\n"

        # Data
        count = 0
        for row in self._matrix:
            result += str(count).ljust(3) + " "
            for char in row:
                if char is None:
                    result += "\u221e".ljust(3) + " "
                else:
                    result += str(char).ljust(3) + " "
            result += "\n"
            count += 1

        return result

    def _extendMatrix(self) -> None:
        """
        _extendMatrix Add an extra column and row to the matrix
        """

        for row in self._matrix:
            row.append(None)
        self._matrix.append([None]*self.x)

    def _addEdge(self, source: int, destination: int, cost: int) -> int:
        """
        _addEdge Add and edge to the graph

        Adds an edge to the graph between the two specified nodes with
        specified cost.

        :param source: Source node
        :type source: int
        :param destination: Destination node
        :type destination: int
        :param cost: Cost of edge
        :type cost: int
        :raises IllegalArgumentError: Source and destination cannot be
            the same.
        :return: Edge ID
        :rtype: int
        """

        if source == destination:
            raise IllegalArgumentError(
                "Source and destination cannot be the same"
            )

        x_index = self._nodes.index(destination)
        y_index = self._nodes.index(source)

        if self._matrix[y_index][x_index] is not None:
            raise AlreadyPopulatedError(source, destination, cost)
        else:
            self._matrix[y_index][x_index] = cost
            self._edges.append((source, destination, cost))
            return len(self._edges) - 1

    def addNode(self) -> int:
        """
        addNode Add a node to the matrix
        
        Adds a node to the matrix, extending the matrix as needed. No
        edges are added
        
        :returns: The ID of the node
        :rtype: int
        """
        
        # We don't need to extend the first time as we start with 1
        # space
        if self.ncount == 0:
            last = -1
        else:
            self._extendMatrix()
            last = self._nodes[-1]
        
        self._nodes.append(last+1) # Increment node ID
        
        return self._nodes[-1]

    def addEdge(
            self, 
            source: int, 
            destination: int, 
            cost: int, 
            directional: bool = False
        ) -> Union[int, list[int, int]]:
        """
        addEdge Add and edge joining two nodes

        Adds and edge between two nodes with the specified cost.
        Optionally, this edge can be directional. If this is the case,
        the path will be from A to B. The path may only be directional
        if the class was initialised with the weighet argument set to
        True. In cases where 

        :param source: ID of the source node
        :type source: int
        :param destination: ID of the destination node
        :type destination: int
        :param cost: Cost of the path
        :type cost: int
        :param directional: Should this path be directional?, defaults
            to False
        :type directional: bool, optional
        :raises NonDirectedError: The graph is non-directed but a
            directed edge was being created.
        :raises IllegalArgumentError: The source and destination node
            cannot be the same.
        :return: The ID of the edge or in case of the graph being and a
           bidirectional edge being created when the graph is directed,
           a list containing the IDs of both edges with the first ID
           being the edge from source to destination.
        :rtype: Union[int, list[int, int]]
        """

        id = [None, None]

        if source == destination:
            raise IllegalArgumentError(
                "The source and destination node cannot be the same"
            )

        if directional:
            if not self._directed:
                raise NonDirectedError()
            else:
                return self._addEdge(source, destination, cost)
        else:
            if self._directed:
                id[0] = self._addEdge(source, destination, cost)
                id[1] = self._addEdge(destination, source, cost)
                return id
            else:
                # For an undirected graph, we only use half of the graph
                # so we must make sure nothing is below the horizontal
                # line.
                first_node = min(source, destination)
                second_node = max(source, destination)
                return self._addEdge(first_node, second_node, cost)

    def neighbours(self, node: int) -> list[int]:
        """
        neighbours Get a list of neighbours

        Returns a list of neighbours of a given node

        :param node: The ID of the node to check
        :type node: int
        :return: A list of neighbouring nodes
        :rtype: list[int]
        """

        nodes: list[int] = []

        for i, val in enumerate(self._matrix[node]):
            if val is not None:
                nodes.append(self.nodes[i])
        
        if not self._directed:
            # We also need to go from dest to source if undirected
            for i in range(node):
                if self._matrix[i][node] is not None:
                    nodes.append(self.nodes[i])

        return nodes

    def edge(self, source: int, destination: int) -> int:
        """
        edge Get the cost of an edge

        Gets the cost of the specified edge between the source and the
        destination.

        :param source: ID of the source node
        :type source: int
        :param destination: ID of destination node
        :type destination: int
        :return: Cost of path.
        :rtype: int
        """

        if self._directed == False:
            node_1 = min(source, destination)
            node_2 = max(source, destination)
        else:
            node_1 = source
            node_2 = destination

        if self._matrix[node_1][node_2] is not None:
            return self._matrix[node_1][node_2]
        
        if self._directed == False:
            # Also check opposite direction for non directed
            if self._matrix[node_2][node_1] is not None:
                return self._matrix[node_2][node_1]

        # There isn't a path between these two nodes
        return None
            

    
def test() -> None:
    """
    Tests for the graph class
    """

    print("Creating graph")
    graph = Graph(True)
    for i in range(5):
        print(f"Adding node with ID: {graph.addNode()}")
    print(graph)
    graph.addEdge(0,3,10)
    graph.addEdge(2,3,1)
    print(graph)
    
def main() -> None:
    print(
        "Warning, this module should not normally be run as a script. "
        + "We will now run the tests"
        )
    test()
    
if __name__ == "__main__":
    main()
