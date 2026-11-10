import os
import sys
import json
import pandas
import matplotlib.pyplot as plt

from itertools import product

"""

"""
def visualize_experiments():
    dfa_sizes = [2**i for i in range(1,11)]
    alphabet_sizes = [2**i for i in range(1,6)]
    p_vals = [0.1, 0.5, 0.9]

    os.makedirs('visuals/length_distributions/', exist_ok=True)

    for dfa_size, alph_size in product(dfa_sizes, alphabet_sizes):
        rows = {}
        max_length = 0
        for p in p_vals:
            # load data
            cur_dir = f'experiments/random_all/size_{dfa_size}_alphabet_{alph_size}_p_{p}'
            with open(os.path.join(cur_dir, 'metrics.json'), 'r') as f:
                metrics = json.load(f)
            with open(os.path.join(cur_dir, 'results.json'), 'r') as f:
                results = json.load(f)

            distribution = [len(s['shortest_distinguishing']) for s in results
                       if s['has_distinguishing'] == True]
            lengths = list(range(max(distribution)+1))
            counts = [0 for _ in lengths]
            for sample in distribution:
                counts[sample] += 1

            max_length = max(len(counts), max_length)
            rows[f'p={p}'] = counts
            #plt.bar([str(l) for l in lengths], counts, label=f"p={p}")

        for k, counts in rows.items():
            rows[k] = counts + [0] * (max_length-len(counts))
        df = pandas.DataFrame(rows)
        plt.ioff()
        df.plot(kind='bar', title=f'Experiment: Uniformly random DFAs\n|Σ|={alph_size}, |Q|={dfa_size}')
        
        plt.xlabel('Shortest distinguishing length')
        plt.ylabel('Count')
        plt.savefig(f'visuals/length_distributions/size_{dfa_size}_alphabet_{alph_size}.jpg')
        plt.close()


"""
make charts under visuals/wrt_alphabet/
- each chart is size_N.jpg
"""
def visualize_wrt_alphabet():
    dfa_sizes = [2**i for i in range(1,11)]
    alphabet_sizes = [2**i for i in range(1,6)]
    p_vals = [0.1, 0.5, 0.9]

    os.makedirs('visuals/wrt_alphabet', exist_ok=True)

    for N in dfa_sizes:
        fig_path = f'visuals/wrt_alphabet/size_{N}.jpg'
        fig, (meanAx, varAx) = plt.subplots(1,2)
        for p in p_vals:
            means = []
            variances = []


            for alph_size in alphabet_sizes:
                # load data
                cur_dir = f'experiments/random_all/size_{N}_alphabet_{alph_size}_p_{p}'
                with open(os.path.join(cur_dir, 'metrics.json'), 'r') as f:
                    metrics = json.load(f)

                means.append(metrics['metrics']['distinguishing_len_mean'])
                variances.append(metrics['metrics']['distinguishing_len_sample_variance'])

            # plot mean vs alphabet size
            meanAx.plot(alphabet_sizes, means, label=f'p={p}')

            varAx.plot(alphabet_sizes, variances, label=f'p={p}')

        fig.suptitle(f"Experiment: Uniformly random DFAs with {N} states")
        fig.set_figheight(6)
        fig.set_figwidth(12)

        meanAx.set_title(f"Mean SDS Length")
        meanAx.set_xlabel("Alphabet Size |Σ|")
        meanAx.set_ylabel("Mean length of shortest distinguishing string")
        meanAx.legend()
        varAx.set_title(f"Sample Variance for SDS Length")
        varAx.set_xlabel("Alphabet Size |Σ|")
        varAx.set_ylabel("Sample variance")
        varAx.legend()

        plt.savefig(fig_path)

"""
make charts under visuals/wrt_dfa_size/
- each chart is alphabet_N.jpg
"""
def visualize_wrt_dfa_size():
    dfa_sizes = [2**i for i in range(1,11)]
    alphabet_sizes = [2**i for i in range(1,6)]
    p_vals = [0.1, 0.5, 0.9]

    os.makedirs('visuals/wrt_dfa_size', exist_ok=True)

    for N in alphabet_sizes:
        fig_path = f'visuals/wrt_dfa_size/alphabet_{N}.jpg'
        fig, (meanAx, varAx) = plt.subplots(1,2)
        for p in p_vals:
            means = []
            variances = []

            for dfa_size in dfa_sizes:
                # load data
                cur_dir = f'experiments/random_all/size_{dfa_size}_alphabet_{N}_p_{p}'
                with open(os.path.join(cur_dir, 'metrics.json'), 'r') as f:
                    metrics = json.load(f)

                means.append(metrics['metrics']['distinguishing_len_mean'])
                variances.append(metrics['metrics']['distinguishing_len_sample_variance'])

            # plot mean vs alphabet size
            meanAx.plot(dfa_sizes, means, label=f'p={p}')
            varAx.plot(dfa_sizes, variances, label=f'p={p}')

        fig.suptitle(f"Experiment: Uniformly Random DFAs with Alphabet Size of {N}")
        fig.set_figheight(6)
        fig.set_figwidth(12)

        meanAx.set_title(f"Mean SDS Length")
        meanAx.set_xlabel("Number of States")
        meanAx.set_ylabel("Mean length of shortest distinguishing string")
        meanAx.legend()
        varAx.set_title(f"Sample Variance for SDS Length")
        varAx.set_xlabel("Number of States")
        varAx.set_ylabel("Sample variance")
        varAx.legend()

        plt.savefig(fig_path)

if __name__ == "__main__":
    visualize_wrt_dfa_size()
    visualize_wrt_alphabet()
    visualize_experiments()
