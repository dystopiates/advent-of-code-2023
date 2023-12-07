import re

r1 = re.compile(r'(\d)')
r2 = re.compile(r'(\d|zero|one|two|three|four|five|six|seven|eight|nine)')
r2r = re.compile(r'(\d|' + 'zero|one|two|three|four|five|six|seven|eight|nine'[::-1] + ')')
mapping = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}
for i in range(10):
    mapping[str(i)] = i

def get_nums(line: str) -> int:
    digits = list(map(int, r1.findall(line)))

    return 10 * digits[0] + digits[-1]


def get_num_pt2(line: str) -> int:
    digits = r2.findall(line)
    backdigits = r2r.findall(line[::-1])

    return 10 * mapping[digits[0]] + mapping[backdigits[0][::-1]]


def main(input: str):
    print(sum(map(get_nums, input.splitlines())))


def main_pt2(input: str):
    input = input.strip().splitlines()

    print(sum(map(get_num_pt2, input)))


if __name__ == '__main__':
    with open('day1.input', 'r') as inf:
        main_pt2(inf.read().strip().lower())
