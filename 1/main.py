# Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.

# For example:

# For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to get 2.
# For a mass of 14, dividing by 3 and rounding down still yields 4, so the fuel required is also 2.
# For a mass of 1969, the fuel required is 654.
# For a mass of 100756, the fuel required is 33583.

import math

def fuel_required(remaining_mass, total_mass = 0):
    if remaining_mass <= 8:
        return total_mass

    amt = math.floor(remaining_mass / 3) - 2
    return fuel_required(amt, total_mass+amt)

data_filename = 'input.txt'
with open(data_filename) as f:
    lines = f.readlines()

masses = [int(l) for l in lines]

fuel_amts = [fuel_required(mass) for mass in masses]

print(sum(fuel_amts))