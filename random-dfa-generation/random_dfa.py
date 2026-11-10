from typing import TypeVar, Generic
from collections.abc import Callable
from random import randint
from itertools import product, chain, combinations_with_replacement
import random

# alphabet member type
A = TypeVar('A')
# state transition type
T = TypeVar('T')

def every_string(Sigma: list[A], n: int) -> list[list[A]]:
    if n == 0:
        return []
    elif n == 1:
        return [ [c] for c in Sigma ] 
    else:
        prev = every_string(Sigma, n-1)
        return [ [ci] + cj for ci, cj in product(Sigma, prev) ]

class DFA(Generic[T,A]):
    """
    Create a DFA using a 5-tuple

    Q:      Finite set of states
    Sigma:  Alphabet of the DFA
    delta:  Transition table
    q0:     Starting state
    F:      Finite set of accepting states
    """
    def __init__(self,
                 Q: set[T],
                 Sigma: list[A],
                 delta: dict[T, dict[T, A]],
                 q0: T, 
                 F: set[T]):

        self.Q = Q
        self.Sigma = Sigma
        self.delta = delta
        self.q0 = q0
        self.F = F

    def debug_print(self):
        print(f"Q:     {self.Q}")
        print(f"Sigma: {self.Sigma}")
        print(f"delta: {self.delta}")
        print(f"q0:    {self.q0}")
        print(f"F:     {self.F}")


    """
    Returns resulting state after running on input w
    """
    def run(self, w: list[A]) -> int:
        state = self.q0
        for c in w:
            state = self.delta[state][c]
        return state
    
    """
    Returns true if DFA is in accepting state after running on input w
    """
    def accepts(self, w: list[A]) -> bool:
        state = self.run(w)
        return state in self.F

    """
    Find shortest string accepted by DFA using BFS on state graph
    """
    def shortest_accepted(self) -> list[A] | None:
        # return if there are no states
        if len(self.Q) == 0:
            return None

        # maps state to shortest path (int -> list[A])
        shortest_paths = {self.q0: []}

        visit_queue = [self.q0]
        while len(visit_queue) > 0:
            cur_state = visit_queue.pop(0)
            cur_path = shortest_paths[cur_state]

            if cur_state in self.F:
                return cur_path

            for symb in self.Sigma:
                next_state = self.delta[cur_state][symb]

                if not next_state in shortest_paths:
                    shortest_paths[next_state] = cur_path + [symb]
                    visit_queue.append(next_state)

                #if next_state in self.F:
                #    return shortest_paths[next_state]

        return None

    """
    construct DFA which recognizes the symmetric difference between two DFAs A1 and A2
    """
    def symmetric_difference(A1, A2):
        if A1.Sigma != A2.Sigma:
            raise ValueError("A1 and A2 must share an alphabet")

        # simple properties for product DFA
        Q = set(product(A1.Q, A2.Q))
        Sigma = A1.Sigma
        q0 = (A1.q0, A2.q0)

        # build transition table (product transition table)
        delta = {}
        for Q1 in A1.Q:
            for Q2 in A2.Q:
                delta[(Q1, Q2)] = {}
                for symb in Sigma:
                    S1 = A1.delta[Q1][symb]
                    S2 = A2.delta[Q2][symb]
                    delta[(Q1, Q2)][symb] = (S1, S2)
        
        # F: states accepted in either but not both
        F = {(s1, s2) for (s1, s2) in Q if (s1 in A1.F) ^ (s2 in A2.F)}

        return DFA(Q, Sigma, delta, q0, F)

    """
    combination of BFS and brute force to find the shortest distinguishing string between
    two DFAs
    """
    def shortest_distinguishing(A1, A2, max_brute_force_len=4):
        if A1.Sigma != A2.Sigma:
            raise ValueError("A1 and A2 must share an alphabet")
        Sigma_ordered = list(A1.Sigma)

        for i in range(max_brute_force_len):
            gen = combinations_with_replacement(Sigma_ordered, i)
            for w in gen:
                if bool(A1.accepts(w)) ^ bool(A2.accepts(w)):
                    return w

        return DFA.symmetric_difference(A1, A2).shortest_accepted()

    """
    generate a random DFA with n states under Sigma

    p is probability for a state to be in F
    """
    def generate_random(Sigma: list[A], n: int, f_prob: float = 0.5):
        # generate delta table: for each state transition, pick a state at random
        delta_table = {}
        for state in range(0, n):
            delta_table[state] = {}
            for c in Sigma:
                delta_table[state][c] = randint(0, n-1)

        # generate F: add each state with p=0.5
        F = set()
        for state in range(0, n):
            if random.random() < f_prob:
                F.add(state)

        return DFA[int,A](
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
    def generate_exhaustive(Sigma: list[A], n: int) -> list:
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
            dfas.append(DFA[int,A](
                Q= set(range(0, n)),
                Sigma= Sigma,
                delta=tbl,
                q0=0,
                F= F
                ))
        return dfas

if __name__ == "__main__":
    import pdb
    random.seed(0)
    Sigma = set(range(32))
    A = DFA.generate_random(Sigma, 10)
    B = DFA.generate_random(Sigma, 10)
