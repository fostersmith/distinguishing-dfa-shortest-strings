import os
import random
import statistics
from random import randint
import time
import argparse

import json

from random_dfa import DFA

def run_experiment(alphabet_size, 
                   min_dfa_size,
                   max_dfa_size,
                   sample_count,
                   comparisons,
                   f_prob,
                   seed,
                   out_dir):
    # prep dirs
    os.makedirs(out_dir, exist_ok=True)
    samples_file = os.path.join(args.out_dir, "samples.json")
    results_file = os.path.join(args.out_dir, "results.json")
    metrics_file = os.path.join(args.out_dir, "metrics.json")

    # seed
    random.seed(seed)
    
    ## alphabet with correct size
    Sigma = set(range(alphabet_size))

    ## generate random samples
    print ("generating samples...")
    start = time.time()

    samples = []
    for _ in range(sample_count):
        sample = DFA.generate_random(Sigma, randint(min_dfa_size, max_dfa_size), f_prob)
        samples.append(sample)

    elapsed = time.time() - start
    print(f"generated {sample_count} samples in {elapsed} seconds.")

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

    ## run comparisons
    print("making comparisons...")
    start = time.time()

    test_results = []
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
            "has_distinguishing": shortest_distinguishing != None,
            "shortest_distinguishing": shortest_distinguishing,
            })
    
    elapsed = time.time() - start
    print(f"made {comparisons} comparisons in {elapsed} seconds")

    with open(results_file, 'w') as f:
        json.dump(test_results, f)

    ## calculate metrics
    str_lens = [len(res['shortest_distinguishing']) for res in test_results
        if res['has_distinguishing'] == True]

    identical_count = 0
    for res in test_results:
        if res['has_distinguishing'] == False:
            identical_count += 1

    dfa_sizes = [len(dfa.Q) for dfa in samples]

    metrics = {}
    metrics['dfa_size_mean'] = statistics.mean(dfa_sizes)
    metrics['p_indistinguishable'] = identical_count / comparisons

    metrics['distinguishing_len_mean'] = statistics.mean(str_lens)
    metrics['distinguishing_len_median'] = statistics.median(str_lens)
    metrics['distinguishing_len_sample_variance'] = statistics.variance(str_lens)

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

    return metrics

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
    metrics = run_experiment(
            args.alphabet_size,
            args.min_dfa_size,
            args.max_dfa_size,
            args.sample_count,
            args.comparisons,
            args.F_prob,
            args.seed,
            args.out_dir)

    print("\n\nMetrics:")
    for lbl in metrics:
        print(f"{lbl:40}:  {metrics[lbl]}")
