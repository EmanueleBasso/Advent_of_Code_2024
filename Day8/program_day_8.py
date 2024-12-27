import os


def print_antenna_positions(antennas_positions: dict[str, list[list[int]]],
                            antennas_positions_antinodes: dict[str, list[list[int]]] = None) -> None:
    for antenna in antennas_positions:
        print("Antenna symbol: " + antenna)

        print("\tPositions: ", end="")
        first_position = True
        for position in antennas_positions[antenna]:
            if first_position:
                print("[" + str(position[0]) + ", " + str(position[1]) + "]", end="")
                first_position = False
            else:
                pass
                print(", [" + str(position[0]) + ", " + str(position[1]) + "]", end="")

        if antennas_positions_antinodes is not None:
            print("\n\tAntinodes positions: ", end="")
            first_position = True
            for position in antennas_positions_antinodes[antenna]:
                if first_position:
                    print("[" + str(position[0]) + ", " + str(position[1]) + "]", end="")
                    first_position = False
                else:
                    pass
                    print(", [" + str(position[0]) + ", " + str(position[1]) + "]", end="")

        print()

    print()

def print_map(antennas_positions: dict[str, list[list[int]]], map_dimension: int,
              antennas_positions_antinodes: dict[str, list[list[int]]] = None) -> None:
    print()

    for i in range(map_dimension):
        for j in range(map_dimension):
            found_antenna = False
            found_antinode = False

            for antenna in antennas_positions:
                for position in antennas_positions[antenna]:
                    if i == position[0] and j == position[1]:
                        print(antenna, end="")
                        found_antenna = True
                        break

                if found_antenna:
                    break

            if antennas_positions_antinodes is not None and not found_antenna:
                for antenna in antennas_positions_antinodes:
                    for position in antennas_positions_antinodes[antenna]:
                        if i == position[0] and j == position[1]:
                            print("#", end="")
                            found_antinode = True
                            break

                    if found_antinode:
                        break

            if not found_antenna and not found_antinode:
                print(".", end="")

        print()

    print()

def calculate_antenna_antinodes(postions: list[list[int]], map_dimension: int) -> list[list[int]]:
    antenna_antinodes = []

    for i in range(len(postions)):
        for j in range(i + 1, len(postions)):
            distance_x = abs(postions[i][0] - postions[j][0])
            distance_y = abs(postions[i][1] - postions[j][1])

            pos_x_first_antinode = -1
            pos_y_first_antinode = -1
            pos_x_second_antinode = -1
            pos_y_second_antinode = -1

            # Horizontal
            if postions[i][0] < postions[j][0]:
                pos_x_first_antinode = postions[i][0] - distance_x
                pos_x_second_antinode = postions[j][0] + distance_x
            else:
                pos_x_first_antinode = postions[i][0] + distance_x
                pos_x_second_antinode = postions[j][0] - distance_x

            # Vertical
            if postions[i][1] < postions[j][1]:
                pos_y_first_antinode = postions[i][1] - distance_y
                pos_y_second_antinode = postions[j][1] + distance_y
            else:
                pos_y_first_antinode = postions[i][1] + distance_y
                pos_y_second_antinode = postions[j][1] - distance_y

            if (
                    0 <= pos_x_first_antinode < map_dimension
                    and 0 <= pos_y_first_antinode < map_dimension
            ):
                antenna_antinodes.append([pos_x_first_antinode, pos_y_first_antinode])

            if (
                    0 <= pos_x_second_antinode < map_dimension
                    and 0 <= pos_y_second_antinode < map_dimension
            ):
                antenna_antinodes.append([pos_x_second_antinode, pos_y_second_antinode])

    return antenna_antinodes

def calculate_antenna_antinodes_with_resonant_harmonics(postions: list[list[int]],
                                                        map_dimension: int) -> list[list[int]]:
    antenna_antinodes = []

    for i in range(len(postions)):
        for j in range(i + 1, len(postions)):
            distance_x = abs(postions[i][0] - postions[j][0])
            distance_y = abs(postions[i][1] - postions[j][1])

            multiplier = 1
            while True:
                no_more_antinodes = True

                pos_x_first_antinode = -1
                pos_y_first_antinode = -1
                pos_x_second_antinode = -1
                pos_y_second_antinode = -1

                # Horizontal
                if postions[i][0] < postions[j][0]:
                    pos_x_first_antinode = postions[i][0] - distance_x * multiplier
                    pos_x_second_antinode = postions[j][0] + distance_x * multiplier
                else:
                    pos_x_first_antinode = postions[i][0] + distance_x * multiplier
                    pos_x_second_antinode = postions[j][0] - distance_x * multiplier

                # Vertical
                if postions[i][1] < postions[j][1]:
                    pos_y_first_antinode = postions[i][1] - distance_y * multiplier
                    pos_y_second_antinode = postions[j][1] + distance_y * multiplier
                else:
                    pos_y_first_antinode = postions[i][1] + distance_y * multiplier
                    pos_y_second_antinode = postions[j][1] - distance_y * multiplier

                if (
                        0 <= pos_x_first_antinode < map_dimension
                        and 0 <= pos_y_first_antinode < map_dimension
                ):
                    antenna_antinodes.append([pos_x_first_antinode, pos_y_first_antinode])
                    no_more_antinodes = False

                if (
                        0 <= pos_x_second_antinode < map_dimension
                        and 0 <= pos_y_second_antinode < map_dimension
                ):
                    antenna_antinodes.append([pos_x_second_antinode, pos_y_second_antinode])
                    no_more_antinodes = False

                if no_more_antinodes:
                    break

                multiplier += 1

    return antenna_antinodes

