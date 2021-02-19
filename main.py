import matplotlib.pyplot as plt
import numpy as np
import random

# VARIABLES
N = int(input("Number of sections, N = "))
P = float(input("Probability of finding leak in section with leak, p = "))
tests = int(input("Number of simulations per strategy x, t = "))  # number of tests per x_range value

print("\nCOST")

# COST VALUES
cost_fix = float(input("Cost of fixing leak, C_F = "))
cost_replace = float(input("Cost of replacing pipeline, C_R = "))
cost_check = float(input("Cost of checking each section, C_L = "))


def average(values: list):
    return sum(values) / len(values)


def bernoulli(prob, res=100000):
    # performs a bernoulli trial

    sample = random.randint(0, res)
    return sample <= prob * res


def simulate_check(r, n, p_f):
    # choose random leak location, between 1 and n inclusive
    leak = random.randint(1, n)

    # for each section i up to r
    for i in range(1, r + 1):

        # check if leak is in this section
        if i == leak:
            # if it is, do we find it?
            find = bernoulli(p_f)
            if find:
                # found.
                return (i * cost_check) + cost_fix

    return (r * cost_check) + cost_replace


def expected_checked(x):
    f = (P + 2 * N) * x - P * pow(x, 2)
    return f / (2 * N)


def expected_cost(x):
    A = -cost_check * P
    B = (2 * N + P) * cost_check + 2 * P * (cost_fix - cost_replace)

    return cost_replace + (A * pow(x, 2) + B * x) / (2 * N)


x_range = list(range(0, N + 1))  # strategy range
y = []

for s in x_range:

    outcomes = []

    for t in range(tests):
        # run cost simulation
        cost = simulate_check(s, N, P)

        outcomes.append(cost)

    y.append(average(outcomes))

ax = plt.gca()
ax.set_xticks(x_range)
plt.bar(x_range, y, color="#d5edc7")

x_func = np.linspace(0, N, 100)
y_func = expected_cost(x_func)  # [expected_cost(i) for i in x_range]
plt.plot(x_func, y_func, 'r', label="Expected Cost, C_x")

ax.set_xlabel("x, sections checked before giving up")
ax.set_ylabel(f"Average Cost over {tests} simulations")
plt.title(
    f"""Average of Cost (each over {tests} simulations) Against Strategy x.
N={N}, p={P}, C_F={cost_fix}, C_R={cost_replace}, C_L={cost_check}.""")

plt.legend()


plt.show()
