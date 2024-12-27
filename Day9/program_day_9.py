import os
import bisect


def binary_search_with_bisect(the_list: list[int], value: int) -> int:
    i = bisect.bisect_left(the_list, value)
    if i != len(the_list) and the_list[i] == value:
        return i
    else:
        return -1

def print_disk_map(disk_map: list[str]) -> None:
    for ele in disk_map:
        print(ele, end="")

    print()

def expand_disk_map(disk_map: list[str]) -> list[str]:
    disk_map_expanded = []
    id_number = 0

    even = True

    for ele in disk_map:
        if even:
            for num_block_file in range(int(ele)):
                disk_map_expanded.append(id_number)

            id_number += 1
            even = False
        else:
            for num_block_file in range(int(ele)):
                disk_map_expanded.append(".")

            even = True

    return disk_map_expanded

def compact_disk_map(disk_map: list[str]) -> list[str]:
    disk_map_compacted = disk_map.copy()

    last_pos_inserted = 0

    for i in range(len(disk_map_compacted) -1 , 0, -1):
        compacted = False

        for j in range(last_pos_inserted, i):
            if disk_map_compacted[j] == ".":
                disk_map_compacted[j] = disk_map_compacted[i]
                disk_map_compacted[i] = "."
                last_pos_inserted = j
                compacted = True
                break

        if not compacted:
            break

    return disk_map_compacted

def compact_disk_map_without_fragmentation(disk_map: list[str]) -> list[str]:
    disk_map_compacted = disk_map.copy()
    file_id_number_compacted = []

    start_pos_file = len(disk_map_compacted) - 1
    free_space_remained = True

    while free_space_remained:

        while start_pos_file >= 0:
            if (
                    disk_map_compacted[start_pos_file] == "." or
                    binary_search_with_bisect(file_id_number_compacted, int(disk_map_compacted[start_pos_file])) != -1
            ):
                start_pos_file -= 1
            else:
                break

        id_number = disk_map_compacted[start_pos_file]
        file_size = 1
        end_pos_file = start_pos_file
        start_pos_file -= 1

        while start_pos_file >= 0:
            if disk_map_compacted[start_pos_file] == id_number:
                start_pos_file -= 1
                file_size += 1
            else:
                break

        free_space_size = 0
        start_pos_free_space = -1
        end_pos_free_space = -1

        i = 0
        free_space_remained = False
        while i < start_pos_file + 1:
            if disk_map_compacted[i] == ".":
                if free_space_size == 0:
                    start_pos_free_space = i
                    end_pos_free_space = start_pos_free_space
                else:
                    end_pos_free_space = i

                free_space_size += 1
                free_space_remained = True
            else:
                free_space_size = 0
                start_pos_free_space = -1
                end_pos_free_space = -1

            if free_space_size == file_size:
                for j in range(start_pos_free_space, end_pos_free_space + 1):
                    disk_map_compacted[j] = id_number

                for j in range(start_pos_file + 1, end_pos_file + 1):
                    disk_map_compacted[j] = "."

                bisect.insort(file_id_number_compacted, int(id_number))

                break

            i += 1

    return disk_map_compacted

def calculate_check_sum(disk_map: list[str]) -> int:
    checksum = 0

    for i in range(len(disk_map)):
        if disk_map[i] == ".":
            break

        checksum += int(disk_map[i]) * i

    return checksum

def calculate_check_sum_without_fragmentation(disk_map: list[str]) -> int:
    checksum = 0

    for i in range(len(disk_map)):
        if disk_map[i] != ".":
            checksum += int(disk_map[i]) * i

    return checksum

def part_one(file_name: str) -> int:
    file_path = os.path.join(os.getcwd(), "input", file_name)

    disk_map = []

    with open(file_path, "r") as file:
        line = file.readline()

        disk_map = list(line)

    disk_map_expanded = expand_disk_map(disk_map)
    disk_map_compacted = compact_disk_map(disk_map_expanded)

    #print_disk_map(disk_map_compacted)

    return calculate_check_sum(disk_map_compacted)

def part_two(file_name: str) -> int:
    file_path = os.path.join(os.getcwd(), "input", file_name)

    disk_map = []

    with open(file_path, "r") as file:
        line = file.readline()

        disk_map = list(line)

    disk_map_expanded = expand_disk_map(disk_map)
    disk_map_compacted = compact_disk_map_without_fragmentation(disk_map_expanded)

    #print_disk_map(disk_map_compacted)

    return calculate_check_sum_without_fragmentation(disk_map_compacted)

if __name__ == "__main__":
    #res = part_one("input.txt")
    res = part_two("input.txt")

    print("Result: " + str(res))
