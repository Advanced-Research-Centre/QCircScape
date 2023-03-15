import numpy as np

system_size = 4
max_length = 3
# gateset = ['h','t','cx']
gateset = ['x','ccx']
gss = ''
for g in gateset:
    gss += '-'+g

all_pathsum = []
all_pathprob = []
all_expressibility = []
for plen in range(1,max_length+1):
    pathsum = np.load(f'../data/info_Q-{system_size}_L-{max_length}_GS{gss}'.npy)
    all_pathsum.append(pathsum)
    all_pathprob.append(np.divide(pathsum,sum(pathsum[0])))
    all_expressibility.append(1*(pathsum != 0))

predicted_pathprob = []
Mi = all_pathprob[0]
predicted_pathprob.append(Mi)
for plen in range(1,max_length):
    Mi = Mi@all_pathprob[0]
    predicted_pathprob.append(Mi)

predicted_expressibility = []
for plen in range(max_length):
    predicted_expressibility.append(1*(predicted_pathprob[plen] != 0))

# Compare predicted/actual expressibility and reachability