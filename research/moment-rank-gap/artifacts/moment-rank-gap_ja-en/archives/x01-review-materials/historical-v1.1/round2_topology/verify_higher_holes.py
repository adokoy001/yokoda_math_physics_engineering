"""Exact mod-2 cellular homology of the n=4, S=5/4 face filtration.

Faces are encoded as -1 (free), 0 (fixed zero), 1 (fixed one).
Finite-cell calculation only; geometric equivalence is proved in the appendix.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def rank_mod2(columns):
    pivots = {}
    for column in columns:
        while column:
            pivot = column.bit_length()-1
            if pivot in pivots:
                column ^= pivots[pivot]
            else:
                pivots[pivot] = column
                break
    return len(pivots)


def face_data(n, S):
    m = S.numerator // S.denominator
    r = S-m
    M = m+r*r
    faces = []
    for state in product([-1, 0, 1], repeat=n):
        p, j = state.count(-1), state.count(1)
        if p and 0 < S-j < p:
            faces.append((state, p-1, M-j-(S-j)**2/p))
    return faces


def betti_at(faces, E, n):
    cells = [[state for state,d,weight in faces if d == k and weight <= E]
             for k in range(n)]
    ranks = [0]
    matrices = [[]]
    for k in range(1,n):
        index = {state:i for i,state in enumerate(cells[k-1])}
        columns = []
        for state in cells[k]:
            col = 0
            for i, coordinate in enumerate(state):
                if coordinate == -1:
                    for value in [0,1]:
                        child = state[:i]+(value,)+state[i+1:]
                        if child in index:
                            col ^= 1 << index[child]
            columns.append(col)
        ranks.append(rank_mod2(columns))
        matrices.append(columns)
    ranks.append(0)
    for k in range(2,n):
        for col in matrices[k]:
            composite = 0
            while col:
                pivot = col.bit_length()-1
                composite ^= matrices[k-1][pivot]
                col ^= 1 << pivot
            assert composite == 0
    betti = [len(cells[k])-ranks[k]-ranks[k+1] for k in range(n)]
    return dict(cells=list(map(len,cells)), betti_mod2=betti)


if __name__ == '__main__':
    n, S = 4, F(5,4)
    faces = face_data(n,S)
    thresholds = sorted(set(weight for _,_,weight in faces))
    expected = [[12,0,0,0],[4,4,0,0],[4,0,0,0],
                [1,3,0,0],[1,0,1,0],[1,0,0,0]]
    rows = []
    for i,E in enumerate(thresholds):
        result = betti_at(faces,E,n)
        assert result['betti_mod2'] == expected[i], (E,result)
        rows.append(dict(E=str(E), **result))
        if i+1 < len(thresholds):
            midpoint = (E+thresholds[i+1])/2
            assert betti_at(faces,midpoint,n) == result
    output = dict(status='all_passed', n=n, S=str(S),
                  arithmetic='exact fractions and binary linear algebra',
                  coefficient_field='F_2', thresholds=rows)
    Path(__file__).with_name('higher_holes_results.json').write_text(
        json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))
