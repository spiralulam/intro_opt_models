import time
from itertools import combinations

import pandas as pd
from mip import BINARY, CBC, GUROBI, INTEGER, Model

for solver_name in [GUROBI, CBC]:
    # Track execution time
    t_start = time.time()

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
    boxes = [
        [
            (3 * i + k, 3 * j + l)
            for k in range(1, 4)
            for l in range(1, 4)
        ]
        for i in range(3)
        for j in range(3)
    ]

    # Model declaration
    m = Model("Sudoku integer", solver_name=solver_name)

    # Decision variables
    x = {
        (r, c): m.add_var(var_type=INTEGER, lb=1, ub=9)
        for r in rows
        for c in columns
    }
    y = {
        (r, c, r1, c1): m.add_var(var_type=BINARY)
        for r in rows
        for c in columns
        for r1 in rows
        for c1 in columns
    }

    # Constraints
    # Respect initial values
    for ((r, c), v) in init_vals.items():
        m += x[r, c] == v
    # Unique value per row
    for r in rows:
        for (c, c1) in combinations(columns, 2):
            m += x[r, c] + 1 <= x[r, c1] + y[r, c, r, c1] * 9
            m += x[r, c] >= x[r, c1] + 1 - (1 - y[r, c, r, c1]) * 9
    # Unique value per column
    for c in columns:
        for (r, r1) in combinations(rows, 2):
            m += x[r, c] + 1 <= x[r1, c] + y[r, c, r1, c] * 9
            m += x[r, c] >= x[r1, c] + 1 - (1 - y[r, c, r1, c]) * 9
    # Unique value per box
    for box in boxes:
        for ((r, c), (r1, c1)) in combinations(box, 2):
            m += x[r, c] + 1 <= x[r1, c1] + y[r, c, r1, c1] * 9
            m += x[r, c] >= x[r1, c1] + 1 - (1 - y[r, c, r1, c1]) * 9

    # Optimize statement
    m.optimize()

    # Track and print execution time
    t_end = time.time()
    print(
        f"Elapsed second for solution with {solver_name}: {t_end-t_start} seconds."
    )

    # Print solution
    for r in rows:
        if (r - 1) % 3 == 0:
            print("+-------+-------+-------+")
        line = ""
        for c in columns:
            if (c - 1) % 3 == 0:
                line += "| "
            line += f"{int(x[r, c].x)} "
            if c == 9:
                line += "|"
        print(line)
    print("+-------+-------+-------+")
