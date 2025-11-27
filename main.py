
from heapq import heappush, heappop


def prim_mst(graph, start):
    """
    Build a Minimum Spanning Tree (MST) using Prim's algorithm.

    Parameters
    - graph: dict[str, list[tuple[str, int|float]]] adjacency list of an undirected graph
             Each entry maps a node to a list of (neighbor, weight) pairs.
    - start: starting node for the algorithm. Assumed to exist in `graph`.

    Returns
    - (mst_edges, total_cost):
        mst_edges: list of (u, v, w) edges chosen for the MST
        total_cost: sum of the weights of those edges
    """

    if start not in graph:
        raise KeyError(f"Start node '{start}' not in graph")
    if len(graph) == 1:
        return [], 0

    visited = set([start])
    mst_edges = []
    total_cost = 0

    # Min-heap of candidate edges: (weight, u, v)
    heap = []
    for v, w in graph.get(start, []):
        heappush(heap, (w, start, v))

    # Extract the smallest edge that connects to an unvisited node
    while heap and len(visited) < len(graph):
        w, u, v = heappop(heap)
        if v in visited:
            continue
        # Accept this edge into the MST
        visited.add(v)
        mst_edges.append((u, v, w))
        total_cost += w
        # Push all frontier edges from the newly added node
        for nv, nw in graph.get(v, []):
            if nv not in visited:
                heappush(heap, (nw, v, nv))

    return mst_edges, total_cost


if __name__ == "__main__":
    # Optional manual test
    sample_graph = {
        "G1": [("G2", 4), ("G3", 2)],
        "G2": [("G1", 4), ("G3", 3)],
        "G3": [("G1", 2), ("G2", 3)],
    }
    edges, cost = prim_mst(sample_graph, "G1")
    print("Sample MST edges:", edges)
    print("Total cost:", cost)
