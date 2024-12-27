import os
import numpy as np
import bisect
from position_visited_with_direction import PositionVisitedWithDirection


def binary_search_with_bisect(the_list: list[PositionVisitedWithDirection], value: PositionVisitedWithDirection) -> int:
    i = bisect.bisect_left(the_list, value)
    if i != len(the_list) and the_list[i] == value:
        return i
    else:
        return -1

def print_map(map: np.ndarray) -> None:
    print()

    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            print(map[i][j], end="")
        print()

    print()

def find_initial_guard_position(map: np.ndarray) -> list[int]:
    guard_symbols = ["^", ">", "v", "<"]

    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i][j] in guard_symbols:
                return [i, j]

def guard_will_be_out_of_map(next_x: int, next_y: int, map_dimension: int) -> bool:
    if (
        next_x < 0
        or next_x >= map_dimension
        or next_y < 0
        or next_y >= map_dimension
    ):
        return True
    else:
        return False

def get_next_symbol(current_symbol: str) -> str:
    if current_symbol == "^":
        return ">"
    elif current_symbol == ">":
        return "v"
    elif current_symbol == "v":
        return "<"
    else:
        return "^"

def apply_patrol_protocol(map: np.ndarray, guard_symbol: str, x: int, y: int,
                          next_x: int, next_y: int) -> list[int]:
    if map[next_x][next_y] == "#" or map[next_x][next_y] == "0":
        map[x][y] = get_next_symbol(guard_symbol)
        return [x, y]
    else:
        map[x][y] = "X"
        map[next_x, next_y] = guard_symbol
        return [next_x, next_y]

def calculate_patrolled_map(map: np.ndarray, initial_x: int, initial_y: int, map_dimension: int) -> np.ndarray:
    x = initial_x
    y = initial_y

    while True:
        guard_symbol = map[x][y]

        if guard_symbol == "^":
            next_x = x - 1
            next_y = y
        elif guard_symbol == ">":
            next_x = x
            next_y = y + 1
        elif guard_symbol == "v":
            next_x = x + 1
            next_y = y
        else:
            next_x = x
            next_y = y - 1

        if guard_will_be_out_of_map(next_x, next_y, map_dimension):
            map[x][y] = "X"
            break

        next_positions = apply_patrol_protocol(map, guard_symbol, x, y, next_x, next_y)

        x = next_positions[0]
        y = next_positions[1]

    return map

def is_position_visited_yet(position_visited_with_direction_list: list[PositionVisitedWithDirection],
                            next_position: PositionVisitedWithDirection) -> bool:
    if binary_search_with_bisect(position_visited_with_direction_list, next_position) < 0:
        return False
    else:
        return True

def is_loop_map(map: np.ndarray, initial_x: int, initial_y: int, map_dimension: int) -> bool:
    x = initial_x
    y = initial_y

    position_visited_with_direction_list = []

    while True:
        guard_symbol = map[x][y]

        bisect.insort(position_visited_with_direction_list, PositionVisitedWithDirection(x, y, guard_symbol))

        if guard_symbol == "^":
            next_x = x - 1
            next_y = y
        elif guard_symbol == ">":
            next_x = x
            next_y = y + 1
        elif guard_symbol == "v":
            next_x = x + 1
            next_y = y
        else:
            next_x = x
            next_y = y - 1

        if guard_will_be_out_of_map(next_x, next_y, map_dimension):
            return False

        next_positions = apply_patrol_protocol(map, guard_symbol, x, y, next_x, next_y)

        x = next_positions[0]
        y = next_positions[1]

        if is_position_visited_yet(position_visited_with_direction_list, PositionVisitedWithDirection(x, y, map[x, y])):
            return True

def count_position_patrolled(map: np.ndarray) -> int:
    pos_patrolled = 0

    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i][j] == "X":
                pos_patrolled += 1

    return pos_patrolled

def create_new_map_with_obstacle(map: np.ndarray, i: int, j: int) -> np.ndarray:
    new_map = map.copy()

    new_map[i][j] = "0"

    return new_map

def part_one(file_name: str) -> int:
    file_path = os.path.join(os.getcwd(), "input", file_name)

    map = None

    with open(file_path, "r") as file:
        for row in file:
            if map is None:
                map = np.array(list(row.strip()))
            else:
                map = np.vstack([map, list(row.strip())])

    map_dimension = len(map)
    initial_guard_position = find_initial_guard_position(map)
    patrolled_map = calculate_patrolled_map(map, initial_guard_position[0], initial_guard_position[1], map_dimension)

    print_map(patrolled_map)

    return count_position_patrolled(patrolled_map)

def part_two(file_name: str) -> int:
    file_path = os.path.join(os.getcwd(), "input", file_name)

    map = None

    with open(file_path, "r") as file:
        for row in file:
            if map is None:
                map = np.array(list(row.strip()))
            else:
                map = np.vstack([map, list(row.strip())])

    map_dimension = len(map)
    initial_guard_position = find_initial_guard_position(map)
    loop_maps = 0

    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i][j] == "#" or (i == initial_guard_position[0] and j == initial_guard_position[1]):
                continue
            else:
                new_map = create_new_map_with_obstacle(map, i, j)
                print(f"Created new map with an obstacle added to the position: [{i}, {j}]")

                if is_loop_map(new_map, initial_guard_position[0], initial_guard_position[1], map_dimension):
                    loop_maps += 1
                    print(f"=================================================================> FOUND LOOP MAP! "
                          f"TOTAL LOOP MAPS: {loop_maps}")

    return loop_maps

if __name__ == "__main__":
    #res = part_one("input.txt")
    res = part_two("input.txt")

    print("Result: " + str(res))
