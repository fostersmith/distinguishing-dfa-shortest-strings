# Shortest Distinguishing Strings for DFAs

This is the repository containing code for our CS473 Final Project

The upper bound of the shortest distinguishing string between the languages of two DFAs is 
known, but we seek to determine what the length of this string is in practice.

We experimentally determine the length of this string for randomly generated DFAs as well
as several DFAs from a regex dataset, then analyze the findings.

## Running

### Step 0: Install prerequisites

**using pip:**

```bash
pip install matplotlib
pip install -r requirements.txt
```

**using nix-shell environment:**

```bash
nix-shell
```

### Step 1: Run random DFA experiments

```bash
python3 random_dfa_generation/run_all.py
```

### Step 2: Run regex101 experiment

```bash
# load data
python3 dataset_regex/load_data.py
# run experiment
python3 dataset_regex run_experiment.py -c 1024 --seed 100
```

### Step 3 (optional): Generate visuals

```bash
# visuals for random experiment
python3 random_dfa_generation/visualize.py
# visual for regex101 experiment
python3 dataset_regex/visualize_experiment.py dataset_regex/result.json
```
## Project Structure

### `random_dfa_generation/`

Python files pertaining to Random DFA experiments

* `random_dfa.py`: custom DFA implementation with randomization, symmetric difference, and
    BFS shortest string finder
* `run_all.py`: runner to generate random comparison data under experiments/random_all/ 
* `visualize.py`: generate random experiment visuals from `run_all.py` results

### `dataset_regex/`

Python files pertaining to regex101 experiment

* `load_data.py`: load original dataset from huggingface, perform cleanup, 
    write to `dataset_regex/regex_data.csv`
* `run_experiment.py`: run comparisons on data from `load_data.py`,
    write result to `dataset_regex/result.json`
* `visualize_experiment.py`: generate bar chart from experiment result
