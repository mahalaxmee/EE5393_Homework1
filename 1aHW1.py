"""
Reactions:
  R1: 2X1 + X2 -> 4X3   k1 = 1
  R2: X1 + 2X3 -> 3X2   k2 = 2
  R3: X2 + X3  -> 2X1   k3 = 3

Starting state: [110, 26, 55]
Outcomes:
  C1: x1 >= 150
  C2: x2 < 10
  C3: x3 > 100
"""

import random

def propensities(x1, x2, x3):
    """Compute propensities for R1, R2, R3."""
    # R1: needs 2 X1 and 1 X2 -> C(x1,2) * x2 * k1
    a1 = (x1 * (x1 - 1) / 2) * x2 * 1  if x1 >= 2 and x2 >= 1 else 0
    # R2: needs 1 X1 and 2 X3 -> x1 * C(x3,2) * k2
    a2 = x1 * (x3 * (x3 - 1) / 2) * 2  if x1 >= 1 and x3 >= 2 else 0
    # R3: needs 1 X2 and 1 X3 -> x2 * x3 * k3
    a3 = x2 * x3 * 3                     if x2 >= 1 and x3 >= 1 else 0
    return a1, a2, a3

def gillespie_step(x1, x2, x3):
    """Perform one Gillespie step. Returns new state and which reaction fired."""
    a1, a2, a3 = propensities(x1, x2, x3)
    total = a1 + a2 + a3
    if total == 0:
        return x1, x2, x3, None  # absorbed / stuck

    # Choose which reaction fires
    u = random.random() * total
    if u < a1:
        rxn = 1
    elif u < a1 + a2:
        rxn = 2
    else:
        rxn = 3

    # Apply state changes
    if rxn == 1:   # 2X1 + X2 -> 4X3
        x1 -= 2; x2 -= 1; x3 += 4
    elif rxn == 2: # X1 + 2X3 -> 3X2
        x1 -= 1; x2 += 3; x3 -= 2
    else:          # X2 + X3 -> 2X1
        x1 += 2; x2 -= 1; x3 -= 1

    return x1, x2, x3, rxn

def run_simulation(x1_init, x2_init, x3_init, max_steps=5000):
    """
    Run one simulation trajectory.
    Returns a dict of which outcome conditions were EVER met.
    """
    x1, x2, x3 = x1_init, x2_init, x3_init
    hit_C1 = x1 >= 150
    hit_C2 = x2 < 10
    hit_C3 = x3 > 100

    for _ in range(max_steps):
        if hit_C1 and hit_C2 and hit_C3:
            break  # all found, no need to continue
        x1, x2, x3, rxn = gillespie_step(x1, x2, x3)
        if rxn is None:
            break  # stuck
        if x1 >= 150: hit_C1 = True
        if x2 < 10:   hit_C2 = True
        if x3 > 100:  hit_C3 = True

    return hit_C1, hit_C2, hit_C3

# ── Monte Carlo ──────────────────────────────────────────────────────────────
N_RUNS = 10_000
random.seed(42)

count_C1 = count_C2 = count_C3 = 0

for _ in range(N_RUNS):
    c1, c2, c3 = run_simulation(110, 26, 55)
    if c1: count_C1 += 1
    if c2: count_C2 += 1
    if c3: count_C3 += 1

print("=" * 50)
print("Problem 1(a) Results")
print(f"Number of simulations: {N_RUNS}")
print(f"Starting state: [110, 26, 55]")
print("=" * 50)
print(f"Pr(C1) — x1 >= 150:  {count_C1/N_RUNS:.4f}  ({count_C1}/{N_RUNS})")
print(f"Pr(C2) — x2 <  10:   {count_C2/N_RUNS:.4f}  ({count_C2}/{N_RUNS})")
print(f"Pr(C3) — x3 > 100:   {count_C3/N_RUNS:.4f}  ({count_C3}/{N_RUNS})")
print("=" * 50)

# ── Sanity check: verify firing probabilities at [3,3,3] match the HW ────────
a1, a2, a3 = propensities(3, 3, 3)
tot = a1 + a2 + a3
print(f"\nSanity check at [3,3,3]:")
print(f"  p1 = {a1/tot:.4f}  (expected 1/6 = {1/6:.4f})")
print(f"  p2 = {a2/tot:.4f}  (expected 1/3 = {1/3:.4f})")
print(f"  p3 = {a3/tot:.4f}  (expected 1/2 = {1/2:.4f})")
