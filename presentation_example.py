from random_dfa_generation.random_dfa import DFA

A1 = DFA(
         Q={'A', 'B'},
         Sigma={'0', '1'},
         delta = { 'A': {'0': 'A', '1': 'B'},
                   'B': {'0': 'B', '1': 'A'} },
         q0='A',
         F={'A'},
        )

A2 = DFA(
         Q={'C', 'D', 'E'},
         Sigma={'0', '1'},
         delta = { 'C': {'0': 'C', '1': 'D'},
                   'D': {'0': 'D', '1': 'E'},
                   'E': {'0': 'E', '1': 'C'} },
         q0='C',
         F={'C'},
        )

symmetric_difference = DFA.symmetric_difference(A1, A2)

breakpoint()

shortest_distinguishing = symmetric_difference.shortest_accepted()
print(shortest_distinguishing)

breakpoint()
