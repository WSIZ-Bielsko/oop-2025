import os


def process_file(file_name: str, marker: str = 'def') -> list[str] | None:
    if not os.path.exists(file_name):
        return None

    with open(file_name, "r") as f:
        lines = f.readlines()

    for l in lines:
        if l.startswith(marker):
            print(l)

    return lines


if __name__ == '__main__':
    w = process_file('a.txt')
