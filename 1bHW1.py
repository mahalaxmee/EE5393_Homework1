import random
import statistics

def propensities(x1, x2, x3):
    a1 = (x1 * (x1 - 1) / 2) * x2 * 1  if x1 >= 2 and x2 >= 1 else 0
    a2 = x1 * (x3 * (x3 - 1) / 2) * 2  if x1 >= 1 and x3 >= 2 else 0
    a3 = x2 * x3 * 3                     if x2 >= 1 and x3 >= 1 else 0
    return a1, a2, a3

def gillespie_step(x1, x2, x3):
    a1, a2, a3 = propensities(x1, x2, x3)
    total = a1 + a2 + a3
    if total == 0:
        return x1, x2, x3, None

    u = random.random() * total
    if u < a1:       # R1: 2X1 + X2 -> 4X3
        x1 -= 2; x2 -= 1; x3 += 4
    elif u < a1+a2:  # R2: X1 + 2X3 -> 3X2
        x1 -= 1; x2 += 3; x3 -= 2
    else:            # R3: X2 + X3 -> 2X1
        x1 += 2; x2 -= 1; x3 -= 1
    return x1, x2, x3, 1

def run_7_steps(x1_init, x2_init, x3_init):
    """Run exactly 7 steps (skip step if system is stuck)."""
    x1, x2, x3 = x1_init, x2_init, x3_init
    steps_done = 0
    while steps_done < 7:
        x1, x2, x3, rxn = gillespie_step(x1, x2, x3)
        if rxn is None:
            break   # stuck, can't fire — record where we are
        steps_done += 1
    return x1, x2, x3

# ── Monte Carlo ───────────────────────────────────────────────────────────────
N_RUNS = 100_000
random.seed(42)

samples_x1, samples_x2, samples_x3 = [], [], []

for _ in range(N_RUNS):
    x1, x2, x3 = run_7_steps(9, 8, 7)
    samples_x1.append(x1)
    samples_x2.append(x2)
    samples_x3.append(x3)

def mean_var(samples):
    n = len(samples)
    m = sum(samples) / n
    v = sum((s - m)**2 for s in samples) / (n - 1)
    return m, v

m1, v1 = mean_var(samples_x1)
m2, v2 = mean_var(samples_x2)
m3, v3 = mean_var(samples_x3)

print("=" * 55)
print("Problem 1(b) — Distribution after exactly 7 steps")
print(f"Starting state: [9, 8, 7]   |   N = {N_RUNS:,} runs")
print("=" * 55)
print(f"{'Species':<10} {'Mean':>12} {'Variance':>14} {'Std Dev':>12}")
print("-" * 55)
print(f"{'X1':<10} {m1:>12.4f} {v1:>14.4f} {v1**0.5:>12.4f}")
print(f"{'X2':<10} {m2:>12.4f} {v2:>14.4f} {v2**0.5:>12.4f}")
print(f"{'X3':<10} {m3:>12.4f} {v3:>14.4f} {v3**0.5:>12.4f}")
print("=" * 55)

# ── Show distribution of X1 for illustration ──────────────────────────────
from collections import Counter
print("\nX1 distribution snapshot (top values):")
cnt = Counter(samples_x1)
total = sum(cnt.values())
for val in sorted(cnt.keys()):
    bar = "#" * int(cnt[val]/total*50)
    print(f"  X1={val:3d}: {cnt[val]/total:.4f}  {bar}")
