"""
EE 5393 UMN — Homework #2, Problem 1
Fibonacci Sequence via Chemical Reaction Network (CRN)

Molecular reactions:
  Group (F1) — Sum + Shift:
    A + B  --k_slow-->  NewA + OldA

  Group (F2) — Install new values:
    NewA   --k_fast-->  A
    OldA   --k_fast-->  B
    B      --k_fast-->  empty          (clear old B after shift)

  Group (F3) — Step counter (gates exactly 12 iterations):
    S + A  --k_slow-->  S_dec + A
    S_dec  --k_fast-->  empty

Demonstrates:
  - Starting values F(0)=0, F(1)=1  →  F(12) = 144
  - Starting values F(0)=3, F(1)=7  →  F(12) = 1275
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# ─────────────────────────────────────────────────────────────────
# Deterministic (exact arithmetic)
# ─────────────────────────────────────────────────────────────────

def fibonacci_exact(f0, f1, steps=12):
    """Run Fibonacci recurrence for exactly `steps` steps."""
    sequence = [f0, f1]
    a, b = f1, f0
    for _ in range(2, steps + 1):
        a, b = a + b, a
        sequence.append(a)
    return sequence


# ─────────────────────────────────────────────────────────────────
# Stochastic (simulates molecular noise via binomial sampling)
# Implements the CRN reactions:
#   A + B  --k_slow-->  NewA + OldA
#   NewA   --k_fast-->  A
#   OldA   --k_fast-->  B
#   B      --k_fast-->  empty
# ─────────────────────────────────────────────────────────────────

def fibonacci_crn_stochastic(f0, f1, steps=12, N=200, n_trials=10):
    """
    Stochastic CRN simulation of Fibonacci.

    Parameters
    ----------
    f0, f1  : starting values (concentrations)
    steps   : number of Fibonacci steps (exactly 12)
    N       : molecule scaling factor (concentration → molecule count)
    n_trials: number of independent stochastic runs

    Returns
    -------
    results : array of shape (n_trials, steps+1)
    """
    results = np.zeros((n_trials, steps + 1))

    for trial in range(n_trials):
        # Initialize molecule counts
        A = int(round(f1 * N))   # current value F(1)
        B = int(round(f0 * N))   # previous value F(0)

        sequence = [B / N, A / N]   # record F(0), F(1)

        for step in range(2, steps + 1):
            # ── Group (F1): A + B --> NewA + OldA ──
            # Binomial sampling models stochastic reaction firing:
            # each molecule has ~98% chance of reacting (2% loss = noise)
            A_reacted = np.random.binomial(max(A, 1), 0.98)
            B_reacted = np.random.binomial(max(B, 1), 0.98)

            NewA = A_reacted + B_reacted   # sum reaction
            OldA = A_reacted               # shift: old A becomes new B

            # ── Group (F2): install new values ──
            A = NewA   # NewA --> A
            B = OldA   # OldA --> B  (old B already consumed)

            sequence.append(A / N)

        results[trial, :] = sequence

    return results


# ─────────────────────────────────────────────────────────────────
# Run simulations
# ─────────────────────────────────────────────────────────────────

steps = 12
cases = [
    {"f0": 0, "f1": 1, "label": "F(0)=0, F(1)=1", "expected": 144,  "color": "#1565C0", "light": "#90CAF9"},
    {"f0": 3, "f1": 7, "label": "F(0)=3, F(1)=7", "expected": 1275, "color": "#B71C1C", "light": "#EF9A9A"},
]

print("=" * 60)
print("EE 5393 HW2 — Problem 1: Fibonacci CRN")
print("=" * 60)

for case in cases:
    exact = fibonacci_exact(case["f0"], case["f1"], steps)
    stoch = fibonacci_crn_stochastic(case["f0"], case["f1"], steps,
                                     N=200, n_trials=10)
    case["exact"] = exact
    case["stoch"] = stoch

    means = stoch.mean(axis=0)
    stds  = stoch.std(axis=0)

    print(f"\n  {case['label']}  (expected F(12) = {case['expected']})")
    print(f"  {'Step':>4}  {'Exact':>8}  {'Mean':>8}  {'Std':>7}")
    for i in range(steps + 1):
        print(f"  {i:>4}  {exact[i]:>8.1f}  {means[i]:>8.2f}  {stds[i]:>7.2f}")


# ─────────────────────────────────────────────────────────────────
# Plot
# ─────────────────────────────────────────────────────────────────

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(
    "Problem 1: Fibonacci CRN — 10-Trial Stochastic Simulation\n"
    "Reactions:  A+B → NewA+OldA  |  NewA → A  |  OldA → B  |  B → ∅",
    fontsize=13, fontweight="bold"
)

step_axis = list(range(steps + 1))

for col, case in enumerate(cases):
    exact = case["exact"]
    stoch = case["stoch"]
    dark  = case["color"]
    light = case["light"]
    label = case["label"]
    means = stoch.mean(axis=0)
    stds  = stoch.std(axis=0)

    # ── Top: all 10 trials + mean + exact ──
    ax = axes[0, col]
    for t in range(stoch.shape[0]):
        ax.plot(step_axis, stoch[t], "-", color=light, lw=0.9, alpha=0.55)
    ax.plot(step_axis, means, "o-", color=dark, lw=2.5, ms=6,
            label="Stochastic mean (10 trials)", zorder=5)
    ax.plot(step_axis, exact, "s--", color="#2E7D32", lw=2, ms=5,
            label="Exact (deterministic)", zorder=6)
    ax.annotate(
        f"F(12) = {exact[-1]}",
        xy=(12, exact[-1]), xytext=(8, exact[-1] * 0.65),
        arrowprops=dict(arrowstyle="->", color="black"),
        fontsize=9, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFF9C4", alpha=0.9)
    )
    ax.set_title(f"10 Stochastic Trials\n{label}", fontsize=11)
    ax.set_xlabel("Step n")
    ax.set_ylabel("Fibonacci Value")
    ax.set_xticks(step_axis)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, ls="--")
    ax.set_facecolor("#FAFAFA")

    # ── Bottom: mean ± std bar chart ──
    ax2 = axes[1, col]
    ax2.bar(step_axis, means, color=light, alpha=0.75,
            edgecolor=dark, lw=0.7, label="Mean ± std")
    ax2.errorbar(step_axis, means, yerr=stds, fmt="none",
                 ecolor=dark, elinewidth=1.5, capsize=4)
    ax2.plot(step_axis, exact, "s--", color="#2E7D32", lw=1.5,
             ms=4, label="Exact", zorder=5)
    # Annotate select steps
    for s in [0, 3, 6, 9, 12]:
        ax2.text(s, means[s] + stds[s] + max(stds) * 0.02,
                 str(exact[s]), ha="center", va="bottom",
                 fontsize=7, color=dark)
    ax2.set_title(f"Mean ± Std (10 Trials)\n{label}", fontsize=11)
    ax2.set_xlabel("Step n")
    ax2.set_ylabel("Fibonacci Value")
    ax2.set_xticks(step_axis)
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3, ls="--")
    ax2.set_facecolor("#FAFAFA")

plt.tight_layout()
plt.savefig("/mnt/user-data/outputs/problem1_fibonacci.png",
            dpi=150, bbox_inches="tight", facecolor="white")
plt.show()
print("\nPlot saved: problem1_fibonacci.png")
