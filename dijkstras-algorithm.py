from weightedGraph import Graph

def _getPath(source: int, destination: int, prev: list[int]) -> list[int]:
    sequence: list[int] = []
    u = destination
    if prev[u] is not None or u == source:
        while u is not None:
            sequence.insert(0, u)
            u = prev[u]
    return sequence


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

    dist = [float('inf') for i in range(graph.ncount)]
    prev = [None for i in range(graph.ncount)]
    nodes = []
    for node in graph.nodes:
        nodes.append(node)

    dist[source] = 0

    while len(nodes) > 0:
        u = min((val, i) for i, val in enumerate(nodes) if val is not None)[0]
        nodes.remove(u)

        # if u == destination:
        #     break

        for neighbor in graph.neighbours(u):
            alt = dist[u] + graph.edge(u, neighbor)
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = u
    
    return _getPath(source, destination, prev)
            

def main() -> None:
    """
    main The main entrypoint into the program

    Generate a graph before running the shortest path first algorithm.
    """

    # The graph should have the following routes from 0
    # Node 1 - -> 0 4 1
    # Node 2 - -> 0 4 3 2
    # Node 3 - -> 0 4 3
    # Node 4 - -> 0 4
    # Node 5 - -> 0 4 1 6 5
    # Node 6 - -> 0 4 1 6
    # Node 7 - -> 0 4 1 6 7
    # Node 8 - -> 0 4 3 2 8
    # Node 9 - -> 0 4 1 6 7 9

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

    for test in test_data:
        print(f"Testing {test[0]} to {test[1]}")
        if (res := dijkstra(graph, test[0], test[1])) == test[2]:
            print("Passed")
        else:
            print(f"Failed - Got {res} Expected {test[2]}")

if __name__ == "__main__":
    main()
