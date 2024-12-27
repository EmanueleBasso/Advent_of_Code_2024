import os


def check_report(report: list[str]) -> bool:
    incresing = None
    if int(report[0]) > int(report[1]):
        incresing = False
    elif int(report[0]) < int(report[1]):
        incresing = True
    else:
        return False

    for i in range(len(report) - 1):
        if incresing:
            if int(report[i]) > int(report[i + 1]):
                return False
        else:
            if int(report[i]) < int(report[i + 1]):
                return False

        if abs(int(report[i]) - int(report[i + 1])) < 1 or abs(int(report[i]) - int(report[i + 1])) > 3:
            return False

    return True

def part_one(file_name: str) -> int:
    file_path = os.path.join(os.getcwd(), "input", file_name)

    safe_reports = 0

    with open(file_path, "r") as file:
        for row in file:
            report = row.split(" ")

            if check_report(report):
                safe_reports += 1

    return safe_reports

def part_two(file_name: str) -> int:
    file_path = os.path.join(os.getcwd(), "input", file_name)

    safe_reports = 0

    with (open(file_path, "r") as file):
        for row in file:
            report = row.split(" ")

            if check_report(report):
                safe_reports += 1
            else:
                for i in range(len(report)):
                    small_report = report.copy()
                    small_report.pop(i)

                    if check_report(small_report):
                        safe_reports += 1
                        break

    return safe_reports

if __name__ == "__main__":
    #res = part_one("input.txt")
    res = part_two("input.txt")

    print("Result: " + str(res))
