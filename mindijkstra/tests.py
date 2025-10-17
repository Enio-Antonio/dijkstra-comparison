from mindijsktra.minddijkstra_alg import *
from mindijsktra.mindijkstra_alg_paths import *

def test_dijkstras_algorithm():
    """
    Test function for Dijkstra's algorithm.

    This test evaluates the correctness of the `dijkstrasAlgorithm` function using a predefined input graph
    and expected output. The graph is represented as an adjacency list, and the test ensures that the
    algorithm computes the shortest paths correctly.

    Input Graph:
        Node 0 -> Node 1 (weight 7)
        Node 1 -> Node 2 (weight 6), Node 3 (weight 20), Node 4 (weight 3)
        Node 2 -> Node 3 (weight 14)
        Node 3 -> Node 4 (weight 2)
        Node 4 -> No outgoing edges
        Node 5 -> No outgoing edges

    Expected Output:
        [0, 7, 13, 27, 10, -1]
        - Shortest distances from node 0 to all other nodes.
        - `-1` represents unreachable nodes (node 5 in this case).

    Assertions:
        The test checks if the result matches the expected output and raises an assertion error otherwise.

    Returns:
        None. Prints "Test passed" if the output is correct.
    """
    # Input graph represented as an adjacency list
    edges = [
        [[1, 7]],                   # Node 0 -> Node 1 (weight 7)
        [[2, 6], [3, 20], [4, 3]],  # Node 1 -> Node 2 (6), Node 3 (20), Node 4 (3)
        [[3, 14]],                  # Node 2 -> Node 3 (weight 14)
        [[4, 2]],                   # Node 3 -> Node 4 (weight 2)
        [],                         # Node 4 has no outgoing edges
        []                          # Node 5 has no outgoing edges
    ]
    start = 0  # Starting node for Dijkstra's algorithm

    # Expected output: Shortest distances from the starting node
    expected_output = [0, 7, 13, 27, 10, -1]

    # Step 1: Run Dijkstra's algorithm on the input graph
    result = minHeapDijkstrasAlgorithm(start, edges)

    # Step 2: Compare the result with the expected output
    assert result == expected_output, f"Test failed: expected {expected_output}, but got {result}"

    # Step 3: If no assertion error, print test success message
    print("Test passed: Output matches expected result.")


# Run the test function
test_dijkstras_algorithm()

def test_dijkstrasAlgorithmWithPaths():
    """
    Test function for the `dijkstrasAlgorithmWithPaths` function.

    This test verifies:
        1. The correctness of the minimum distances calculated by Dijkstra's algorithm.
        2. The correctness of the reconstructed paths using the `reconstructPath` function.

    Input Graph (Adjacency List):
        - Node 0 -> Node 1 (weight 7)
        - Node 1 -> Node 2 (weight 6), Node 3 (weight 20), Node 4 (weight 3)
        - Node 2 -> Node 3 (weight 14)
        - Node 3 -> Node 4 (weight 2)
        - Node 4 has no outgoing edges
        - Node 5 is isolated (no incoming or outgoing edges).

    Expected Results:
        - Minimum Distances:
            [0, 7, 13, 27, 10, float("inf")]
            - Distances from node 0 to all other nodes. `float("inf")` represents unreachable nodes.
        - Reconstructed Paths:
            - Path to node 3: [0, 1, 2, 3]
            - Path to node 4: [0, 1, 4]
            - Path to node 5: []

    Assertions:
        The test uses assertions to ensure that the computed distances and paths match the expected values.

    Returns:
        None. Prints "All tests passed!" if the results are correct.
    """
    # Step 1: Define the input graph as an adjacency list
    edges = [
        [[1, 7]],                   # Node 0 -> Node 1 (weight 7)
        [[2, 6], [3, 20], [4, 3]],  # Node 1 -> Node 2 (6), Node 3 (20), Node 4 (3)
        [[3, 14]],                  # Node 2 -> Node 3 (weight 14)
        [[4, 2]],                   # Node 3 -> Node 4 (weight 2)
        [],                         # Node 4 has no outgoing edges
        []                          # Node 5 has no outgoing edges
    ]
    start = 0  # Starting node for Dijkstra's algorithm

    # Step 2: Run Dijkstra's algorithm
    minDistances, previousNodes = minHeapDijkstrasAlgorithmWithPaths(start, edges)

    # Step 3: Check the minimum distances
    expectedDistances = [0, 7, 13, 27, 10, float("inf")]
    assert minDistances == expectedDistances, f"Distances test failed: {minDistances}"

    # Step 4: Reconstruct paths to specific nodes and validate them
    # Path to node 3
    path_to_3 = reconstructPath(previousNodes, start, 3)
    expectedPathTo3 = [0, 1, 2, 3]
    assert path_to_3 == expectedPathTo3, f"Path to 3 test failed: {path_to_3}"

    # Path to node 4
    path_to_4 = reconstructPath(previousNodes, start, 4)
    expectedPathTo4 = [0, 1, 4]
    assert path_to_4 == expectedPathTo4, f"Path to 4 test failed: {path_to_4}"

    # Path to node 5 (unreachable)
    path_to_5 = reconstructPath(previousNodes, start, 5)
    expectedPathTo5 = []
    assert path_to_5 == expectedPathTo5, f"Path to 5 test failed: {path_to_5}"

    # Step 5: Print success message if all tests pass
    print("All tests passed!")


# Run the test
test_dijkstrasAlgorithmWithPaths()