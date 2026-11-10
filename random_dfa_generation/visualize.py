import os
import sys
import json
import matplotlib.pyplot as plt

"""
visualize string length as bar chart
"""
def visualize_experiment(results, metrics, out_dir):
    out_file = os.path.join(out_dir, "shortest_distinguishing_len_chart.jpg")
    distribution = [len(s['shortest_distinguishing']) for s in results
               if s['has_distinguishing'] == True]
    lengths = list(range(max(distribution)+1))
    counts = [0 for _ in lengths]
    for sample in distribution:
        counts[sample] += 1

    plt.bar([str(l) for l in lengths], counts)
    plt.title(f'Length of shortest distinguishing string for randomly generated DFAs')
    plt.xlabel('Shortest distinguishing length')
    plt.ylabel('Count')
    plt.savefig(out_file)

if __name__ == "__main__":
    for res_dir in sys.argv[1:]:
        #samples_file = os.path.join(res_dir, "samples.json")
        results_file = os.path.join(res_dir, "results.json")
        metrics_file = os.path.join(res_dir, "metrics.json")
        #with open(samples_file, 'r') as f:
        #    samples = json.load(f)
        with open(results_file, 'r') as f:
            results = json.load(f)
        with open(metrics_file, 'r') as f:
            metrics = json.load(f)

        visualize_experiment(results, metrics, res_dir)
