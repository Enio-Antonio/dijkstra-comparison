from dijkstra.dijkstra_alg import dijkstrasAlgorithm
from dijkstra.dijkstra_alg_paths import *

def test_dijkstras_algorithm():
    # Input graph
    edges = [
        [[1, 7]],           # Node 0 -> Node 1 (weight 7)
        [[2, 6], [3, 20], [4, 3]],  # Node 1 -> Nodes 2 (weight 6), 3 (weight 20), 4 (weight 3)
        [[3, 14]],          # Node 2 -> Node 3 (weight 14)
        [[4, 2]],           # Node 3 -> Node 4 (weight 2)
        [],                 # Node 4 has no outgoing edges
        []                  # Node 5 has no outgoing edges
    ]
    start = 0

    # Expected output
    expected_output = [0, 7, 13, 27, 10, -1]

    # Run Dijkstra's algorithm
    result = dijkstrasAlgorithm(start, edges)

    # Test the result
    assert result == expected_output, f"Test failed: expected {expected_output}, but got {result}"

    print("Test passed: Output matches expected result.")

# Run the test
test_dijkstras_algorithm()

def test_dijkstrasAlgorithmWithPaths():
    # Input graph (adjacency list)
    edges = [
        [[1, 7]],               # Node 0 -> Node 1 (weight 7)
        [[2, 6], [3, 20], [4, 3]],  # Node 1 -> Nodes 2 (6), 3 (20), 4 (3)
        [[3, 14]],              # Node 2 -> Node 3 (weight 14)
        [[4, 2]],               # Node 3 -> Node 4 (weight 2)
        [],                     # Node 4 has no outgoing edges
        []                      # Node 5 has no outgoing edges
    ]
    start = 0  # Starting node

    # Run Dijkstra's algorithm
    minDistances, previousNodes = dijkstrasAlgorithmWithPaths(start, edges)

    # Expected distances
    expectedDistances = [0, 7, 13, 27, 10, float("inf")]
    assert minDistances == expectedDistances, f"Distances test failed: {minDistances}"

    # Reconstruct paths
    path_to_3 = reconstructPath(previousNodes, start, 3)
    expectedPathTo3 = [0, 1, 2, 3]
    assert path_to_3 == expectedPathTo3, f"Path to 3 test failed: {path_to_3}"

    path_to_4 = reconstructPath(previousNodes, start, 4)
    expectedPathTo4 = [0, 1, 4]
    assert path_to_4 == expectedPathTo4, f"Path to 4 test failed: {path_to_4}"

    path_to_5 = reconstructPath(previousNodes, start, 5)
    expectedPathTo5 = []
    assert path_to_5 == expectedPathTo5, f"Path to 5 test failed: {path_to_5}"

    print("All tests passed!")

# Run the test
test_dijkstrasAlgorithmWithPaths()