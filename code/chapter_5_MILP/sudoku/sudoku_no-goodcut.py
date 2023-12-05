import pandas as pd
from mip import BINARY, CBC, Model, xsum

# Read and store initial numbers
df = pd.read_csv(
    "initial_numbers.csv",
    header=None,
    index_col=[0, 1],
    names=["initial values"],
)
init_vals = df.to_dict()["initial values"]

# Needed data structures
rows = range(1, 10)
columns = range(1, 10)
values = range(1, 10)
boxes = [
    [(3 * i + k, 3 * j + l) for k in range(1, 4) for l in range(1, 4)]
    for i in range(3)
    for j in range(3)
]

# Model declaration
m = Model("Sudoku binary", solver_name=CBC)

# Decision variables
y = {
    (r, c, v): m.add_var(var_type=BINARY)
    for r in rows
    for c in columns
    for v in values
}

# Constraints
# Respect initial values
for ((r, c), v) in init_vals.items():
    m += y[r, c, v] == 1
# One entry per cell
for r in rows:
    for c in columns:
        m += xsum(y[r, c, v] for v in values) == 1
# Unique value per row
for r in rows:
    for v in values:
        m += xsum(y[r, c, v] for c in columns) == 1
# Unique value per column
for c in columns:
    for v in values:
        m += xsum(y[r, c, v] for r in rows) == 1
# Unique value per box
for box in boxes:
    for v in values:
        m += xsum(y[r, c, v] for (r, c) in box) == 1

# Optimize statement
m.optimize()

# Collect indices from solution
I = [k for k in y if y[k].x > 0.99]

# Add no-good cut
m += xsum(y[k] for k in I) <= 80

# Print optimization status
print(m.status)
