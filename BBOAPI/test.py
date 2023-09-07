import matplotlib.pyplot as plt
import random

data = [random.randint(0, 20) for i in range(0, 10)]

plt.plot(data, color='magenta', marker='o',mfc='pink' )
plt.xticks(range(0,len(data)+1, 1))

plt.ylabel('data')
plt.xlabel('index')
plt.title("Plotting a list")
plt.show()