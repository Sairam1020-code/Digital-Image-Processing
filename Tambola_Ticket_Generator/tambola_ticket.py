import random
import numpy as np
import matplotlib.pyplot as plt

ticket = np.zeros((3, 9), dtype=int)

ranges = [
    range(1, 10),
    range(10, 20),
    range(20, 30),
    range(30, 40),
    range(40, 50),
    range(50, 60),
    range(60, 70),
    range(70, 80),
    range(80, 91)
]

positions = []

for row in range(3):
    cols = random.sample(range(9), 5)

    for col in cols:
        positions.append((row, col))

used = {i: [] for i in range(9)}

for row, col in positions:

    available = list(set(ranges[col]) - set(used[col]))

    number = random.choice(available)

    ticket[row, col] = number

    used[col].append(number)

for col in range(9):

    values = sorted(ticket[:, col][ticket[:, col] != 0])

    rows = np.where(ticket[:, col] != 0)[0]

    for i, row in enumerate(rows):
        ticket[row, col] = values[i]

fig, ax = plt.subplots(figsize=(12, 4))

ax.set_xlim(0, 9)
ax.set_ylim(0, 3)

for i in range(10):
    ax.plot([i, i], [0, 3], linewidth=2)

for i in range(4):
    ax.plot([0, 9], [i, i], linewidth=2)

for row in range(3):
    for col in range(9):

        value = ticket[row, col]

        if value != 0:
            ax.text(
                col + 0.5,
                2.5 - row,
                str(value),
                ha="center",
                va="center",
                fontsize=16
            )

ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Tambola Ticket")

plt.show()