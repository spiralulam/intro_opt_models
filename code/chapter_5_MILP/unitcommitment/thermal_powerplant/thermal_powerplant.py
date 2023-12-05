from mip import BINARY, CBC, minimize, Model, xsum

# Data

# Demand
demand = [310.0,
 322.3523806378151,
 401.5,
 424.3883476483185,
 455.25317547305485,
 418.7407282861335,
 459.0,
 433.7407282861335,
 458.25317547305485,
 372.3883476483185,
 399.5,
 358.35238063781514,
 341.0,
 306.6476193621849,
 237.5,
 243.6116523516816,
 180.7468245269452,
 156.25927171386647,
 182.0,
 206.25927171386644,
 265.74682452694515,
 189.61165235168153,
 265.49999999999994,
 287.6476193621848]

# Last hour of planning horizon
T_max = len(demand)

# Hours
hours = range(T_max)

# Minimum and maximum power output
P_max = 500
P_min = 100

# Maximum ramping rate
delta_max = 120

# Minimum down time
L_min = 8

# Variable production costs
c = 40

# Start-up costs
S = 50000

# Optimization model

# Model declaration
m = Model("Unit commitment", solver_name=CBC)

# Decision variables

# Power production
p = {t: m.add_var(ub=P_max) for t in hours}

# on/off status of power plant
y = {t: m.add_var(var_type=BINARY) for t in hours}

# On switch
delta_on = {t: m.add_var(var_type=BINARY) for t in hours}

# Off switch
delta_off = {t: m.add_var(var_type=BINARY) for t in hours}

# Constraints

# Fix the status variable of "Thermi" for the first hour.
m += y[0] == 1

# Cover demand in each hour
for t in hours:
    m += p[t] >= demand[t]

# The maximum ramping rate must not be exceeded.
for t in hours[1:]:
    m += p[t]-p[t-1] <= delta_max
    m += p[t-1]-p[t] <= delta_max

# Thermi must generate power within its lower and upper limits.
for t in hours:
    m += p[t] <= P_max*y[t]
    m += p[t] >= P_min*y[t]

# The powerplant cannot be put on and off in the same hour
for t in hours:
    m += delta_on[t]+delta_off[t] <= 1

# Linking constraints between on/off status variables and on/off switches
for t in hours[1:]:
    m += y[t] == y[t-1]+delta_on[t]-delta_off[t]

# Minimal down-time constraint part 1
for t in hours[:-L_min+1]:
    m += \
        L_min * delta_off[t] <= \
        sum(1-y[s] for s in range(t, t+L_min))

# Minimal down-time constraint part 2 (last hours)
for t in hours[T_max - L_min + 1:]:
    i = t - T_max + L_min - 1
    m += \
        L_min * delta_off[t] - i <= \
        sum(1-y[s] for s in range(t, T_max))

# Objective
m.objective = minimize(
    xsum( (p[t]*c + delta_on[t]*S) for t in hours)
)

# Solve statement
m.optimize()
