# O(V^2 + E) time | O(V) space - where V is the number of vertices and E is the number of edges in the input graph
def dijkstrasAlgorithm(start: int, edges: list):
    """
    Implements Dijkstra's algorithm to find the shortest path from a starting node to all other nodes in a graph.

    Args:
        start (int): The starting node index.
        edges (list of list): Adjacency list representing the graph. Each index corresponds to a vertex,
                            and each entry is a list of pairs [destination, weight].

    Returns:
        list: A list of the shortest distances from the starting node to each node. If a node is not reachable,
            the distance is -1.
    """
    numberOfVertices = len(edges)

    # Initialize the minimum distances for all vertices as infinity
    # except the starting vertex which is set to 0.
    minDistances = [float("inf") for _ in range(numberOfVertices)]
    minDistances[start] = 0

    # Keep track of visited nodes to avoid reprocessing them.
    visited = set()

    # Continue processing nodes until all have been visited.
    while len(visited) != numberOfVertices:
        # Find the vertex with the smallest known distance that has not been visited.
        vertex, currentMinDistance = getVertexWithMinDistance(minDistances, visited)

        # If the smallest distance is infinity, all remaining vertices are unreachable.
        if currentMinDistance == float("inf"):
            break

        # Mark the current vertex as visited.
        visited.add(vertex)

        # Iterate through all the neighbors of the current vertex.
        for edge in edges[vertex]:
            destination, distanceToDestination = edge

            # Skip the neighbor if it has already been visited.
            if destination in visited:
                continue

            # Calculate the new potential path distance to the neighbor.
            newPathDistance = currentMinDistance + distanceToDestination
            currentDestinationDistance = minDistances[destination]

            # Update the shortest distance to the neighbor if the new path is shorter.
            if newPathDistance < currentDestinationDistance:
                minDistances[destination] = newPathDistance

    # Replace any remaining infinity distances with -1 to indicate unreachable nodes.
    return list(map(lambda x: -1 if x == float("inf") else x, minDistances))


def getVertexWithMinDistance(distances, visited):
    """
    Helper function to find the vertex with the smallest known distance that has not been visited.

    Args:
        distances (list): A list of the shortest known distances to each vertex.
        visited (set): A set of vertices that have already been visited.

    Returns:
        tuple: The index of the vertex with the smallest distance and its distance value.
    """
    currentMinDistance = float("inf")
    vertex = -1

    # Iterate over all vertices to find the one with the smallest distance.
    for vertexIdx, distance in enumerate(distances):
        # Skip the vertex if it has already been visited.
        if vertexIdx in visited:
            continue

        # Update the current minimum distance and vertex if a smaller distance is found.
        if distance <= currentMinDistance:
            vertex = vertexIdx
            currentMinDistance = distance

    return vertex, currentMinDistance