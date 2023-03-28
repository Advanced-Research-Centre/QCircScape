print("\n****** Welcome to Growth Rate Plot! ******\n")

# ****************************************************************************************************************************************

import pickle
import matplotlib.pyplot as plt

plt.rcParams.update(
    {"text.usetex": True, "font.family": "serif", "font.size": 10}
)

prog_growth_info = []
with (open(f'../data/INFO_prog_numb.p', "rb")) as openfile:
    while True:
        try:
            prog_growth_info.append(pickle.load(openfile))
        except EOFError:
            break

prog_growth_info_dict = prog_growth_info[0]
line_type = ['r-', 'b--']
for no, prog_grow_key in enumerate(prog_growth_info_dict.keys()):
    plt.semilogy(prog_growth_info_dict[prog_grow_key], line_type[no],  label = prog_grow_key)

plt.xlabel('Number of qubits')
plt.ylabel('Number of programs')
plt.legend()
plt.savefig(f'../data/growth_rate_prog.pdf')
plt.savefig(f'../data/growth_rate_prog.png')



