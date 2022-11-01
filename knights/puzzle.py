from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(

    # A is a knight or a knave but not both:
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),

    # A is Knight --> true
    Implication(AKnight, And(AKnight, AKnave)),

    # A is knave --> false
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(

    # A is a knight or a knave but not both:
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),

    # B is a knight or a knave but not both:
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    # A is Knight --> true "We are both knaves."
    Implication(AKnight, And(AKnave, BKnave)),

    # A is knave --> false  "We are NOT both knaves."
    Implication(AKnave, Not(And(AKnave, BKnave)))

)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(

    # A is a knight or a knave but not both:
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),

    # B is a knight or a knave but not both:
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    # A is Knight --> true "We are the same kind."
    Implication(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),

    # A is knave --> false "We are NOT the same kind."
    Implication(AKnave, Or(And(AKnave, BKnight), And(AKnight, BKnave))),

    # B is Knight --> true "We are of different kinds."
    Implication(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave))),

    # B is knave --> false  "We are of NOT different kinds."
    Implication(BKnave, Or(And(AKnave, BKnave), And(AKnight, BKnight)))

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(

    # A is a knight or a knave but not both:
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),

    # B is a knight or a knave but not both:
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    # C is a knight or a knave but not both:
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),

    # B is Knight --> true (1) "C is a knave."
    Implication(BKnight,CKnave),

    # (2) "A said 'I am a knave'." What A said might be true or false based on his role
    Implication(BKnight, And(Implication(AKnight, AKnave), Implication(AKnave, AKnight))),

    # B is Knave --> false (2) "C is NOT a knave."
    Implication(BKnave, CKnight),

    # (2) "A said 'I am NOT a knave'." What A said might be true or false based on his role
    Implication(BKnave, And(Implication(AKnight, AKnight), Implication(AKnave, AKnave))),

    # C is Knight --> true "A is a knight."
    Implication(CKnight,AKnight),

    # C is Knave --> false "A is NOT a knight."
    Implication(CKnave,AKnave),

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
