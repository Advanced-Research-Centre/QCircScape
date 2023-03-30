import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

system_size = 4
max_length = 3

gateset_db = {0:['x','ccx'], 1:['h','s','cx'], 2:['h','t','cx'], 3:['p(pi/4)', 'rx(pi/2)', 'cx']}
gateset = gateset_db[0]

gss = ''
for g in gateset:
    gss += '-'+g
gss = gss[1:]

all_pathsum = []
all_pathprob = []
all_expressibility = []
for plen in range(1,max_length+1):
    pathsum = np.load(f'../data/info_Q-{system_size}_L-{plen}_GS-{gss}.npy')
    all_pathsum.append(pathsum)
    all_pathprob.append(np.divide(pathsum,sum(pathsum[0])))
    all_expressibility.append(1*(pathsum != 0))

predicted_pathsum = []
predicted_pathprob = []
predicted_expressibility = []
err_predicted_pathsum = []
err_predicted_pathprob = []
err_predicted_expressibility = []
Rsi = all_pathsum[0]   
Rpi = all_pathprob[0]   
predicted_pathsum.append(Rsi)
predicted_pathprob.append(Rpi)
predicted_expressibility.append(all_expressibility[0])
for plen in range(1,max_length):
    Rsi = Rsi@all_pathsum[0]
    Rpi = Rpi@all_pathprob[0]
    predicted_pathsum.append(Rsi)
    predicted_pathprob.append(Rpi)
    predicted_expressibility.append(1*(predicted_pathprob[plen] != 0))
    err_predicted_pathsum.append(np.around(np.subtract(all_pathsum[plen],predicted_pathsum[plen]),3) == 0)
    err_predicted_pathprob.append(np.around(np.subtract(all_pathprob[plen],predicted_pathprob[plen]),3) == 0)
    err_predicted_expressibility.append(np.around(np.subtract(all_expressibility[plen],predicted_expressibility[plen]),3) == 0)

M = np.zeros(np.shape(all_pathprob[0]))

for plen in range(1,max_length+1):
    M += ((2**-plen)*all_pathprob[plen-1])

maxp = np.max(M)
fig, axes = plt.subplots(1, 1, figsize=(10, 10), sharey=True, sharex=True, subplot_kw=dict(aspect='equal'))
sns.heatmap(M, ax=axes, cmap = 'Blues', vmin=0.0, vmax=maxp, cbar = False, xticklabels = [], yticklabels = [])
fig.suptitle(f'Approximation of circuit probability of states on {system_size} qubits using gate set {gss} for depth {max_length}')        
plt.show()
            
# ==> Manual inspection

# print(all_pathsum[0]) 
# print(all_pathsum[1]) 
# print(predicted_pathsum[1]) 
# print(all_pathsum[2])
# print(err_predicted_pathsum)