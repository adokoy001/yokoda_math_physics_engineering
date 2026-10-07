#!/usr/bin/env python3
"""Exhaustive truth-table audit of the lexicographic next-bit patch lemma.

No circuit-minimization claims are tested here. C is treated as an existing
output wire with arbitrary Boolean semantics. The extra gates are constructed
and counted explicitly in the fan-in-two AND/OR/NOT basis (each gate costs 1).
All n <= 4 functions, all nonzero proper cuts, and both new labels are checked.
"""
import argparse
import json
from pathlib import Path


def audit(max_n=4):
    records = []
    total = 0
    for n in range(1, max_n + 1):
        points = 1 << n
        mask = (1 << points) - 1
        variable_tables = [
            sum(((x >> bit) & 1) << x for x in range(points))
            for bit in range(n)
        ]
        cases = 0
        gate_bounds = []
        for cut in range(1, points):
            support = [bit for bit in range(n) if (cut >> bit) & 1]
            cone = variable_tables[support[0]]
            and_gates = 0
            for bit in support[1:]:
                cone &= variable_tables[bit]
                and_gates += 1
            prefix_mask = (1 << cut) - 1
            assert cone & prefix_mask == 0
            assert (cone >> cut) & 1 == 1
            h = cut.bit_count()
            assert and_gates == h - 1
            gate_bounds.append({
                "cut": cut,
                "popcount": h,
                "label_1_extra_gates": and_gates + 1,
                "label_0_extra_gates": and_gates + 2,
            })
            for original in range(1 << points):
                # One output OR gate.
                patched_1 = original | cone
                assert (patched_1 & prefix_mask) == (original & prefix_mask)
                assert (patched_1 >> cut) & 1 == 1
                assert and_gates + 1 == h
                # One NOT on the cone and one output AND gate.
                patched_0 = original & (mask ^ cone)
                assert (patched_0 & prefix_mask) == (original & prefix_mask)
                assert (patched_0 >> cut) & 1 == 0
                assert and_gates + 2 == h + 1
                cases += 2
        # i=0 is a separate constant-output case, not an empty-conjunction
        # claim with a zero-gate constant. With input x0: x0 AND NOT x0
        # and x0 OR NOT x0 each use two gates and realize labels 0 and 1.
        x0 = variable_tables[0]
        constant_0 = x0 & (mask ^ x0)
        constant_1 = x0 | (mask ^ x0)
        assert constant_0 == 0 and constant_1 == mask
        records.append({
            "n": n,
            "truth_table_points": points,
            "all_boolean_functions": 1 << points,
            "nonzero_proper_cuts": points - 1,
            "patch_cases": cases,
            "empty_prefix_constants_checked": 2,
            "gate_bounds": gate_bounds,
        })
        total += cases
    return {
        "claim": "Lexicographic upper-cone next-bit patch",
        "status": "PASS",
        "basis": "fanin-2 AND, OR; unary NOT; each costs one; free fanout",
        "input_order": "unsigned integer ascending; bit 0 is least significant",
        "domain": "all Boolean truth tables for 1 <= n <= max_n",
        "max_n": max_n,
        "total_patch_cases": total,
        "checks": [
            "upper cone vanishes at every previously read point",
            "upper cone equals one at next point",
            "both patch outputs preserve complete prefix",
            "both patch outputs realize requested next label",
            "explicit extra gate counts equal popcount(i) and popcount(i)+1",
            "empty-prefix constant cases use two gates each",
        ],
        "limitations": [
            "finite checks supplement the symbolic proof",
            "not a circuit enumeration or minimal-gate proof",
            "does not establish a streaming time lower bound",
        ],
        "by_n": records,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("nextbit_patch_verification.json"))
    args = parser.parse_args()
    if not 1 <= args.max_n <= 4:
        parser.error("exhaustive audit supports 1 <= --max-n <= 4")
    result = audit(args.max_n)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": result["status"],
                      "total_patch_cases": result["total_patch_cases"],
                      "output": str(args.output.resolve())}, ensure_ascii=False))


if __name__ == "__main__":
    main()
