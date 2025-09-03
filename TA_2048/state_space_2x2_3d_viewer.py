"""
2x2 2048 State-Space — Symmetry-Reduced Static 3D Visualization (PyVista + VTK)
with Dynamic-Programming Expected Score labels.

Heavily vibecoed
"""

import math
from collections import deque, defaultdict
from functools import lru_cache

import numpy as np
import networkx as nx

# -----------------------------
# Configuration
# -----------------------------
NODE_POINT_SIZE = 40.0
ALL_EDGE_WIDTH   = 1.0
ALL_EDGE_ALPHA   = 0   # thin/faint background context
SKELETON_WIDTH   = 3.0
SKELETON_ALPHA   = 0.65   # bright foreground skeleton

BACKGROUND_COLOR = "black"
EDGE_COLOR       = "white"
SKELETON_COLOR   = "cyan"   # accent color for skeleton/MST

TEXT_OFFSET      = 0.12     # label height offset

# -----------------------------
# 2048 Logic
# -----------------------------
def move_board(board, direction):
    b = [list(board[:2]), list(board[2:])]
    changed = False
    if direction in (0, 1):  # left/right
        new_rows = []
        for row in b:
            r = row[::-1] if direction == 1 else row[:]
            vals = [x for x in r if x != 0]
            merged, i = [], 0
            while i < len(vals):
                if i + 1 < len(vals) and vals[i] == vals[i + 1]:
                    merged.append(vals[i] + 1)
                    i += 2
                    changed = True
                else:
                    merged.append(vals[i]); i += 1
            merged += [0] * (2 - len(merged))
            if direction == 1: merged = merged[::-1]
            if merged != row: changed = True
            new_rows.append(merged)
        new_b = new_rows
    else:  # up/down
        cols = [[b[0][0], b[1][0]], [b[0][1], b[1][1]]]
        new_cols = []
        for col in cols:
            c = col[::-1] if direction == 3 else col[:]
            vals = [x for x in c if x != 0]
            merged, i = [], 0
            while i < len(vals):
                if i + 1 < len(vals) and vals[i] == vals[i + 1]:
                    merged.append(vals[i] + 1); i += 2; changed = True
                else:
                    merged.append(vals[i]); i += 1
            merged += [0] * (2 - len(merged))
            if direction == 3: merged = merged[::-1]
            new_cols.append(merged)
        new_b = [[new_cols[0][0], new_cols[1][0]],
                 [new_cols[0][1], new_cols[1][1]]]
        if new_b != b: changed = True
    return tuple(new_b[0] + new_b[1]), changed

def spawn_children(board):
    """All possible random spawns after a move, with probabilities."""
    empties = [i for i, x in enumerate(board) if x == 0]
    n = len(empties)
    children = []
    for pos in empties:
        for exp, p in [(1, 0.9), (2, 0.1)]:
            nb = list(board); nb[pos] = exp
            children.append((tuple(nb), p/n))
    return children

def board_score(board):
    return sum((x-1) * (1<<x) if x > 0 else 0 for x in board)

# -----------------------------
# Symmetry
# -----------------------------
TRANSFORMS = [
    (0,1,2,3),(2,0,3,1),(3,2,1,0),(1,3,0,2),
    (1,0,3,2),(2,3,0,1),(0,2,1,3),(3,1,2,0)
]
def apply_perm(board, perm): return tuple(board[i] for i in perm)
def canonical(board): return min(apply_perm(board,p) for p in TRANSFORMS)

# -----------------------------
# Expected score (DP with memoization)
# -----------------------------
@lru_cache(None)
def expected_score(board):
    # If no moves are possible, return current board score
    if all(not move_board(board, d)[1] for d in range(4)):
        return board_score(board)

    best = -1e9
    for d in range(4):
        moved, changed = move_board(board, d)
        if not changed: continue
        total = 0.0
        for child, prob in spawn_children(moved):
            total += prob * expected_score(canonical(child))
        best = max(best, total)
    return best

# -----------------------------
# Enumerate quotient graph under symmetry
# -----------------------------
# def enumerate_reachable_states_sym():
#     init_raw = set()
#     for i in range(4):
#         for j in range(i+1,4):
#             for vi in (1,2):
#                 for vj in (1,2):
#                     s = [0,0,0,0]
#                     s[i] = vi; s[j] = vj
#                     init_raw.add(tuple(s))
#     init = {canonical(s) for s in init_raw}
#     print(init)

#     visited, q = set(init), list(init)
#     edges = defaultdict(int)

#     while q:
#         s = q.pop()
#         for d in range(4):
#             moved, changed = move_board(s, d)
#             if not changed:
#                 continue
#             for child, _ in spawn_children(moved):
#                 u = canonical(s)
#                 v = canonical(child)
#                 if u != v:
#                     edges[(u, v)] += 1   # keep directed edge
#                 if v not in visited:
#                     visited.add(v)
#                     q.append(v)

#     nodes = list(visited)
#     idx = {s:i for i,s in enumerate(nodes)}
#     # print(idx[(1, 3, 4, 3)], idx[(1, 1, 4, 4)])
#     edges_w = [(idx[u], idx[v], w) for (u,v),w in edges.items()]

#     labels = {}
#     for s, i in idx.items():
#         arr = np.array(s, dtype=np.int32)
#         labels[i] = {
#             "state": s,
#             "max_tile": int(arr.max(initial=0)),
#             "nnz": int((arr>0).sum()),
#             "sum_exp": int(arr.sum()),
#             "expected_score": expected_score(s)
#         }
#     return nodes, edges_w, labels


