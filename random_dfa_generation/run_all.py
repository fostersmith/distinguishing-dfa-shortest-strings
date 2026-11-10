from run_experiment import run_experiment
from itertools import product

import time

if __name__ == "__main__":
    seed = 100
    sample_count = 512
    comparisons = 1024
    f_prob = 0.5
    # only running with all same size for now
    dfa_sizes = [2**i for i in range(1,11)]
    alphabet_sizes = [2**i for i in range(1,6)]
    p_vals = [0.1, 0.5, 0.9]

    for dfa_size, alphabet_size, p_val in product(dfa_sizes, alphabet_sizes, p_vals):
        comparisons = int(((32-alphabet_size)/32 + (1024-dfa_size)/1024)/2 * 1024 + 64)
        out_dir = f"experiments/random_all/size_{dfa_size}_alphabet_{alphabet_size}_p_{p_val}"

        print(f"dfa_size: {dfa_size}, alphabet_size: {alphabet_size}, p_val: {p_val}")
        print(f"making {comparisons} comparisons")
        start = time.time()

        metrics = run_experiment(
                alphabet_size,
                dfa_size,
                dfa_size,
                sample_count,
                comparisons,
                f_prob,
                seed,
                out_dir,
                verbose=False)

        print(f"done in {time.time()-start} seconds")
        print(f"mean: {metrics['distinguishing_len_mean']}")
