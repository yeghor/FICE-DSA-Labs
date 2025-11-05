import matplotlib.pyplot as plt
from matplotlib.pyplot import ylabel

# DP Task n operations step
# Incrementing to use it in range without cropping last value
FOR_N = 100 + 1

# Operations difference of iterations
STEP = 5

x, dp_y = [], []
for i in range(1, FOR_N):
    x.append(i)
    dp_y.append(i * STEP)


"""
Time complexity formula for nested loops F(n) = 5n + n^2 
Using known static step and arithmetic progression for nested loops S(n) = (2 * 2 + 2(n -1)/ 2) * n <=> n + n^2 
"""
# nl - nested loop
nl_y = []

for n in range(1, FOR_N):
    nl_y.append(5*n + n**2)


plt.plot(x, dp_y, label="Dynamic Programming Approach")
plt.plot(x, nl_y, label="Nested Loops Approach")
plt.ylabel("Operations")
plt.xlabel("n Outer Loop Iterations")
plt.grid(True)
plt.legend()
plt.show()
