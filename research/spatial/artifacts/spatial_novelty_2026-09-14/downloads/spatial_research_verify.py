#!/usr/bin/env python3
"""Spatial mathematical exploration: reproducible exact verification.
Date: 2026 09 14. Requires only the Python standard library.

Usage:
  python spatial_research_verify.py all
  python spatial_research_verify.py intervals --sizes 3 4 5 --max-endpoint 6
  python spatial_research_verify.py intervals --help
  python spatial_research_verify.py trees
  python spatial_research_verify.py fixed

With no mode argument, runs all checks. Interval options also apply to `all`.

Interval checks exhaustively enumerate multisets of closed integer-endpoint
intervals within the requested range; repeated and singleton intervals are
allowed. An independent endpoint oracle checks the O(n log n) adaptive-radius
formula, while an optimal robust MBST and constructive certificates check the
strengthened bound on the interval adaptivity gap. All interval computations
use integers.

Tree checks use direct edge-distance formulas, without the landmark projection
identity, as an independent oracle. Exact Fraction polytope optimization and
affine arrangements cover entire edges for each of the 80 specified weighted
trees with vertex landmarks (5 designated cases and 75 cases from seed
20260914). They check the ambiguity diameter, inverse Lipschitz constant, and
leaf-landmark dominance. No floating point comparisons or grid sampling are
used. Tree results are written to tree_verification_results.json beside this
script.

The fixed mode checks the O(n log n) robust fixed-tree algorithm against
complete-graph Kruskal, direct Prufer tree enumeration, and seeded integer
and rational instances; it also checks the returned robust-weight MST.

These finite, reproducible checks support the accompanying general proofs;
they neither prove the claims for all instances nor constitute a formal proof.
"""

# ===== Independent interval implementation =====
from argparse import ArgumentParser
from collections import deque
from itertools import combinations_with_replacement, product
from math import comb
import json


def robust_distance(first, second):
    a, b = first
    c, d = second
    return max(abs(a - d), abs(b - c))


def adaptive_radius(family):
    """Exact: moving each side of a maximal gap outward preserves its gap."""
    if len(family) <= 1:
        return 0
    return max(
        max(right - left for left, right in zip(ordered, ordered[1:]))
        for endpoints in product(*family)
        for ordered in [sorted(endpoints)]
    )


def adaptive_radius_fast(family):
    """Exact O(n log n) formula via maximal-gap cuts, checked against endpoints."""
    n = len(family)
    if n <= 1:
        return 0
    ordered = sorted(family)
    suffix_min = [0] * n
    suffix_min[-1] = ordered[-1][1]
    for i in range(n - 2, -1, -1):
        suffix_min[i] = min(ordered[i][1], suffix_min[i + 1])
    answer = max(0, max(suffix_min[k + 1] - ordered[k][0]
                        for k in range(n - 1)))
    for j, (a, b) in enumerate(ordered):
        largest_other_a = ordered[-2][0] if j == n - 1 else ordered[-1][0]
        answer = max(answer, b - largest_other_a)
    return answer


