import os
from equation import Equation


def eval_single_equation_with_two_operators(equation: Equation, pos: int, equation_built: str) -> bool:
    if pos == (len(equation.operators) - 1):
        equation_to_eval = "(" + equation_built + ") == " + equation.test_value

        if eval(equation_to_eval):
            print("Valid equation found ===> " + equation_to_eval)
            return True
        else:
            return False

    if eval_single_equation_with_two_operators(equation,
                                               pos + 1,
                                               "(" + equation_built + " + " + equation.operators[pos + 1] + ")"):
        return True
    else:
        return eval_single_equation_with_two_operators(equation,
                                                       pos + 1,
                                                       "(" + equation_built + " * " + equation.operators[pos + 1] + ")")

def eval_single_equation_with_three_operators(equation: Equation, pos: int, equation_built: str) -> bool:
    if pos == (len(equation.operators) - 1):
        equation_to_eval = "int(" + equation_built + ") == " + equation.test_value

        if eval(equation_to_eval):
            print("Valid equation found ===> " + equation_to_eval)
            return True
        else:
            return False

    if eval_single_equation_with_three_operators(equation,
                                                pos + 1,
                                                "int(" + equation_built + ") + int(" + equation.operators[pos + 1] + ")"):
        return True
    elif eval_single_equation_with_three_operators(equation,
                                                   pos + 1,
                                                   "int(" + equation_built + ") * int(" + equation.operators[pos + 1] + ")"):
        return True
    else:
        return eval_single_equation_with_three_operators(equation,
                                                         pos + 1,
                                                         "str(" + equation_built + ") + str(" + equation.operators[pos + 1] + ")")

def is_valid_equation(equation: Equation, num_operators: int) -> bool:
    if num_operators == 2:
        return eval_single_equation_with_two_operators(equation, 0, equation.operators[0])
    else:
        return eval_single_equation_with_three_operators(equation, 0, equation.operators[0])

def part_one(file_name: str) -> int:
    file_path = os.path.join(os.getcwd(), "input", file_name)

    equations = []

    with open(file_path, "r") as file:
        for row in file:
            splitted_row = row.split(":")

            equations.append(Equation(
                splitted_row[0],
                splitted_row[1].strip().split(" ")))

    res = 0

    for i in range(len(equations)):
        print("Line under examination: " + str(i))

        if is_valid_equation(equations[i], 2):
            res += int(equations[i].test_value)

    return res

def part_two(file_name: str) -> int:
    file_path = os.path.join(os.getcwd(), "input", file_name)

    equations = []

    with open(file_path, "r") as file:
        for row in file:
            splitted_row = row.split(":")

            equations.append(Equation(
                splitted_row[0],
                splitted_row[1].strip().split(" ")))

    res = 0

    for i in range(len(equations)):
        print("Line under examination: " + str(i))

        if is_valid_equation(equations[i], 3):
            res += int(equations[i].test_value)

    return res

if __name__ == "__main__":
    #res = part_one("input.txt")
    res = part_two("input.txt")

    print("Result: " + str(res))
