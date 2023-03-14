import numpy as np
print("--------------")

unM1 = np.array([
[12  ,1   ,1   ,0   ,1   ,0   ,0   ,0   ,1   ,0   ,0   ,0   ,0   ,0   ,0   ,0],
[1   ,12  ,0   ,1   ,0   ,1   ,0   ,0   ,0   ,1   ,0   ,0   ,0   ,0   ,0   ,0],
[1   ,0   ,12  ,1   ,0   ,0   ,1   ,0   ,0   ,0   ,1   ,0   ,0   ,0   ,0   ,0],
[0   ,1   ,1   ,10  ,0   ,0   ,0   ,2   ,0   ,0   ,0   ,2   ,0   ,0   ,0   ,0],
[1   ,0   ,0   ,0   ,12  ,1   ,1   ,0   ,0   ,0   ,0   ,0   ,1   ,0   ,0   ,0],
[0   ,1   ,0   ,0   ,1   ,10  ,0   ,2   ,0   ,0   ,0   ,0   ,0   ,2   ,0   ,0],
[0   ,0   ,1   ,0   ,1   ,0   ,10  ,2   ,0   ,0   ,0   ,0   ,0   ,0   ,2   ,0],
[0   ,0   ,0   ,2   ,0   ,2   ,2   ,6   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,4],
[1   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,12  ,1   ,1   ,0   ,1   ,0   ,0   ,0],
[0   ,1   ,0   ,0   ,0   ,0   ,0   ,0   ,1   ,10  ,0   ,2   ,0   ,2   ,0   ,0],
[0   ,0   ,1   ,0   ,0   ,0   ,0   ,0   ,1   ,0   ,10  ,2   ,0   ,0   ,2   ,0],
[0   ,0   ,0   ,2   ,0   ,0   ,0   ,0   ,0   ,2   ,2   ,6   ,0   ,0   ,0   ,4],
[0   ,0   ,0   ,0   ,1   ,0   ,0   ,0   ,1   ,0   ,0   ,0   ,10  ,2   ,2   ,0],
[0   ,0   ,0   ,0   ,0   ,2   ,0   ,0   ,0   ,2   ,0   ,0   ,2   ,6   ,0   ,4],
[0   ,0   ,0   ,0   ,0   ,0   ,2   ,0   ,0   ,0   ,2   ,0   ,2   ,0   ,6   ,4],
[0   ,0   ,0   ,0   ,0   ,0   ,0   ,4   ,0   ,0   ,0   ,4   ,0   ,4   ,4   ,0]])
b = 4
M1 = np.divide(unM1,2**b)

def AP(len):
	Mi = M1
	ap_change = np.empty((len), float)
	reach = np.empty((len), int)
	for i in range(0,len):
		Mi_tmp = Mi@M1
		ap_change[i] = sum(sum(abs(Mi_tmp-Mi)))
		reach[i] = np.count_nonzero(Mi_tmp)-np.count_nonzero(Mi)
		Mi = Mi_tmp
	return ap_change, reach, Mi

ap_change_len, reach, UD = AP(0)
np.set_printoptions(precision=4)
# Sanity check: each row/column should add to 1. i.e. sum(UD[:,i]) = sum(UD[i,:]) = 1
print(UD)
print(reach)

# import tkinter
# import matplotlib.pyplot as plt
# plt.plot(ap_change_len)
# plt.xlabel("difference in universal distribution")
# plt.ylabel("program length")
# plt.show()