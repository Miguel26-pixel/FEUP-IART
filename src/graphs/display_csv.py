import matplotlib.pyplot as plt
import pandas as pd

FILE = "../measurings/remove.csv"

dataset = pd.read_csv(FILE)

dataset[["new_sol_score", "curr_best"]].plot()
plt.show()

print(dataset)
