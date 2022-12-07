#SPDX-FileCopyrightText: 2022 Matthew Nickson <mnickson@sidingsmedia.com>
#SPDX-License-Identifier: MIT

from weightedGraph import Graph


def dijkstra(graph: Graph, source: int, destination: int) -> list[int]:
    """
    dijkstra An implementation of Dijkstra's shortest path algorithm

    :param graph: The graph to trace
    :type graph: weightedGraph.Graph
    :param source: ID of source node
    :type source: int
    :param destination: ID of destination node
    :type destination: int
    :returns: List of node IDs representing the shortest path to take
    :rtype: list[int]
    """

    unvisited = graph.nodes.copy()
    distance = [float("inf") for i in range(len(unvisited))]
    previous = [None for i in range(len(unvisited))]
    distance[source] = 0

    while len(unvisited) != 0:
        # Get the lowest distance unvisited node
        options = []
        for node in unvisited:
            options.append((distance[node], node))
        current_node = min(options)[1]
        
        if current_node == destination:
            # Done, now just get path
            path = []
            prev = destination
            while prev != None:
                path.append(prev)
                prev = previous[prev]
            return path[::-1]
        else:
            for neighbor in graph.neighbours(current_node):
                if neighbor in unvisited:
                    temp_dist = distance[current_node] \
                                + graph.edge(current_node, neighbor)
                    if temp_dist < distance[neighbor]:
                        distance[neighbor] = temp_dist
                        previous[neighbor] = current_node
            
            unvisited.remove(current_node)


def main() -> None:
    """
    main The main entrypoint into the program

    Generate a graph before running the shortest path first algorithm.
    """

    # (source, dest, correct)
    test_data = [
        (0,1,[0,4,1]),
        (0,2,[0,4,3,2]),
        (0,3,[0,4,3]),
        (0,4,[0,4]),
        (0,5,[0,4,1,6,5]),
        (0,6,[0,4,1,6]),
        (0,7,[0,4,1,6,7]),
        (0,8,[0,4,3,2,8]),
        (0,9,[0,4,1,6,7,9])
    ]

    graph = Graph()
    for i in range(10):
        print(f"Adding node {graph.addNode()}")
    edges = [
        (0,1,6),
        (0,3,4),
        (0,4,2),
        (1,4,3),
        (1,6,5),
        (2,3,3),
        (2,8,10),
        (3,4,1),
        (5,8,5),
        (5,9,3),
        (5,6,6),
        (6,7,2),
        (7,9,2),
        (8,9,9)
        ]

    for edge in edges:
        print(f"Adding edge {edge[0]} to {edge[1]} cost {edge[2]}", end="")
        print(f" with ID {graph.addEdge(edge[0], edge[1], edge[2])}")

    print(graph)
    fail = False
    for test in test_data:
        if (res := dijkstra(graph, test[0], test[1])) != test[2]:
            print(f"Testing {test[0]} to {test[1]}")
            print(f"Failed - Got {res} Expected {test[2]}")
            fail = True
            
    if fail:
        print("Some tests failed")
    else:
        print("All tests passed")


if __name__ == "__main__":
    main()
