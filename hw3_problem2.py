"""
EE 5393 - Circuits, Computation and Biology
Homework #1 — Python verification code
Problems 2(a) and 2(b): Transforming Probabilities
"""

from fractions import Fraction


# ---------------------------------------------------------------------------
# Evaluation helpers
# ---------------------------------------------------------------------------

def AND(p, q):
    return p * q

def NOT(p):
    return 1 - p


# ---------------------------------------------------------------------------
# Problem 2(a) — Exact synthesis from S = {0.4, 0.5}
# ---------------------------------------------------------------------------

def problem_2a():
    A = Fraction(4, 10)   # 0.4
    B = Fraction(1, 2)    # 0.5

    print("=" * 60)
    print("Problem 2(a): Exact synthesis from S = {0.4, 0.5}")
    print("=" * 60)

    # --- i. Target 0.8881188 ---
    print("\n--- i. Target: 0.8881188 ---")
    u1  = AND(B, B)
    u2  = AND(A, A)
    u3  = NOT(A)
    u4  = AND(A, B)
    u5  = NOT(AND(u4, A))
    u6  = AND(u1, u5)
    u7  = NOT(u1)
    u8  = AND(u1, u2)
    u9  = AND(u7, u8)
    u10 = AND(u3, u2)
    u11 = NOT(u10)
    u12 = AND(u9, u11)
    u13 = NOT(u12)
    u14 = AND(B, u6)
    u15 = AND(u14, u13)
    fi  = NOT(u15)

    steps_i = [
        ("u1",  "AND(B,B)",        u1),
        ("u2",  "AND(A,A)",        u2),
        ("u3",  "NOT(A)",          u3),
        ("u4",  "AND(A,B)",        u4),
        ("u5",  "NOT(AND(u4,A))",  u5),
        ("u6",  "AND(u1,u5)",      u6),
        ("u7",  "NOT(u1)",         u7),
        ("u8",  "AND(u1,u2)",      u8),
        ("u9",  "AND(u7,u8)",      u9),
        ("u10", "AND(u3,u2)",      u10),
        ("u11", "NOT(u10)",        u11),
        ("u12", "AND(u9,u11)",     u12),
        ("u13", "NOT(u12)",        u13),
        ("u14", "AND(B,u6)",       u14),
        ("u15", "AND(u14,u13)",    u15),
        ("f",   "NOT(u15)",        fi),
    ]
    print(f"{'Signal':<8} {'Operation':<22} {'Exact (Fraction)':<25} {'Decimal'}")
    print("-" * 70)
    for name, op, val in steps_i:
        print(f"{name:<8} {op:<22} {str(val):<25} {float(val):.7f}")
    print(f"\nResult: {float(fi):.7f}  (target 0.8881188)  match={abs(float(fi)-0.8881188)<1e-9}")

    # --- ii. Target 0.2119209 ---
    print("\n--- ii. Target: 0.2119209 ---")
    u1  = AND(A, B)
    u2  = NOT(u1)
    u3  = AND(B, B)
    u4  = NOT(u3)
    u5  = NOT(A)
    u6  = AND(u5, u5)
    u7  = AND(u4, u6)
    u8  = NOT(u7)
    u9  = AND(u3, u5)
    u10 = AND(u4, u9)
    u11 = NOT(u10)
    u12 = AND(u3, u3)
    u13 = AND(u1, A)
    u14 = NOT(u13)
    u15 = AND(u12, A)
    u16 = AND(u15, u14)
    u17 = AND(u8, u11)
    u18 = AND(u16, u17)
    u19 = NOT(u18)
    u20 = AND(u2, u19)
    fii = NOT(u20)

    steps_ii = [
        ("u1",  "AND(A,B)",    u1),
        ("u2",  "NOT(u1)",     u2),
        ("u3",  "AND(B,B)",    u3),
        ("u4",  "NOT(u3)",     u4),
        ("u5",  "NOT(A)",      u5),
        ("u6",  "AND(u5,u5)",  u6),
        ("u7",  "AND(u4,u6)",  u7),
        ("u8",  "NOT(u7)",     u8),
        ("u9",  "AND(u3,u5)",  u9),
        ("u10", "AND(u4,u9)",  u10),
        ("u11", "NOT(u10)",    u11),
        ("u12", "AND(u3,u3)",  u12),
        ("u13", "AND(u1,A)",   u13),
        ("u14", "NOT(u13)",    u14),
        ("u15", "AND(u12,A)",  u15),
        ("u16", "AND(u15,u14)",u16),
        ("u17", "AND(u8,u11)", u17),
        ("u18", "AND(u16,u17)",u18),
        ("u19", "NOT(u18)",    u19),
        ("u20", "AND(u2,u19)", u20),
        ("f",   "NOT(u20)",    fii),
    ]
    print(f"{'Signal':<8} {'Operation':<22} {'Exact (Fraction)':<30} {'Decimal'}")
    print("-" * 75)
    for name, op, val in steps_ii:
        print(f"{name:<8} {op:<22} {str(val):<30} {float(val):.7f}")
    print(f"\nResult: {float(fii):.7f}  (target 0.2119209)  match={abs(float(fii)-0.2119209)<1e-9}")

    # --- iii. Target 0.5555555 ---
    print("\n--- iii. Target: 0.5555555 ---")
    u1  = AND(B, B)
    u2  = NOT(u1)
    u3  = AND(u1, A)
    u4  = AND(u2, u3)
    u5  = NOT(u4)
    u6  = AND(A, A)
    u7  = NOT(u6)
    u8  = AND(B, A)
    u9  = AND(u7, u8)
    u10 = NOT(A)
    u11 = AND(u8, u10)
    u12 = NOT(u11)
    u13 = AND(u9, u12)
    u14 = AND(u2, u1)
    u15 = NOT(u14)
    u16 = AND(u15, u13)
    u17 = AND(u5, u16)
    u18 = NOT(u17)
    u19 = AND(B, u18)
    fiii = NOT(u19)

    steps_iii = [
        ("u1",  "AND(B,B)",    u1),
        ("u2",  "NOT(u1)",     u2),
        ("u3",  "AND(u1,A)",   u3),
        ("u4",  "AND(u2,u3)",  u4),
        ("u5",  "NOT(u4)",     u5),
        ("u6",  "AND(A,A)",    u6),
        ("u7",  "NOT(u6)",     u7),
        ("u8",  "AND(B,A)",    u8),
        ("u9",  "AND(u7,u8)",  u9),
        ("u10", "NOT(A)",      u10),
        ("u11", "AND(u8,u10)", u11),
        ("u12", "NOT(u11)",    u12),
        ("u13", "AND(u9,u12)", u13),
        ("u14", "AND(u2,u1)",  u14),
        ("u15", "NOT(u14)",    u15),
        ("u16", "AND(u15,u13)",u16),
        ("u17", "AND(u5,u16)", u17),
        ("u18", "NOT(u17)",    u18),
        ("u19", "AND(B,u18)",  u19),
        ("f",   "NOT(u19)",    fiii),
    ]
    print(f"{'Signal':<8} {'Operation':<22} {'Exact (Fraction)':<30} {'Decimal'}")
    print("-" * 75)
    for name, op, val in steps_iii:
        print(f"{name:<8} {op:<22} {str(val):<30} {float(val):.7f}")
    print(f"\nResult: {float(fiii):.7f}  (target 0.5555555)  match={abs(float(fiii)-0.5555555)<1e-9}")


