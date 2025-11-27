import pytest
from main import prim_mst


def normalize_edges(edge_list):
    """
    Convert (u, v, w) to (frozenset({u, v}), w) and sort,
    so that (A, B, w) is the same as (B, A, w).
    """
    return sorted((frozenset((u, v)), w) for (u, v, w) in edge_list)


# Normal tests (4)


def test_simple_triangle():
    graph = {
        "A": [("B", 4), ("C", 1)],
        "B": [("A", 4), ("C", 3)],
        "C": [("A", 1), ("B", 3)],
    }
    mst_edges, total_cost = prim_mst(graph, "A")
    norm = normalize_edges(mst_edges)
    expected = normalize_edges([("A", "C", 1), ("C", "B", 3)])
    assert norm == expected
    assert total_cost == 4


def test_square_graph():
    graph = {
        "A": [("B", 1), ("D", 4)],
        "B": [("A", 1), ("C", 2)],
        "C": [("B", 2), ("D", 1)],
        "D": [("A", 4), ("C", 1)],
    }
    mst_edges, total_cost = prim_mst(graph, "A")
    assert len(mst_edges) == 3
    assert total_cost == 1 + 2 + 1  # 4


def test_chain_graph():
    graph = {
        "G1": [("G2", 2)],
        "G2": [("G1", 2), ("G3", 3)],
        "G3": [("G2", 3), ("G4", 1)],
        "G4": [("G3", 1)],
    }
    mst_edges, total_cost = prim_mst(graph, "G1")
    assert len(mst_edges) == 3
    assert total_cost == 2 + 3 + 1


def test_two_possible_msts_same_cost():
    graph = {
        "A": [("B", 1), ("C", 1)],
        "B": [("A", 1), ("C", 2)],
        "C": [("A", 1), ("B", 2)],
    }
    mst_edges, total_cost = prim_mst(graph, "A")
    assert len(mst_edges) == 2
    assert total_cost == 2


# Edge-case tests (3)


def test_single_node_graph():
    graph = {"Solo": []}
    mst_edges, total_cost = prim_mst(graph, "Solo")
    assert mst_edges == []
    assert total_cost == 0


def test_two_node_graph():
    graph = {
        "A": [("B", 10)],
        "B": [("A", 10)],
    }
    mst_edges, total_cost = prim_mst(graph, "A")
    norm = normalize_edges(mst_edges)
    expected = normalize_edges([("A", "B", 10)])
    assert norm == expected
    assert total_cost == 10


def test_graph_with_heavier_extra_edges():
    graph = {
        "A": [("B", 1), ("C", 10)],
        "B": [("A", 1), ("C", 1)],
        "C": [("A", 10), ("B", 1)],
    }
    mst_edges, total_cost = prim_mst(graph, "A")
    norm = normalize_edges(mst_edges)
    expected = normalize_edges([("A", "B", 1), ("B", "C", 1)])
    assert norm == expected
    assert total_cost == 2


# Complex tests (3)


def test_larger_graph_multiple_branches():
    graph = {
        "H1": [("H2", 3), ("H3", 2)],
        "H2": [("H1", 3), ("H4", 4), ("H5", 6)],
        "H3": [("H1", 2), ("H5", 1)],
        "H4": [("H2", 4), ("H5", 5)],
        "H5": [("H2", 6), ("H3", 1), ("H4", 5)],
    }
    mst_edges, total_cost = prim_mst(graph, "H1")
    assert len(mst_edges) == 4
    # One MST: H1-H3 (2), H3-H5 (1), H1-H2 (3), H2-H4 (4) => 10
    assert total_cost == 10


@pytest.mark.parametrize("start", ["H1", "H2", "H3"])
def test_mst_same_cost_from_any_start(start):
    graph = {
        "H1": [("H2", 3), ("H3", 2)],
        "H2": [("H1", 3), ("H4", 4), ("H5", 6)],
        "H3": [("H1", 2), ("H5", 1)],
        "H4": [("H2", 4), ("H5", 5)],
        "H5": [("H2", 6), ("H3", 1), ("H4", 5)],
    }
    mst_edges, total_cost = prim_mst(graph, start)
    assert len(mst_edges) == len(graph) - 1
    assert total_cost == 10


def test_graph_with_many_edges():
    graph = {
        "A": [("B", 3), ("C", 1), ("D", 4)],
        "B": [("A", 3), ("C", 2), ("D", 5)],
        "C": [("A", 1), ("B", 2), ("D", 1)],
        "D": [("A", 4), ("B", 5), ("C", 1)],
    }
    mst_edges, total_cost = prim_mst(graph, "A")
    assert len(mst_edges) == 3
    assert total_cost == 4  # Correct MST cost: C-D(1), A-C(1), C-B(2)
