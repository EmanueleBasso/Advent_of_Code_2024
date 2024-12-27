import os
import bisect


ordering_rules = {}
updates = []

def binary_search_with_bisect(the_list: list[int], value: int) -> int:
    i = bisect.bisect_left(the_list, value)
    if i != len(the_list) and the_list[i] == value:
        return i
    else:
        return -1

def are_two_pages_ordered(first_page: int, second_page: int) -> bool:
    if second_page not in ordering_rules:
        return True

    if binary_search_with_bisect(ordering_rules[second_page], first_page) < 0:
        return True
    else:
        return False

def order_update(update: list[int]) -> list[int]:
    update_ordered = update.copy()

    i = 0
    while i < len(update_ordered):
        reorder = False

        for j in range(i + 1, len(update_ordered)):
            if not are_two_pages_ordered(update_ordered[i], update_ordered[j]):
                ele = update_ordered.pop(j)
                update_ordered.insert(i, ele)
                reorder = True
                break

        if not reorder:
            i += 1

    return update_ordered

def part_one(file_name: str) -> int:
    file_path = os.path.join(os.getcwd(), "input", file_name)

    new_section = False
    with open(file_path, "r") as file:
        for row in file:
            if row == "\n":
                new_section = True
                continue

            if not new_section:
                numbers = row.strip().split("|")
                left_number = int(numbers[0])
                right_number = int(numbers[1])

                if left_number not in ordering_rules:
                    ordering_rules[left_number] = [right_number]
                else:
                    left_number_list = ordering_rules[left_number]
                    bisect.insort(left_number_list, right_number)
            else:
                updates.append([int(ele) for ele in list(row.strip().split(","))])

    res = 0

    for update in updates:
        valid_update = True

        for i in range(len(update)):
            for j in range(i + 1, len(update)):
                if not are_two_pages_ordered(update[i], update[j]):
                    valid_update = False
                    break

            if not valid_update:
                break

        if valid_update:
            res += update[(len(update) // 2)]

    return res

def part_two(file_name: str) -> int:
    file_path = os.path.join(os.getcwd(), "input", file_name)

    new_section = False
    with open(file_path, "r") as file:
        for row in file:
            if row == "\n":
                new_section = True
                continue

            if not new_section:
                numbers = row.strip().split("|")
                left_number = int(numbers[0])
                right_number = int(numbers[1])

                if left_number not in ordering_rules:
                    ordering_rules[left_number] = [right_number]
                else:
                    left_number_list = ordering_rules[left_number]
                    bisect.insort(left_number_list, right_number)
            else:
                updates.append([int(ele) for ele in list(row.strip().split(","))])

    res = 0

    for update in updates:
        valid_update = True

        for i in range(len(update)):
            for j in range(i + 1, len(update)):
                if not are_two_pages_ordered(update[i], update[j]):
                    valid_update = False
                    break

            if not valid_update:
                break

        if not valid_update:
            update_ordered = order_update(update)
            res += update_ordered[(len(update_ordered) // 2)]

    return res

if __name__ == "__main__":
    #res = part_one("input.txt")
    res = part_two("input.txt")

    print("Result: " + str(res))
