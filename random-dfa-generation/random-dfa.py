from typing import TypeVar, Generic
from collections.abc import Callable
from random import randint
from itertools import product

T = TypeVar('T')

def every_string(Sigma: list[T], n: int) -> list[list[T]]:
    if n == 0:
        return []
    elif n == 1:
        return [ [c] for c in Sigma ] 
    else:
        prev = every_string(Sigma, n-1)
        return [ [ci] + cj for ci, cj in product(Sigma, prev) ]
        #builder = []
        #for ci in Sigma:
        #    for cj in prev:
        #        builder.append([ci] + cj)
        #return builder

class DFA(Generic[T]):
    """
    Create a DFA using a 5-tuple

    Q:      Finite set of states
    Sigma:  Alphabet of the DFA
    delta:  Transition table
    q0:     Starting state
    F:      Finite set of accepting states
    """
    def __init__(self,
                 Q: set[int],
                 Sigma: list[T],
                 delta: dict[int, dict[int, T]],
                 q0: int, 
                 F: set[int]):

        self.Q = Q
        self.Sigma = Sigma
        self.delta = delta
        self.q0 = q0
        self.F = F

    def run(self, w: list[T]) -> int:
        state = self.q0
        for c in w:
            state = self.delta[state][c]
        return state
    
    def accepts(self, w: list[T]) -> bool:
        state = self.run(w)
        return state in self.F

    def debug_print(self):
        print(f"Q:     {self.Q}")
        print(f"Sigma: {self.Sigma}")
        print(f"delta: {self.delta}")
        print(f"q0:    {self.q0}")
        print(f"F:     {self.F}")

    def generate_random(Sigma: list[T], n: int):
        # generate delta table: for each state transition, pick a state at random
        delta_table = {}
        for state in range(0, n):
            delta_table[state] = {}
            for c in Sigma:
                delta_table[state][c] = randint(0, n-1)

        # generate F: add each state with p=0.5
        F = set()
        for state in range(0, n):
            if randint(0,1) == 1:
                F.add(state)

        return DFA[T](
                Q= set(range(0, n)),
                Sigma= Sigma,
                delta= delta_table,
                q0= 0,
                F= F)

    """
    generate every possible DFA under Sigma with len(Q) = n

    this takes a very long time and generates duplicates

    there is probably a better way to do this
    """
    def generate_exhaustive(Sigma: list[T], n: int) -> list:
        # generate delta tables exhaustively
        delta_tables = []
        possible_rows = every_string(list(range(0,n)), len(Sigma))
        possible_mats = every_string(possible_rows, n)
        for delta_mat in possible_mats:
            tbl = {}
            for (st, row) in enumerate(delta_mat):
                tbl[st] = {}
                for (c, elem) in enumerate(row):
                    tbl[st][Sigma[c]] = elem
            delta_tables.append(tbl)

        # generate every F exhaustively
        f_strings = every_string([True, False], n) # slow
        f_vals = []
        for s in f_strings:
            f_vals.append(set(st for st in range(0, n) if s[st]))

        dfas = []
        for tbl, F in product(delta_tables, f_vals):
            dfas.append(DFA[T](
                Q= set(range(0, n)),
                Sigma= Sigma,
                delta=tbl,
                q0=0,
                F= F
                ))
        return dfas

dfas = DFA.generate_exhaustive(['a'], 2)
for dfa in dfas:
    print(dfa.delta)
    #dfa.debug_print()
print(f"generated {len(dfas)} DFAs.")
