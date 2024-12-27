import os
import numpy as np


def evaluate_sequence_xmas(a: str, b: str, c: str, d: str) -> bool:
    sequence = a + b + c + d

    if sequence == "XMAS" or sequence == "SAMX":
        return True
    else:
        return False

def evaluate_sequence_mas(a: str, b: str, c: str) -> bool:
    sequence = a + b + c

    if sequence == "MAS" or sequence == "SAM":
        return True
    else:
        return False

def search_in_matrix_hor(pos_x: int, pos_y: int, matrix: np.ndarray, matrix_highlighted: np.ndarray) -> int:
    # horizontal backward
    if evaluate_sequence_xmas(matrix[pos_x][pos_y],
                         matrix[pos_x][pos_y - 1],
                         matrix[pos_x][pos_y - 2],
                         matrix[pos_x][pos_y - 3]):
        matrix_highlighted[pos_x][pos_y] = True
        matrix_highlighted[pos_x][pos_y - 1] = True
        matrix_highlighted[pos_x][pos_y - 2] = True
        matrix_highlighted[pos_x][pos_y - 3] = True

        return 1
    else:
        return 0

def search_in_matrix_ver(pos_x: int, pos_y: int, matrix: np.ndarray, matrix_highlighted: np.ndarray) -> int:
    # vertical backward
    if evaluate_sequence_xmas(matrix[pos_x][pos_y],
                         matrix[pos_x - 1][pos_y],
                         matrix[pos_x - 2][pos_y],
                         matrix[pos_x - 3][pos_y]):
        matrix_highlighted[pos_x][pos_y] = True
        matrix_highlighted[pos_x - 1][pos_y] = True
        matrix_highlighted[pos_x - 2][pos_y] = True
        matrix_highlighted[pos_x - 3][pos_y] = True

        return 1
    else:
        return 0

def search_in_matrix_diag(pos_x: int, pos_y: int, matrix: np.ndarray, matrix_highlighted: np.ndarray) -> int:
    sequence_found = 0

    # NE backward
    if pos_y + 3 < len(matrix[0]) and evaluate_sequence_xmas(matrix[pos_x][pos_y],
                                                        matrix[pos_x - 1][pos_y + 1],
                                                        matrix[pos_x - 2][pos_y + 2],
                                                        matrix[pos_x - 3][pos_y + 3]):
        matrix_highlighted[pos_x][pos_y] = True
        matrix_highlighted[pos_x - 1][pos_y + 1] = True
        matrix_highlighted[pos_x - 2][pos_y + 2] = True
        matrix_highlighted[pos_x - 3][pos_y + 3] = True

        sequence_found += 1

    # NO backward
    if pos_y - 3 >= 0 and evaluate_sequence_xmas(matrix[pos_x][pos_y],
                                           matrix[pos_x - 1][pos_y - 1],
                                           matrix[pos_x - 2][pos_y - 2],
                                           matrix[pos_x - 3][pos_y - 3]):
        matrix_highlighted[pos_x][pos_y] = True
        matrix_highlighted[pos_x - 1][pos_y - 1] = True
        matrix_highlighted[pos_x - 2][pos_y - 2] = True
        matrix_highlighted[pos_x - 3][pos_y - 3] = True

        sequence_found += 1

    return sequence_found

def search_in_matrix_diag_mas(pos_x: int, pos_y: int, matrix: np.ndarray, matrix_highlighted: np.ndarray) -> int:
    # X-MAS centered
    if (evaluate_sequence_mas(matrix[pos_x - 1][pos_y + 1],
                              matrix[pos_x][pos_y],
                              matrix[pos_x + 1][pos_y - 1])
        and evaluate_sequence_mas(matrix[pos_x - 1][pos_y - 1],
                                  matrix[pos_x][pos_y],
                                  matrix[pos_x + 1][pos_y + 1])):
        matrix_highlighted[pos_x][pos_y] = True
        matrix_highlighted[pos_x - 1][pos_y + 1] = True
        matrix_highlighted[pos_x + 1][pos_y - 1] = True
        matrix_highlighted[pos_x - 1][pos_y - 1] = True
        matrix_highlighted[pos_x + 1][pos_y + 1] = True
        return 1
    else:
        return 0

def print_matrix(matrix: np.ndarray, matrix_highlighted: np.ndarray) -> None:
    print()

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix_highlighted[i][j]:
                print(matrix[i][j], end="")
            else:
                print(".", end="")

        print()

    print()

def part_one(file_name: str) -> int:
    file_path = os.path.join(os.getcwd(), "input", file_name)

    matrix = None

    with open(file_path, "r") as file:
        for row in file:
            if matrix is None:
                matrix = np.array(list(row.strip()))
            else:
                matrix = np.vstack([matrix, list(row.strip())])

    res = 0

    matrix_highlighted = np.full(matrix.shape, False)

    for i in range(len(matrix)):
        for j in range(3, len(matrix[i])):
            res += search_in_matrix_hor(i, j, matrix, matrix_highlighted)

    for i in range(3, len(matrix)):
        for j in range(len(matrix[i])):
            res += search_in_matrix_ver(i, j, matrix, matrix_highlighted)

    for i in range(3, len(matrix)):
        for j in range(len(matrix[i])):
            res += search_in_matrix_diag(i, j, matrix, matrix_highlighted)

    print_matrix(matrix, matrix_highlighted)

    return res

def part_two(file_name: str) -> int:
    file_path = os.path.join(os.getcwd(), "input", file_name)

    matrix = None

    with open(file_path, "r") as file:
        for row in file:
            if matrix is None:
                matrix = np.array(list(row.strip()))
            else:
                matrix = np.vstack([matrix, list(row.strip())])

    res = 0

    matrix_highlighted = np.full(matrix.shape, False)

    for i in range(1, len(matrix) - 1):
        for j in range(1, len(matrix[i]) - 1):
            res += search_in_matrix_diag_mas(i, j, matrix, matrix_highlighted)

    print_matrix(matrix, matrix_highlighted)

    return res

if __name__ == "__main__":
    #res = part_one("input.txt")
    res = part_two("input.txt")

    print("Result: " + str(res))