# ---------------------------------------------------------------------------
# Problem 2(b) — Binary fractions from S = {0.5}
# ---------------------------------------------------------------------------

def problem_2b():
    H = Fraction(1, 2)

    print("\n" + "=" * 60)
    print("Problem 2(b): Binary fractions from S = {0.5}")
    print("Recursion: b1=0 -> AND(H,q);  b1=1 -> NOT(AND(H,NOT(q)))")
    print("=" * 60)

    # --- i. 0.1011111_2 = 95/128 ---
    print("\n--- i. 0.1011111_2 ---")
    steps = []
    p1 = H;                             steps.append(("0.1",       "H (source)",              p1))
    p2 = NOT(AND(H, NOT(p1)));          steps.append(("0.11",      "NOT(AND(H,NOT(p1)))",     p2))
    p3 = NOT(AND(H, NOT(p2)));          steps.append(("0.111",     "NOT(AND(H,NOT(p2)))",     p3))
    p4 = NOT(AND(H, NOT(p3)));          steps.append(("0.1111",    "NOT(AND(H,NOT(p3)))",     p4))
    p5 = NOT(AND(H, NOT(p4)));          steps.append(("0.11111",   "NOT(AND(H,NOT(p4)))",     p5))
    q  = AND(H, p5);                    steps.append(("0.011111",  "AND(H,p5)",               q))
    t1 = NOT(AND(H, NOT(q)));           steps.append(("0.1011111", "NOT(AND(H,NOT(q)))",      t1))
    expected1 = Fraction(95, 128)
    print(f"{'Value':<14} {'Construction':<30} {'Decimal':<12} {'Exact Frac'}")
    print("-" * 68)
    for lbl, desc, v in steps:
        print(f"{lbl:<14} {desc:<30} {float(v):<12.7f} {v}")
    print(f"\nResult: {t1} = {float(t1):.7f}   match={t1==expected1}")

    # --- ii. 0.1101111_2 = 111/128 ---
    print("\n--- ii. 0.1101111_2 ---")
    steps = []
    p1 = H;                             steps.append(("0.1",       "H (source)",              p1))
    p2 = NOT(AND(H, NOT(p1)));          steps.append(("0.11",      "NOT(AND(H,NOT(p1)))",     p2))
    p3 = NOT(AND(H, NOT(p2)));          steps.append(("0.111",     "NOT(AND(H,NOT(p2)))",     p3))
    p4 = NOT(AND(H, NOT(p3)));          steps.append(("0.1111",    "NOT(AND(H,NOT(p3)))",     p4))
    q1 = AND(H, p4);                    steps.append(("0.01111",   "AND(H,p4)",               q1))
    q2 = NOT(AND(H, NOT(q1)));          steps.append(("0.101111",  "NOT(AND(H,NOT(q1)))",     q2))
    t2 = NOT(AND(H, NOT(q2)));          steps.append(("0.1101111", "NOT(AND(H,NOT(q2)))",     t2))
    expected2 = Fraction(111, 128)
    print(f"{'Value':<14} {'Construction':<30} {'Decimal':<12} {'Exact Frac'}")
    print("-" * 68)
    for lbl, desc, v in steps:
        print(f"{lbl:<14} {desc:<30} {float(v):<12.7f} {v}")
    print(f"\nResult: {t2} = {float(t2):.7f}   match={t2==expected2}")

    # --- iii. 0.1010111_2 = 87/128 ---
    print("\n--- iii. 0.1010111_2 ---")
    steps = []
    p1 = H;                             steps.append(("0.1",       "H (source)",              p1))
    p2 = NOT(AND(H, NOT(p1)));          steps.append(("0.11",      "NOT(AND(H,NOT(p1)))",     p2))
    p3 = NOT(AND(H, NOT(p2)));          steps.append(("0.111",     "NOT(AND(H,NOT(p2)))",     p3))
    q1 = AND(H, p3);                    steps.append(("0.0111",    "AND(H,p3)",               q1))
    q2 = NOT(AND(H, NOT(q1)));          steps.append(("0.10111",   "NOT(AND(H,NOT(q1)))",     q2))
    q3 = AND(H, q2);                    steps.append(("0.010111",  "AND(H,q2)",               q3))
    t3 = NOT(AND(H, NOT(q3)));          steps.append(("0.1010111", "NOT(AND(H,NOT(q3)))",     t3))
    expected3 = Fraction(87, 128)
    print(f"{'Value':<14} {'Construction':<30} {'Decimal':<12} {'Exact Frac'}")
    print("-" * 68)
    for lbl, desc, v in steps:
        print(f"{lbl:<14} {desc:<30} {float(v):<12.7f} {v}")
    print(f"\nResult: {t3} = {float(t3):.7f}   match={t3==expected3}")


