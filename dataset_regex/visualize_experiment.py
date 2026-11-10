import sys
import json
import matplotlib.pyplot as plt

if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        results = json.load(f)

    distribution = [len(results['distinguishing'][i]) for i in range(len(results['reg1']))
                    if results['has_distinguishing'][i] == True]
    lengths = list(range(max(distribution)+1))
    counts = [0 for _ in lengths]
    for sample in distribution:
        counts[sample] += 1

    plt.bar(lengths, counts)

    plt.title(f'Length of shortest distinguishing string for\nrandomly sampled regex (regex101)')
    plt.xlabel('Shortest distinguishing string length')
    plt.ylabel('Count')
    plt.savefig('dataset_regex/fig.jpg')