def fixed_radius(family):
    """Kruskal on pairwise worst distances; MST is a bottleneck MST."""
    n = len(family)
    if n <= 1:
        return 0
    parent = list(range(n))
    remaining = n

    def root(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    edges = sorted(
        (robust_distance(family[i], family[j]), i, j)
        for i in range(n) for j in range(i)
    )
    for weight, i, j in edges:
        u, v = root(i), root(j)
        if u != v:
            parent[u] = v
            remaining -= 1
        if remaining == 1:
            return weight
    raise AssertionError("Complete graph did not become connected")


def shortest_path(adjacency, starts, targets):
    queue = deque(starts)
    predecessor = {vertex: None for vertex in starts}
    target_set = set(targets)
    while queue:
        vertex = queue.popleft()
        if vertex in target_set:
            path = []
            while vertex is not None:
                path.append(vertex)
                vertex = predecessor[vertex]
            return path[::-1]
        for neighbor in adjacency[vertex]:
            if neighbor not in predecessor:
                predecessor[neighbor] = vertex
                queue.append(neighbor)
    raise AssertionError("No path between endpoint neighbor sets")


def constructive_tree(family, radius):
    """Return a fixed tree and the proved bound, asserting all certificates.

    Short core: intervals of length <= radius. Long intervals become leaves.
    The proof gives a sharper factor ceil((m+1)/2), m = core size, if any
    long interval is present, and factor 1 if all intervals are short.
    """
    n = len(family)
    if n <= 1:
        return [], 0
    if radius == 0:
        assert all(a == b == family[0][0] for a, b in family)
        return [(0, i) for i in range(1, n)], 0

    core = [i for i, (a, b) in enumerate(family) if b - a <= radius]
    long = [i for i, (a, b) in enumerate(family) if b - a > radius]
    assert core, "A robustly connected family must have a short interval"
    adjacency = {
        i: [j for j in core if j != i and
            robust_distance(family[i], family[j]) <= radius]
        for i in core
    }
    tree = []
    seen = {core[0]}
    queue = deque([core[0]])
    while queue:
        vertex = queue.popleft()
        for neighbor in adjacency[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                tree.append((vertex, neighbor))
                queue.append(neighbor)
    assert seen == set(core), "The short core must have a fixed radius tree"

    for i in long:
        a, b = family[i]
        starts = [j for j in core if
                  robust_distance((a, a), family[j]) <= radius]
        targets = [j for j in core if
                   robust_distance((b, b), family[j]) <= radius]
        assert starts and targets, "Each endpoint has a guaranteed core neighbor"
        path = shortest_path(adjacency, starts, targets)
        # Augmented path: endpoint a, core path vertices, endpoint b.
        # Its edge count is len(path)+1; this is an interior central vertex.
        center = path[(len(path) - 1) // 2]
        assert robust_distance(family[i], family[center]) <= \
            ((len(path) + 2) // 2) * radius
        tree.append((i, center))

    factor = (len(core) + 2) // 2 if long else 1
    bound = factor * radius
    assert len(tree) == n - 1
    assert max(robust_distance(family[i], family[j]) for i, j in tree) <= bound
    assert bound <= ((n + 1) // 2) * radius
    return tree, bound


def run_intervals():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", nargs="+", type=int, default=[3, 4, 5])
    parser.add_argument("--max-endpoint", type=int, default=6)
    options = parser.parse_args()
    regions = [(a, b) for a in range(options.max_endpoint + 1)
               for b in range(a, options.max_endpoint + 1)]
    total = 0
    for n in options.sizes:
        count = zero = violations = 0
        numerator, denominator, example = 0, 1, None
        for family in combinations_with_replacement(regions, n):
            count += 1
            adaptive = adaptive_radius(family)
            assert adaptive_radius_fast(family) == adaptive
            fixed = fixed_radius(family)
            tree, bound = constructive_tree(family, adaptive)
            assert fixed <= bound
            if adaptive == 0:
                zero += 1
            if fixed > ((n + 1) // 2) * adaptive:
                violations += 1
            if adaptive and fixed * denominator > numerator * adaptive:
                numerator, denominator, example = fixed, adaptive, family
        assert count == comb(len(regions) + n - 1, n)
        total += count
        print(json.dumps({
            "n": n, "families": count, "zero_adaptive_radius": zero,
            "violations": violations,
            "maximum_ratio_fraction": [numerator, denominator],
            "first_maximizer": example,
            "constructive_certificates_verified": count,
        }, ensure_ascii=False))
    print(json.dumps({"total_families": total}))


# ===== Independent tree implementation =====
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import random


class Tree:
    def __init__(self, edges):
        self.edges = [(a, b, Q(w)) for a, b, w in edges]
        self.n = 1 + max(max(a, b) for a, b, _ in edges)
        self.adj = [[] for _ in range(self.n)]
        for a, b, w in self.edges:
            self.adj[a].append((b, w))
            self.adj[b].append((a, w))
        self.d = []
        for start in range(self.n):
            row = [None] * self.n
            row[start] = Q(0)
            stack = [(start, -1)]
            while stack:
                v, p = stack.pop()
                for u, w in self.adj[v]:
                    if u != p:
                        row[u] = row[v] + w
                        stack.append((u, v))
            self.d.append(row)
        self.diameter = max(map(max, self.d))

    def sensor_affine(self, e, s):
        a, b, w = self.edges[e]
        if self.d[a][s] < self.d[b][s]:
            return Q(1), self.d[a][s]
        return Q(-1), w + self.d[b][s]

    def edge_regions(self, e, f, sensors):
        a, b, le = self.edges[e]
        c, d, lf = self.edges[f]
        constraints = [(-1, 0, 0), (1, 0, le), (0, -1, 0), (0, 1, lf)]
        affines = []
        for s in sensors:
            ax, bx = self.sensor_affine(e, s)
            ay, by = self.sensor_affine(f, s)
            z = (ax, -ay, bx - by)
            affines.extend([z, tuple(-t for t in z)])
        if e == f:
            return [
                (constraints + [(-1, 1, 0)], (1, -1, 0), affines),
                (constraints + [(1, -1, 0)], (-1, 1, 0), affines),
            ]
        candidates = [(1, 1, self.d[a][c]),
                      (1, -1, lf + self.d[a][d]),
                      (-1, 1, le + self.d[b][c]),
                      (-1, -1, le + lf + self.d[b][d])]
        distance = min(candidates, key=lambda z: value(z, (le / 2, lf / 2)))
        return [(constraints, distance, affines)]


def value(z, p):
    return z[0] * p[0] + z[1] * p[1] + z[2]


def vertices(lines, domain):
    answer = set()
    for (a, b, c), (u, v, w) in combinations(lines, 2):
        determinant = a * v - b * u
        if not determinant:
            continue
        x = Q(c * v - b * w) / determinant
        y = Q(a * w - c * u) / determinant
        if all(i * x + j * y <= k for i, j, k in domain):
            answer.add((x, y))
    return answer


def arrangement_vertices(domain, affines):
    lines = list(domain)
    for a, b in combinations(affines, 2):
        line = (a[0] - b[0], a[1] - b[1], b[2] - a[2])
        if line[0] or line[1]:
            lines.append(line)
    return vertices(lines, domain)


def oracle_c(tree, sensors):
    result = Q(1)
    for e in range(len(tree.edges)):
        for f in range(e, len(tree.edges)):
            for domain, distance, affines in tree.edge_regions(e, f, sensors):
                for p in arrangement_vertices(domain, affines):
                    d = value(distance, p)
                    if d > 0:
                        result = min(result, max(value(z, p) for z in affines) / d)
    return result


def oracle_A(tree, sensors, delta):
    result = Q(0)
    for e in range(len(tree.edges)):
        for f in range(e, len(tree.edges)):
            for domain, distance, affines in tree.edge_regions(e, f, sensors):
                feasible = domain + [(a, b, delta - c) for a, b, c in affines]
                for p in vertices(feasible, feasible):
                    result = max(result, value(distance, p))
    return result


def hull_vertices(tree, sensors):
    hull = set(sensors)
    for s, t in combinations(sensors, 2):
        hull.update(v for v in range(tree.n)
                    if tree.d[s][v] + tree.d[v][t] == tree.d[s][t])
    return hull


def structural_data(tree, sensors):
    hull = hull_vertices(tree, sensors)
    roots = {}
    branch_heights = []

    def visit(v, parent):
        child_heights = sorted([w + visit(u, v) for u, w in tree.adj[v]
                                if u != parent and u not in hull], reverse=True)
        if len(child_heights) >= 2:
            branch_heights.append((v, child_heights[0], child_heights[1]))
        return child_heights[0] if child_heights else Q(0)

    for v in hull:
        h = visit(v, -1)
        if h > 0:
            roots[v] = h
    return hull, roots, branch_heights


def predicted_c(tree, roots, branches):
    if branches:
        return Q(0)
    return min([Q(1)] + [tree.d[b][c] / (tree.d[b][c] + 2 * min(h, k))
                        for (b, h), (c, k) in combinations(roots.items(), 2)])


def predicted_A(tree, roots, branches, delta):
    terms = [min(delta, tree.diameter)]
    for (b, h), (c, k) in combinations(roots.items(), 2):
        d = tree.d[b][c]
        if d <= delta:
            terms.append(min(d + h + k, delta + 2 * min(h, k)))
    for _, h, k in branches:
        terms.append(min(h + k, delta + 2 * min(h, k)))
    return max(terms)


def dominating_leaf_sensors(tree, sensors):
    hull = hull_vertices(tree, sensors)
    if len(hull) < 2:
        return None
    selected = []
    for v in hull:
        if sum(u in hull for u, _ in tree.adj[v]) != 1:
            continue
        reachable = []
        stack = [(v, -1)]
        while stack:
            u, parent = stack.pop()
            if len(tree.adj[u]) == 1:
                reachable.append(u)
            stack.extend((z, u) for z, _ in tree.adj[u]
                         if z != parent and z not in hull)
        selected.append(min(reachable))
    assert len(set(selected)) == len(selected) <= len(sensors)
    assert hull <= hull_vertices(tree, selected)
    return selected


def verify_dominance(tree, old, new):
    # Both observation norms are affine on the common full arrangement.
    # Therefore checking its vertices proves the inequality for this tree.
    checked = 0
    for e in range(len(tree.edges)):
        for f in range(e, len(tree.edges)):
            old_regions = tree.edge_regions(e, f, old)
            new_regions = tree.edge_regions(e, f, new)
            for (domain, _, a), (_, _, b) in zip(old_regions, new_regions):
                for p in arrangement_vertices(domain, a + b):
                    assert max(value(z, p) for z in a) <= max(value(z, p) for z in b)
                    checked += 1
    return checked


def run():
    rng = random.Random(20260914)
    cases = [
        ([(0, 1, 1), (1, 2, 1), (2, 3, 1), (1, 4, 10), (2, 5, 10)], [0, 3], "21-fold example"),
        ([(0, 1, 2), (1, 2, 3), (1, 3, 5)], [0], "noninjective tripod"),
        ([(0, 1, 2), (1, 2, 3)], [0], "single endpoint sensor"),
        ([(0, 1, 2), (1, 2, 3)], [1], "single interior sensor"),
        ([(0, 1, 2), (1, 2, 3), (1, 3, 5), (3, 4, 4), (3, 5, 2)], [0, 2], "deep outside branching"),
    ]
    for index in range(75):
        n = rng.randint(3, 8)
        edges = [(rng.randrange(v), v, rng.randint(1, 6)) for v in range(1, n)]
        sensors = sorted(rng.sample(range(n), rng.randint(1, n)))
        cases.append((edges, sensors, f"seeded random {index}"))
    reports = []
    count_A = 0
    dominance_vertices = 0
    injective = 0
    for edges, sensors, label in cases:
        tree = Tree(edges)
        hull, roots, branches = structural_data(tree, sensors)
        actual_c = oracle_c(tree, sensors)
        expect_c = predicted_c(tree, roots, branches)
        assert actual_c == expect_c, (label, "c", actual_c, expect_c)
        injective += not bool(branches)
        thresholds = {Q(0), Q(1, 2), Q(1), tree.diameter / 3, tree.diameter / 2,
                      tree.diameter, tree.diameter + 1}
        for b, c in combinations(roots, 2):
            d = tree.d[b][c]
            thresholds.update({d, max(Q(0), d - Q(1, 2)), d + Q(1, 2)})
        for delta in sorted(thresholds):
            actual_A = oracle_A(tree, sensors, delta)
            expect_A = predicted_A(tree, roots, branches, delta)
            assert actual_A == expect_A, (label, "A", delta, actual_A, expect_A)
            count_A += 1
        new_sensors = dominating_leaf_sensors(tree, sensors)
        if new_sensors is not None:
            dominance_vertices += verify_dominance(tree, sensors, new_sensors)
        reports.append({"name": label, "edges": edges, "sensors": sensors,
                        "c": str(actual_c), "injective": not bool(branches),
                        "thresholds_checked": len(thresholds),
                        "dominating_leaf_sensors": new_sensors})
        if len(reports) % 10 == 0:
            print(f"Validated {len(reports)} / {len(cases)} trees", flush=True)
    results = {
        "seed": 20260914,
        "trees_checked": len(cases),
        "injective_cases": injective,
        "noninjective_cases": len(cases) - injective,
        "exact_continuous_c_checks": len(cases),
        "exact_continuous_A_checks": count_A,
        "exact_dominance_arrangement_vertices_checked": dominance_vertices,
        "mismatches": 0,
        "method": "Direct edge-distance affine formulas; exact Fraction arrangement and polytope vertex enumeration",
        "scope": "Finite listed weighted trees with vertex sensors; no grid sampling; does not replace general proof",
        "cases": reports,
    }
    out = Path(__file__).with_name("tree_verification_results.json")
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in results.items() if k != "cases"}, indent=2))





# ===== Fixed robust MST: center-sorted Boruvka and independent checks =====
from fractions import Fraction

def _offer(two, value, vertex, color):
    """Keep the two smallest (value, vertex) entries of distinct colors."""
    entries = sorted(two + [(value, vertex, color)])
    out = []
    for entry in entries:  # At most three entries: constant time.
        if all(entry[2] != previous[2] for previous in out):
            out.append(entry)
            if len(out) == 2:
                break
    return out


def robust_fixed_fast(intervals):
    """Return (RF, MST_edges, round_component_counts).

    Each edge is (weight, smaller_label, larger_label). Original label indices
    are preserved. The returned tree also minimizes the SUM of robust edge
    weights, which implies its maximum edge is the optimal bottleneck RF.
    n=1 is assigned RF=0 and the empty tree; n=0 is rejected.
    """
    n = len(intervals)
    if not n or any(a > b for a, b in intervals):
        raise ValueError("Expected nonempty bounded closed intervals, n >= 1")
    order = sorted(range(n), key=lambda i: (sum(intervals[i]), i))
    colors = list(range(n))
    count = n
    tree = []
    counts = [count]

    while count > 1:
        best = [None] * count
        for reverse in (False, True):
            two = []
            for i in (reversed(order) if reverse else order):
                color = colors[i]
                # The smallest stored entry outside this component, if present.
                eligible = next((entry for entry in two if entry[2] != color), None)
                if eligible is not None:
                    _, j, _ = eligible
                    # Center-sorted i_left,j_right imply w=b_right-a_left.
                    weight = intervals[j][1] - intervals[i][0] if reverse else intervals[i][1] - intervals[j][0]
                    edge = (weight, min(i, j), max(i, j))
                    if best[color] is None or edge < best[color]:
                        best[color] = edge
                value = intervals[i][1] if reverse else -intervals[i][0]
                two = _offer(two, value, i, color)

        # All components have at least one outgoing edge in the complete graph.
        assert all(edge is not None for edge in best)
        adjacency = [[] for _ in range(count)]
        for edge in best:
            _, i, j = edge
            u, v = colors[i], colors[j]
            adjacency[u].append((v, edge))
            adjacency[v].append((u, edge))

        # Traverse the chosen-edge forest (allowing duplicate undirected edges).
        # Assign dense new component IDs in O(number of old components).
        new_color = [-1] * count
        new_count = 0
        for root in range(count):
            if new_color[root] >= 0:
                continue
            new_color[root] = new_count
            stack = [root]
            while stack:
                u = stack.pop()
                for v, edge in adjacency[u]:
                    if new_color[v] < 0:
                        new_color[v] = new_count
                        tree.append(edge)
                        stack.append(v)
            new_count += 1
        assert new_count * 2 <= count
        colors = [new_color[color] for color in colors]
        count = new_count
        counts.append(count)

    assert len(tree) == n - 1
    return max((edge[0] for edge in tree), default=0), tree, counts


def robust_fixed_complete(intervals):
    """Independent full-edge Kruskal oracle, O(n^2 log n)."""
    n = len(intervals)
    edges = sorted((max(bi - aj, bj - ai), i, j)
                   for i, (ai, bi) in enumerate(intervals)
                   for j, (aj, bj) in enumerate(intervals) if i < j)
    parents = list(range(n))

    def find(i):
        while parents[i] != i:
            parents[i] = parents[parents[i]]
            i = parents[i]
        return i

    tree = []
    for edge in edges:
        _, i, j = edge
        u, v = find(i), find(j)
        if u != v:
            parents[u] = v
            tree.append(edge)
            if len(tree) == n - 1:
                break
    return max((edge[0] for edge in tree), default=0), tree


def robust_fixed_prufer(intervals):
    """Third oracle: enumerate labeled trees, directly minimize bottleneck."""
    n = len(intervals)
    if n == 1:
        return 0
    answer = None
    for code in product(range(n), repeat=n - 2):
        degree = [1] * n
        for v in code:
            degree[v] += 1
        weights = []
        for v in code:
            u = next(j for j in range(n) if degree[j] == 1)
            weights.append(max(intervals[u][1] - intervals[v][0], intervals[v][1] - intervals[u][0]))
            degree[u] -= 1
            degree[v] -= 1
        u, v = [j for j in range(n) if degree[j] == 1]
        weights.append(max(intervals[u][1] - intervals[v][0], intervals[v][1] - intervals[u][0]))
        value = max(weights)
        answer = value if answer is None else min(answer, value)
    return answer


def _rf_check(intervals, use_prufer=False):
    value, edges, counts = robust_fixed_fast(intervals)
    expected, expected_edges = robust_fixed_complete(intervals)
    assert value == expected, (intervals, value, expected)
    assert sum(edge[0] for edge in edges) == sum(edge[0] for edge in expected_edges), intervals
    # Common total edge ordering yields the same unique tie-broken MST.
    assert sorted(edges) == sorted(expected_edges), intervals
    assert all(max(intervals[i][1] - intervals[j][0], intervals[j][1] - intervals[i][0]) == weight
               for weight, i, j in edges)
    assert all(2 * after <= before for before, after in zip(counts, counts[1:]))
    if use_prufer:
        assert value == robust_fixed_prufer(intervals), intervals


def run_fixed_fast():
    universe = [(a, b) for a in range(7) for b in range(a, 7)]
    exhaustive = {}
    for n in (2, 3, 4):
        total = 0
        for intervals in combinations_with_replacement(universe, n):
            _rf_check(intervals)
            total += 1
        exhaustive[n] = total

    # Independent direct minimax oracle, with label permutations and ties.
    small_universe = [(a, b) for a in range(5) for b in range(a, 5)]
    prufer_total = 0
    for n in (2, 3, 4):
        for intervals in combinations_with_replacement(small_universe, n):
            _rf_check(intervals, use_prufer=True)
            prufer_total += 1

    rng = random.Random(20260914)
    random_total = 2500
    for _ in range(random_total):
        n = rng.randrange(2, 51)
        intervals = []
        for i in range(n):
            a, b = sorted((rng.randrange(-100, 101), rng.randrange(-100, 101)))
            intervals.append((a, b))
        rng.shuffle(intervals)
        _rf_check(intervals)

    rational_total = 200
    for _ in range(rational_total):
        n = rng.randrange(2, 20)
        intervals = [tuple(sorted((Fraction(rng.randrange(-30, 31), rng.randrange(1, 11)),
                                   Fraction(rng.randrange(-30, 31), rng.randrange(1, 11)))))
                     for i in range(n)]
        _rf_check(intervals)
    _rf_check([(0, 0)])
    _rf_check([(0, 0)] * 50)
    _rf_check([(-i, i) for i in range(50)])
    _rf_check([(i, i) for i in range(50)])

    result = {
        "algorithm": "center-sorted two-color Boruvka, O(n log n) arithmetic/comparison operations, O(n) space",
        "exhaustive_integer_multisets_endpoints_0_to_6": exhaustive,
        "exhaustive_total": sum(exhaustive.values()),
        "prufer_crosschecks_endpoints_0_to_4": prufer_total,
        "random_integer_labelled_families": random_total,
        "random_rational_labelled_families": rational_total,
        "handpicked_degenerate_cases": 4,
        "mismatches": 0,
        "seed": 20260914,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result




if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode not in {"all", "intervals", "trees", "fixed"}:
        raise SystemExit("Choose all, intervals, trees, or fixed")
    sys.argv = [sys.argv[0]] + sys.argv[2:]
    if mode in {"all", "intervals"}:
        print("INTERVAL CHECKS", flush=True)
        run_intervals()
    if mode in {"all", "fixed"}:
        print("FIXED ROBUST TREE CHECKS", flush=True)
        run_fixed_fast()
    if mode in {"all", "trees"}:
        print("TREE CHECKS", flush=True)
        run()