# ---------------------------------------------------------------------------
# Problem 1(c) verification — Bernstein polynomial evaluation
# ---------------------------------------------------------------------------

def bernstein_poly(coeffs, t):
    """Evaluate degree-n Bernstein polynomial with given coefficients at t."""
    n = len(coeffs) - 1
    from math import comb
    result = Fraction(0)
    t = Fraction(t)
    for k, bk in enumerate(coeffs):
        result += Fraction(bk) * comb(n, k) * t**k * (1 - t)**(n - k)
    return result


def problem_1c():
    print("\n" + "=" * 60)
    print("Problem 1(c): Bernstein polynomial verification")
    print("p(t) = (31/32)t^5 + (5/32)t^4 - (5/8)t^3 + (5/4)t^2 - (5/4)t + 1/2")
    print("=" * 60)

    def p_exact(t):
        t = Fraction(t)
        return (Fraction(31,32)*t**5 + Fraction(5,32)*t**4
                - Fraction(5,8)*t**3 + Fraction(5,4)*t**2
                - Fraction(5,4)*t + Fraction(1,2))

    bk = [Fraction(1,2), Fraction(1,4), Fraction(1,8),
          Fraction(1,16), Fraction(1,32), Fraction(1,1)]

    test_pts = [Fraction(0), Fraction(1,4), Fraction(1,2), Fraction(3,4), Fraction(1)]
    print(f"\n{'X':<8} {'p(X) exact':<20} {'Bernstein eval':<20} {'Decimal':<12} {'Match'}")
    print("-" * 72)
    for t in test_pts:
        px = p_exact(t)
        bx = bernstein_poly(bk, t)
        print(f"{str(t):<8} {str(px):<20} {str(bx):<20} {float(px):<12.9f} {px==bx}")

    print("\nBernstein coefficients confirmed: b = [1/2, 1/4, 1/8, 1/16, 1/32, 1]")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    problem_2a()
    problem_2b()
    problem_1c()