def calculate_total_antinodes(antennas_positions: dict[str, list[list[int]]],
                              map_dimension: int, with_resonant_harmonics: bool = False) -> dict[str, list[list[int]]]:
    antennas_positions_antinodes = {}

    for antenna in antennas_positions:
        if not with_resonant_harmonics:
            antennas_positions_antinodes[antenna] = calculate_antenna_antinodes(antennas_positions[antenna],
                                                                                map_dimension)
        else:
            antenna_antinodes_with_resonant_harmonics = calculate_antenna_antinodes_with_resonant_harmonics(
                antennas_positions[antenna], map_dimension)
            antenna_antinodes_with_resonant_harmonics.extend(antennas_positions[antenna])

            antennas_positions_antinodes[antenna] = antenna_antinodes_with_resonant_harmonics

    return antennas_positions_antinodes

def calculate_distinct_antinodes(antennas_positions_antinodes: dict[str, list[list[int]]]) -> int:
    distinct_antinodes = []

    for antenna in antennas_positions_antinodes:
        for antinode_position in antennas_positions_antinodes[antenna]:
            antinode_already_inserted = False

            for antinode_position_already_inserted in distinct_antinodes:
                if (
                    antinode_position[0] == antinode_position_already_inserted[0] and
                    antinode_position[1] == antinode_position_already_inserted[1]
                ):
                    antinode_already_inserted = True
                    break

            if not antinode_already_inserted:
                distinct_antinodes.append(antinode_position)

    return len(distinct_antinodes)

def part_one(file_name: str) -> int:
    file_path = os.path.join(os.getcwd(), "input", file_name)

    map_dimension = -1
    antennas_positions = {}

    with open(file_path, "r") as file:
        lines = file.readlines()

        map_dimension = len(lines)
        for i in range(len(lines)):
            line = list(lines[i].strip())

            for j in range(len(line)):
                antenna_symbol = line[j]

                if antenna_symbol == ".":
                    continue

                if antenna_symbol in antennas_positions:
                    antenna_positions = antennas_positions[antenna_symbol]
                    antenna_positions.append([i, j])
                    antennas_positions[antenna_symbol] = antenna_positions
                else:
                    antennas_positions[antenna_symbol] = [[i, j]]

    antennas_positions_antinodes = calculate_total_antinodes(antennas_positions, map_dimension)

    #print_antenna_positions(antennas_positions)
    #print_antenna_positions(antennas_positions, antennas_positions_antinodes)
    #print_map(antennas_positions, map_dimension, antennas_positions_antinodes)

    return calculate_distinct_antinodes(antennas_positions_antinodes)

def part_two(file_name: str) -> int:
    file_path = os.path.join(os.getcwd(), "input", file_name)

    map_dimension = -1
    antennas_positions = {}

    with open(file_path, "r") as file:
        lines = file.readlines()

        map_dimension = len(lines)
        for i in range(len(lines)):
            line = list(lines[i].strip())

            for j in range(len(line)):
                antenna_symbol = line[j]

                if antenna_symbol == ".":
                    continue

                if antenna_symbol in antennas_positions:
                    antenna_positions = antennas_positions[antenna_symbol]
                    antenna_positions.append([i, j])
                    antennas_positions[antenna_symbol] = antenna_positions
                else:
                    antennas_positions[antenna_symbol] = [[i, j]]

    antennas_positions_antinodes = calculate_total_antinodes(antennas_positions, map_dimension, with_resonant_harmonics=True)

    #print_antenna_positions(antennas_positions)
    #print_antenna_positions(antennas_positions, antennas_positions_antinodes)
    #print_map(antennas_positions, map_dimension, antennas_positions_antinodes)

    return calculate_distinct_antinodes(antennas_positions_antinodes)

if __name__ == "__main__":
    #res = part_one("input.txt")
    res = part_two("input.txt")

    print("Result: " + str(res))
