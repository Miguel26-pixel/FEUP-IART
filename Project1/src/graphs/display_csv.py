import matplotlib.pyplot as plt
import pandas as pd

FILE = "../measurings/hill_climb_long.csv"

dataset = pd.read_csv(FILE)

dataset[["new_sol_score", "curr_best"]].plot()
plt.ylim(900000, 1550000)
plt.show()

print(dataset)
