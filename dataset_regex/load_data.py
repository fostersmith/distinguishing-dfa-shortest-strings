# load regex from dataset into data.csv, drop everything that can't be easily converted
# to DFA
import os
import pandas as pd

import automata.regex.regex as regex_lib
from automata.fa.nfa import NFA

import string
alphabet = set(string.ascii_lowercase)

if __name__ == "__main__":
    df = pd.read_json("hf://datasets/innovatorved/regex_dataset/data.json")

    # correct \d to [0-9]
    # remove ^ (start-of-line)
    # remove $ (end-of-line)
    # change group (?<foo>bar)/(?P<foo>bar)/(?:bar) to (bar)
    df['regex'] = df['regex'].str \
        .replace('\\d', '[0-9]') \
        .replace(r'[^\[\\]?\^', '', regex=True) \
        .replace(r'[^\\]?\$', '', regex=True) \
        .replace(r'\(\?(P?\<.*\>|:)', '(', regex=True)

    # drop rows that dont fit our regex format
    drop_rows = []
    for i, regex in enumerate(df['regex']):
        try:
            if type(regex) != str:
                raise Exception()

            regex_lib.validate(regex)

            # this library refuses to load certain regexes without invalidating them,
            # and i don't have time to figure out what is happening. this takes forever
            # but it works for now
            nfa = NFA.from_regex(regex, input_symbols=alphabet)

            # also check for empty
            if len(nfa.final_states) == 0:
                raise Exception()
        except:
            drop_rows.append(i)
    df.drop(drop_rows, inplace=True)
    print(f"Dropped {len(drop_rows)} rows")

    # write to csv
    dirname = os.path.dirname(__file__)
    df.to_csv(os.path.join(dirname, 'regex_data.csv'))
