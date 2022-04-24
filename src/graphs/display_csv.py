import matplotlib.pyplot as plt
import pandas as pd

FILE = "../measurings/hill_climb.csv"

dataset = pd.read_csv(FILE)

dataset[["new_sol_score", "curr_best"]].plot()
plt.ylim(900000, 1500000)
plt.show()

print(dataset)
