import os
import re
import bisect
from knowledge_base import KnowledgeBase


def binary_search_with_bisect(the_list: list[KnowledgeBase], value: KnowledgeBase) -> int:
    i = bisect.bisect_left(the_list, value)
    if i != len(the_list) and the_list[i] == value:
        return i
    else:
        return -1

def print_stones(stones: list[str]) -> None:
    for stone in stones:
        print(stone, end=" ")

    print()

def blink(stone: str, how_many_times: int) -> list[str]:
    stones_expanded = [stone]

    #print("Stone: " + stone)
    for i in range(how_many_times):
        #print("\tBlink iteration: " + str(i + 1) + ", Current number of stones: " + str(len(stones_expanded)))

        i = 0
        while i < len(stones_expanded):
            stone_i = stones_expanded[i]

            if stone_i == "0":
                stones_expanded[i] = "1"
                i += 1
            elif len(stone_i) % 2 == 0:
                stone_half_len = int(len(stone_i) / 2)

                stones_expanded[i] = stone_i[: - stone_half_len]

                right_stone = re.sub(r"^0+", "", stone_i[stone_half_len :])
                if right_stone == "":
                    right_stone = "0"

                stones_expanded.insert(i + 1, right_stone)
                i += 2
            else:
                stones_expanded[i] = str(int(stone_i) * 2024)
                i += 1

    return stones_expanded

def expand_stones(stones: list[str], how_many_times: int) -> int:
    kb = []
    stones_size = 0

    for stone in stones:
        iteration = 0

        stone_expanded = [stone]
        while iteration < how_many_times:
            print("Stone: " + stone)
            print("Iteration step: " + str(iteration))
            print("KB size: " + str(len(kb)))
            print()

            next_iteration_stone_expanded = []

            stone_expanded_len = len(stone_expanded)
            for i in range(stone_expanded_len):
                stone_i = stone_expanded[i]

                stone_found_in_kb = binary_search_with_bisect(kb, KnowledgeBase(int(stone_i), []))

                stone_expanded_tmp = []
                if (
                        len(kb) == 0
                        or stone_found_in_kb < 0
                ):
                    stone_expanded_tmp = blink(stone_i, 25)
                    # print_stones(stones_expanded)
                    bisect.insort(kb, KnowledgeBase(int(stone_i), stone_expanded_tmp))
                else:
                    stone_expanded_tmp = kb[stone_found_in_kb].expansion_after_twentyfive_blinks

                if iteration + 25 == how_many_times:
                    stones_size += len(stone_expanded_tmp)
                else:
                    next_iteration_stone_expanded.extend(stone_expanded_tmp)

            stone_expanded.clear()
            stone_expanded = next_iteration_stone_expanded.copy()

            iteration += 25

        stone_expanded.clear()

    return stones_size

def execute(file_name: str, how_many_times: int) -> int:
    file_path = os.path.join(os.getcwd(), "input", file_name)

    stones = []

    with open(file_path, "r") as file:
        stones = file.readline().split(" ")

    return expand_stones(stones, how_many_times)

if __name__ == "__main__":
    #res = execute("input.txt", 25)
    res = execute("input.txt", 75)

    print("Result: " + str(res))
