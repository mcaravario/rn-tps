import numpy as np
M = np.array([[3  , -9 , 0  , 5] ,
              [2  , -5 , -3 , 1] ,
              [-1 , 5  , 8  , 4]])

A = np.array([-1, 1, 2], ndmin=2)
B = np.array([-4, 2, 1,-1], ndmin=2)

# 1.

R_1 = np.dot(A, M)
print(R_1)

# 2.

R_2 = np.dot(A.T, B)
print(R_2)

# 3.

R_3 = np.dot(M, B.T)
print(R_3)

# 4.
R_4 = np.dot(A, A.T)
print(R_4)
