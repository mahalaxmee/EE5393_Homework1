from itertools import product

# ------------------------------------------------------------
# Helper functions for permutations
# ------------------------------------------------------------

def cycle_map(cycle):
    """
    Convert cycle notation such as (1, 4, 3, 5, 2)
    into mapping form.
    """
    mapping = {i: i for i in range(1, 6)}

    for i, value in enumerate(cycle):
        mapping[value] = cycle[(i + 1) % len(cycle)]

    return tuple(mapping[i] for i in range(1, 6))


def inverse(p):
    """
    Return the inverse of a permutation.
    """
    q = [0] * 5

    for i, value in enumerate(p, start=1):
        q[value - 1] = i

    return tuple(q)


def compose(p, q):
    """
    Compose two permutations.
    This applies q first and then p.
    """
    return tuple(p[q[i - 1] - 1] for i in range(1, 6))


def compose_left_to_right(seq):
    """
    Apply permutations in the same left-to-right order
    used in the homework sequences.
    """
    result = IDENTITY

    for p in seq:
        result = compose(p, result)

    return result


# ------------------------------------------------------------
# Given permutations
# ------------------------------------------------------------

IDENTITY = tuple(range(1, 6))

A = cycle_map((1, 4, 3, 5, 2))
B = cycle_map((1, 4, 5, 2, 3))
C = cycle_map((1, 3, 4, 2, 5))
D = cycle_map((1, 2, 4, 5, 3))
E = cycle_map((1, 4, 2, 3, 5))

perms = {
    "A": A,
    "B": B,
    "C": C,
    "D": D,
    "E": E,
    "*": IDENTITY
}


def parse_product(text):
    """
    Convert a product such as C'B or D'B'
    into the corresponding permutation.
    """
    text = text.strip()

    if text == "*":
        return IDENTITY

    seq = []
    i = 0

    while i < len(text):
        ch = text[i]

        if ch in perms and ch != "*":
            p = perms[ch]

            if i + 1 < len(text) and text[i + 1] == "'":
                p = inverse(p)
                i += 1

            seq.append(p)

        i += 1

    return compose_left_to_right(seq)


def evaluate_sequence(sequence, values):
    """
    Evaluate one conditional permutation sequence
    for a given assignment of x1, x2, and x3.
    """
    result = IDENTITY

    for variable, true_perm, false_perm in sequence:
        selected = true_perm if values[variable] else false_perm
        selected_perm = parse_product(selected)

        result = compose_left_to_right([result, selected_perm])

    return result


# ------------------------------------------------------------
# Simplified Boolean functions from the circuit
# ------------------------------------------------------------

def boolean_outputs(x1, x2, x3):
    f1 = x1 and (x2 or x3)
    f2 = x2 or (x1 and x3)
    f3 = x3 and (x1 or x2)
    f4 = x1 or (x2 and x3)
    f5 = x2 and (x1 or x3)
    f6 = x3 or (x1 and x2)

    return {
        "f1": f1,
        "f2": f2,
        "f3": f3,
        "f4": f4,
        "f5": f5,
        "f6": f6
    }


# ------------------------------------------------------------
# Conditional permutation sequences from the writeup
# ------------------------------------------------------------

sequences = {
    "f1": [
        ("x1", "C", "*"),
        ("x2", "*", "D"),
        ("x3", "*", "C"),
        ("x2", "*", "D'"),
        ("x3", "B", "C'B"),
        ("x1", "C'", "*"),
        ("x2", "*", "C"),
        ("x3", "*", "D"),
        ("x2", "*", "C'"),
        ("x3", "B'", "D'B'")
    ],

    "f2": [
        ("x1", "D", "*"),
        ("x3", "C", "*"),
        ("x1", "D'", "*"),
        ("x3", "C'B", "B"),
        ("x2", "*", "C"),
        ("x1", "C", "*"),
        ("x3", "D", "*"),
        ("x1", "C'", "*"),
        ("x3", "D'B'", "B'"),
        ("x2", "A", "C'A")
    ],

    "f3": [
        ("x3", "C", "*"),
        ("x1", "*", "D"),
        ("x2", "*", "C"),
        ("x1", "*", "D'"),
        ("x2", "B", "C'B"),
        ("x3", "C'", "*"),
        ("x1", "*", "C"),
        ("x2", "*", "D"),
        ("x1", "*", "C'"),
        ("x2", "B'", "D'B'")
    ],

    "f4": [
        ("x2", "D", "*"),
        ("x3", "C", "*"),
        ("x2", "D'", "*"),
        ("x3", "C'B", "B"),
        ("x1", "*", "C"),
        ("x2", "C", "*"),
        ("x3", "D", "*"),
        ("x2", "C'", "*"),
        ("x3", "D'B'", "B'"),
        ("x1", "A", "C'A")
    ],

    "f5": [
        ("x2", "C", "*"),
        ("x1", "*", "D"),
        ("x3", "*", "C"),
        ("x1", "*", "D'"),
        ("x3", "B", "C'B"),
        ("x2", "C'", "*"),
        ("x1", "*", "C"),
        ("x3", "*", "D"),
        ("x1", "*", "C'"),
        ("x3", "B'", "D'B'")
    ],

    "f6": [
        ("x1", "D", "*"),
        ("x2", "C", "*"),
        ("x1", "D'", "*"),
        ("x2", "C'B", "B"),
        ("x3", "*", "C"),
        ("x1", "C", "*"),
        ("x2", "D", "*"),
        ("x1", "C'", "*"),
        ("x2", "D'B'", "B'"),
        ("x3", "A", "C'A")
    ]
}


# ------------------------------------------------------------
# Main verification
# ------------------------------------------------------------

print("Checking all conditional permutation sequences...\n")

all_passed = True

for function_name, sequence in sequences.items():
    function_passed = True

    for x1, x2, x3 in product([False, True], repeat=3):
        values = {
            "x1": x1,
            "x2": x2,
            "x3": x3
        }

        actual_perm = evaluate_sequence(sequence, values)
        expected_bool = boolean_outputs(x1, x2, x3)[function_name]
        expected_perm = A if expected_bool else IDENTITY

        if actual_perm != expected_perm:
            function_passed = False
            all_passed = False

            print("Mismatch found!")
            print("Function:", function_name)
            print("Inputs:", values)
            print("Actual permutation:", actual_perm)
            print("Expected permutation:", expected_perm)
            print()

    if function_passed:
        print(function_name, "passed verification.")

print()

if all_passed:
    print("All functions passed verification.")
else:
    print("Some functions failed verification.")