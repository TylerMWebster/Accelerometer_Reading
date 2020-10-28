import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd


data = pd.read_csv('Reference/test_COM6_9600.csv', names=['radx', 'rady', 'radz'])
#data.drop(0,3)
datx = data['radx'].to_numpy()
daty = data['rady'].to_numpy()
datz = data['radz'].to_numpy()
indexes = []
for i in range(0, len(datx)):
    indexes.append(i)
plt.plot(datx)
plt.plot(daty)
plt.plot(datz)
plt.show()
