import os
import re


def part_one(file_name: str) -> int:
    file_path = os.path.join(os.getcwd(), "input", file_name)

    input_row = ""

    with open(file_path, "r") as file:
        for row in file:
            input_row += row

    res = 0

    mul_list = list(re.finditer("mul\(\d+,\d+\)", input_row))

    for mul in mul_list:
        factors = re.findall("\d+", mul.group())
        res += int(factors[0]) * int(factors[1])

    return res

def find_previous_pos_in_the_list(pos: int, the_list: list[re.Match]) -> int:
    last_pos = -1

    for ele in the_list:
        if ele.span()[0] > pos:
            return last_pos
        else:
            last_pos = ele.span()[0]

    return last_pos

def part_two(file_name: str) -> int:
    file_path = os.path.join(os.getcwd(), "input", file_name)

    input_row = ""

    with open(file_path, "r") as file:
        for row in file:
            input_row += row

    res = 0

    mul_list = list(re.finditer("mul\(\d+,\d+\)", input_row))
    do_list = list(re.finditer("do\(\)", input_row))
    dont_list = list(re.finditer("don\'t\(\)", input_row))

    for mul in mul_list:
        previous_pos_do = find_previous_pos_in_the_list(mul.span()[0], do_list)
        previous_pos_dont = find_previous_pos_in_the_list(mul.span()[0], dont_list)

        if previous_pos_dont == -1 or previous_pos_dont < previous_pos_do:
            factors = re.findall("\d+", mul.group())
            res += int(factors[0]) * int(factors[1])

    return res

if __name__ == "__main__":
    #res = part_one("input.txt")
    res = part_two("input.txt")

    print("Result: " + str(res))
