import os, sys
import pandas
import json

import random
import argparse

from automata.fa.dfa import DFA as automata_lib_DFA
from automata.fa.nfa import NFA as automata_lib_NFA

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from random_dfa_generation.random_dfa import DFA

def load_as_DFA(reg):
    as_lib_nfa = automata_lib_NFA.from_regex(reg)
    as_lib_dfa = automata_lib_DFA.from_nfa(as_lib_nfa, minify=True).to_complete()
    #skipping custom implementation because this lib has a MUCH FASTER symmetric difference
    return as_lib_dfa
    #return DFA (
    #        Q= as_lib_dfa.states,
    #        Sigma= as_lib_dfa.input_symbols,
    #        delta= as_lib_dfa.transitions,
    #        q0= as_lib_dfa.initial_state,
    #        F= as_lib_dfa.final_states
    #        )

# merge input_symbols for two automata_lib_DFA (give them the same language)
# returns a partial DFA
def merge_sigma(a1, a2):
    new_sigma = a1.input_symbols | a2.input_symbols
    a1p = automata_lib_DFA (
            states = a1.states,
            input_symbols = new_sigma,
            transitions = a1.transitions,
            initial_state = a1.initial_state,
            final_states = a1.final_states,
            allow_partial = True
            )
    a2p = automata_lib_DFA (
            states = a2.states,
            input_symbols = new_sigma,
            transitions = a2.transitions,
            initial_state = a2.initial_state,
            final_states = a2.final_states,
            allow_partial = True
            )
    return (a1p, a2p)

import time
import multiprocessing as mp

class TimeoutError(Exception):
    pass

def task_shortest_distinguishing(queue, reg1, reg2):
    queue.put(shortest_distinguishing(reg1, reg2))
def shortest_distinguishing_with_timeout(reg1, reg2, timeout=10):
    queue = mp.Queue()

    p = mp.Process(target=task_shortest_distinguishing, args=(queue,reg1,reg2,))
    p.start()
    p.join(timeout)

    if queue.empty():
        p.terminate()
        raise TimeoutError(f"Timed out on input: '{reg1}', '{reg2}'")
    else:
        return queue.get()

def shortest_distinguishing(reg1, reg2):
    a1, a2 = merge_sigma(load_as_DFA(reg1), load_as_DFA(reg2))

    diff_lib_dfa = a1.symmetric_difference(a2).to_complete()
    diff = DFA (
            Q= diff_lib_dfa.states,
            Sigma= diff_lib_dfa.input_symbols,
            delta= diff_lib_dfa.transitions,
            q0= diff_lib_dfa.initial_state,
            F= diff_lib_dfa.final_states
            )

    shortest_accepted_l = diff.shortest_accepted()
    if shortest_accepted_l != None:
        return ''.join(shortest_accepted_l)
    else:
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--comparisons', type=int)
    parser.add_argument('--seed', type=int, default=random.randint(0,1024))
    args = parser.parse_args()

    comparisons = args.comparisons
    random.seed(args.seed)

    # read dataset from csv
    try:
        dirname = os.path.dirname(__file__)
        df = pandas.read_csv(os.path.join(dirname, 'regex_data.csv'))
        print(f"Loaded {len(df['regex'])} rows")
    except:
        print("Couldn't find dataset. Did you run load_data.py?")
        exit(1)

    results = {"reg1": [], "reg2": [], "has_distinguishing": [], "distinguishing": []}

    # take N samples, find symmetric difference
    for i in range(comparisons):
        i1 = 0
        i2 = 0
        while i1 == i2:
            i1 = random.randrange(len(df['regex']))
            i2 = random.randrange(len(df['regex']))

        reg1 = df['regex'][i1]
        reg2 = df['regex'][i2]

        try:
            distinguishing = shortest_distinguishing_with_timeout(reg1, reg2)
            print(distinguishing)
            results['reg1'].append(reg1)
            results['reg2'].append(reg2)
            results['has_distinguishing'].append(distinguishing != None)
            results['distinguishing'].append(distinguishing)
        except Exception as err:
            print(f"Encountered error at i={i}: {err}")

    with open('dataset_regex/result.json', 'w') as f:
        json.dump(results, f)
