from mip import CBC, Model, minimize, xsum

numbers = [
    1, 34, 5, 6, 3, 7, 8, 5, 6, 89, 4, 56,
    234, 5, 6, 3457, 8, 45, 2, 35, 3
]

m = Model(solver_name=CBC)

x = m.add_var(lb=-float("inf"))

z = {n: m.add_var() for n in numbers}

for n in numbers:
    m += n - x <= z[n]
    m += -(n - x) <= z[n]

m.objective = minimize(1 / len(numbers) * xsum(z[n] for n in numbers))

m.optimize()

print(f"MAE minimizing number: {x.x}")