def enumerate_reachable_states_sym():
    init_raw = set()
    for i in range(4):
        for j in range(i+1,4):
            for vi in (1,2):
                for vj in (1,2):
                    s = [0,0,0,0]
                    s[i] = vi; s[j] = vj
                    init_raw.add(tuple(s))
    init = {canonical(s) for s in init_raw}

    visited, q = set(init), list(init)
    edges = defaultdict(float)  # accumulate probabilities on directed edges

    while q:
        s = q.pop()
        for d in range(4):
            moved, changed = move_board(s, d)
            if not changed:
                continue
            moved_can = canonical(moved)
            for child, prob in spawn_children(moved_can):
                v = canonical(child)
                if s != v:
                    edges[(s, v)] = 1
                if v not in visited:
                    visited.add(v)
                    q.append(v)

    nodes = list(visited)
    idx = {s:i for i,s in enumerate(nodes)}
    edges_w = [(idx[u], idx[v], w) for (u,v),w in edges.items()]

    labels = {}
    for i,s in enumerate(nodes):
        arr = np.array(s, dtype=np.int32)
        labels[i] = {
            "state": s,
            "max_tile": int(arr.max(initial=0)),
            "nnz": int((arr>0).sum()),
            "sum_exp": int(arr.sum()),
            "expected_score": expected_score(s)
        }
    return nodes, edges_w, labels

# -----------------------------
# 3D Layout
# -----------------------------
def layout_3d(n, edges_w):
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for u,v,w in edges_w: G.add_edge(u,v,weight=float(w))
    try:
        pos = nx.spring_layout(G, dim=3, weight="weight", scale=1.0)
    except Exception:
        pos = nx.spring_layout(G, dim=3, weight="weight", iterations=300)
    xyz = np.array([pos[i] for i in range(n)],dtype=np.float32)
    xyz -= xyz.mean(0,keepdims=True)
    m=float(np.abs(xyz).max())
    if m>0: xyz/=m
    xyz*=1.5
    return xyz,G

# -----------------------------
# Build line polydata helpers
# -----------------------------
def build_lines_polydata(xyz, edges_idx):
    import pyvista as pv
    if not edges_idx: return None
    n=len(edges_idx)
    pts=np.empty((2*n,3),dtype=np.float32)
    conn=np.empty((n,3),dtype=np.int64)
    for i,(u,v) in enumerate(edges_idx):
        pts[2*i]=xyz[u]; pts[2*i+1]=xyz[v]
        conn[i]=(2,2*i,2*i+1)
    poly=pv.PolyData()
    poly.points=pts; poly.lines=conn.ravel()
    return poly

def maximum_spanning_edges(G):
    T=nx.maximum_spanning_tree(G,weight="weight")
    return list(T.edges())

# -----------------------------
# Main
# -----------------------------
def main():
    print("Enumerating symmetry-reduced reachable states...")
    nodes, edges_w, labels = enumerate_reachable_states_sym()
    print(nodes, edges_w)
    print(f"Canonical states: {len(nodes)} | Canonical edges: {len(edges_w)}")

    print("Computing 3D graph layout...")
    xyz,G=layout_3d(len(nodes),edges_w)

    scalars=np.array([labels[i]["max_tile"] for i in range(len(nodes))],dtype=np.float32)
    edges_all=[(u,v) for (u,v,w) in edges_w]
    # print((64, 69) in edges_all)
    edges_skel=maximum_spanning_edges(G)

    import pyvista as pv
    pv.set_plot_theme("document")
    pl=pv.Plotter(window_size=(1280,800))
    pl.background_color=BACKGROUND_COLOR

    # Nodes as spheres
    cloud=pv.PolyData(xyz)
    pl.add_points(
        cloud, render_points_as_spheres=True, point_size=NODE_POINT_SIZE,
        scalars=scalars, cmap="plasma", opacity=1,
        show_scalar_bar=True,
        scalar_bar_args=dict(title="Max Tile (log2)", color="white"),
    )

    # Expected score labels
    pl.add_point_labels(
        xyz,
        [f"{labels[i]['expected_score']:.0f} {[2**x if x else 0 for x in nodes[i]]}" for i in range(len(nodes))],
        font_size=30,
        text_color="white",
        point_color=None,
        shape=None
    )

    # Edges
    poly_all=build_lines_polydata(xyz,edges_all)
    if poly_all is not None:
        pl.add_mesh(poly_all,line_width=ALL_EDGE_WIDTH,opacity=ALL_EDGE_ALPHA,color=EDGE_COLOR)
    poly_skel=build_lines_polydata(xyz,edges_skel)
    if poly_skel is not None:
        pl.add_mesh(poly_skel,line_width=SKELETON_WIDTH,opacity=SKELETON_ALPHA,color=SKELETON_COLOR)

    # Floor grid
    grid=pv.Plane(center=(0,0,-1.2),i_size=6,j_size=6,i_resolution=10,j_resolution=10)
    pl.add_mesh(grid,style="wireframe",opacity=0,color="white")

    pl.camera_position=[(2.4,2.0,2.2),(0,0,0),(0,0,1)]
    pl.camera.zoom(1.2)
    pl.show()

if __name__=="__main__":
    main()
