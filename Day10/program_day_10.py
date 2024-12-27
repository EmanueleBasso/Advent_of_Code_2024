import os
import numpy as np


def print_map(map: np.ndarray) -> None:
    print()

    for i in range(len(map)):
        for j in range(len(map[0])):
            print(map[i][j], end="")

        print()

    print()

def nine_pos_already_found(nine_pos_found: list[list[int]], x: int, y: int) -> bool:
    for pos in nine_pos_found:
        if pos[0] == x and pos[1] == y:
            return True

    return False

def find_trails_from_starting_point(map: np.ndarray, x: int, y: int,
                                    map_dimension: int, nine_pos_found: list[list[int]],
                                    counts_distinct_nine: bool = True) -> int:
    symbol_position = map[x][y]

    if symbol_position == "9":
        if counts_distinct_nine:
            if nine_pos_already_found(nine_pos_found, x, y):
                return 0
            else:
                nine_pos_found.append([x, y])
                return 1
        else:
            return 1

    trailheads = 0

    if (
        x - 1 >= 0
        and (int(symbol_position) + 1 == int(map[x - 1][y]))
    ):
        trailheads += find_trails_from_starting_point(map, x - 1, y, map_dimension, nine_pos_found, counts_distinct_nine)

    if (
        x + 1 < map_dimension
        and (int(symbol_position) + 1 == int(map[x + 1][y]))
    ):
        trailheads += find_trails_from_starting_point(map, x + 1, y, map_dimension, nine_pos_found, counts_distinct_nine)

    if (
        y - 1 >= 0
        and (int(symbol_position) + 1 == int(map[x][y - 1]))
    ):
        trailheads += find_trails_from_starting_point(map, x, y - 1, map_dimension, nine_pos_found, counts_distinct_nine)

    if (
        y + 1 < map_dimension
        and (int(symbol_position) + 1 == int(map[x][y + 1]))
    ):
        trailheads += find_trails_from_starting_point(map, x, y + 1, map_dimension, nine_pos_found, counts_distinct_nine)

    return trailheads

def find_total_trailheads(map: np.ndarray, map_dimension: int, counts_distinct_nine: bool = True) -> int:
    trailheads = 0

    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == "0":
                trailheads_found = find_trails_from_starting_point(map, i, j, map_dimension, [], counts_distinct_nine)
                trailheads += trailheads_found
                #print(f"Find {trailheads_found} for position: [{i}, {j}]")

    return trailheads

def part_one(file_name: str) -> int:
    file_path = os.path.join(os.getcwd(), "input", file_name)

    map = None
    map_dimension = -1

    with open(file_path, "r") as file:
        for row in file:
            if map is None:
                map = np.array(list(row.strip()))
            else:
                map = np.vstack([map, list(row.strip())])

    map_dimension = len(map)
    return find_total_trailheads(map, map_dimension)

def part_two(file_name: str) -> int:
    file_path = os.path.join(os.getcwd(), "input", file_name)

    map = None
    map_dimension = -1

    with open(file_path, "r") as file:
        for row in file:
            if map is None:
                map = np.array(list(row.strip()))
            else:
                map = np.vstack([map, list(row.strip())])

    map_dimension = len(map)
    return find_total_trailheads(map, map_dimension, False)

if __name__ == "__main__":
    #res = part_one("input.txt")
    res = part_two("input.txt")

    print("Result: " + str(res))
