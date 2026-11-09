from typing import TypeVar, Generic
from collections.abc import Callable
from random import randint
from itertools import product
import argparse
import random
import pdb
import json

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
        #builder = []
        #for ci in Sigma:
        #    for cj in prev:
        #        builder.append([ci] + cj)
        #return builder

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
    parser = argparse.ArgumentParser(
            description="run shortest strings expirement on randomly generated DFAs")
    parser.add_argument('-a', '--alphabet-size', type=int)
    parser.add_argument('-m', '--min-dfa-size', type=int, default=1)
    parser.add_argument('-M', '--max-dfa-size', type=int)
    parser.add_argument('-S', '--sample-count', type=int)
    parser.add_argument('-c', '--comparisons', type=int)
    parser.add_argument('-p', '--F-prob' , type=float, default=0.5,
        help="probability for a state to be in F")
    parser.add_argument('--seed', type=int, default=randint(0, 1024))

    parser.add_argument('--out-dir', type=str, default='experiments/random/last')

    args = parser.parse_args()
    alphabet_size = args.alphabet_size
    min_dfa_size = args.min_dfa_size
    max_dfa_size = args.max_dfa_size
    sample_count = args.sample_count
    comparisons = args.comparisons
    f_prob = args.F_prob

    import os
    os.makedirs(args.out_dir)
    samples_file = os.path.join(args.out_dir, "samples.json")
    results_file = os.path.join(args.out_dir, "results.json")
    metrics_file = os.path.join(args.out_dir, "metrics.json")

    random.seed(args.seed)
    
    # run the experiment

    ## alphabet with correct size
    Sigma = set(range(alphabet_size))

    ## generate random samples
    samples = []
    for _ in range(sample_count):
        sample = DFA.generate_random(Sigma, randint(min_dfa_size, max_dfa_size), f_prob)
        samples.append(sample)

    ## write samples to file
    with open(samples_file, 'w') as f:
        sample_dicts = []
        for dfa in samples:
            sample_dict = {
                    'Q': list(dfa.Q), 
                    'delta': dfa.delta, 
                    'q0': dfa.q0, 
                    'F': list(dfa.F)
                    }
            sample_dicts.append(sample_dict)

        json.dump({'Sigma': list(Sigma), 'samples': sample_dicts}, f)

    test_results = []
    ## run comparisons
    for _ in range(comparisons):
        # don't compare same sample
        first = 0
        second = 0
        while first == second:
            first = random.randrange(sample_count)
            second = random.randrange(sample_count)

        A = samples[first]
        B = samples[second]

        # NOTE remember this could be None
        shortest_distinguishing = DFA.symmetric_difference(A,B).shortest_accepted()

        test_results.append({
            "A_index": first,
            "B_index": second,
            "shortest_distinguishing": shortest_distinguishing,
            })

    with open(results_file, 'w') as f:
        json.dump(test_results, f)

    ## calculate metrics
    import statistics
    metrics = {}
    str_lens = [len(res['shortest_distinguishing']) for res in test_results]

    metrics['mean'] = statistics.mean(str_lens)
    metrics['median'] = statistics.median(str_lens)
    metrics['sample_variance'] = statistics.variance(str_lens)
    metrics['pop_variance'] = statistics.pvariance(str_lens)

    with open(metrics_file, 'w') as f:
        params = {
                'alphabet_size': args.alphabet_size,
                'min_dfa_size': args.min_dfa_size,
                'max_dfa_size': args.max_dfa_size,
                'sample_count': args.sample_count,
                'comparisons': args.comparisons,
                'f_prob': args.F_prob,
                'seed': args.seed
                }
        json.dump({'params': params, 'metrics': metrics}, f)

    print("Metrics for length of shortest distinguishing string:")
    for lbl in metrics:
        print(f"{lbl:16}:  {metrics[lbl]}")
