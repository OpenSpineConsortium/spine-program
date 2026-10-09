"""Independent re-derivation of the Wilson lower bounds quoted in SchwingNet/results/power/power.json and
power_table.json (Topic 2 handoff note). Pure arithmetic, no repository code imported."""
import math

Z = 1.959964


def wilson_lower(k_correct, n):
    p = k_correct / n
    den = 1 + Z * Z / n
    centre = p + Z * Z / (2 * n)
    half = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n))
    return (centre - half) / den


def first_n(errors, target):
    for n in range(errors + 1, 5000):
        if wilson_lower(n - errors, n) >= target:
            return n
    return None


for k in (0, 1, 2, 5):
    print(f"errors {k}: n for 90% = {first_n(k, 0.90)}, n for 85% = {first_n(k, 0.85)}")
for n in (7, 37, 51, 89):
    print(f"error-free Wilson lower bound at n={n}: {100 * wilson_lower(n, n):.2f} %")
for n in (30, 45, 60, 100):
    print(f"n={n}, 0 errors: {100 * wilson_lower(n, n):.2f}")
