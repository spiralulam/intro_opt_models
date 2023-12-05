import time

import pandas as pd
from mip import BINARY, CBC, GUROBI, Model, xsum

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
    values = range(1, 10)
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
    m = Model("Sudoku binary", solver_name=solver_name)

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
            val = int(sum(y[r, c, v].x * v for v in values))
            line += f"{val} "
            if c == 9:
                line += "|"
        print(line)
    print("+-------+-------+-------+")
