import os
import bisect


def part_one(file_name: str) -> int:
    file_path = os.path.join(os.getcwd(), "input", file_name)

    first_list = []
    second_list = []

    with open(file_path, "r") as file:
        for row in file:
            data_row = row.split("   ")

            bisect.insort(first_list, int(data_row[0]))
            bisect.insort(second_list, int(data_row[1]))

    res = 0

    for i in range(len(first_list)):
        res += abs(first_list[i] - second_list[i])

    return res

def part_two(file_name: str) -> int:
    file_path = os.path.join(os.getcwd(), "input", file_name)

    first_list = []
    second_list = []

    with open(file_path, "r") as file:
        for row in file:
            data_row = row.split("   ")

            bisect.insort(first_list, int(data_row[0]))
            bisect.insort(second_list, int(data_row[1]))

    res = 0

    for i in range(len(first_list)):
        res += first_list[i] * second_list.count(first_list[i])

    return res

if __name__ == "__main__":
    #res = part_one("input.txt")
    res = part_two("input.txt")

    print("Result: " + str(res))
