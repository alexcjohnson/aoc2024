import math
import os
import sys
import time as _time

_dir = os.getcwd()
TEMPLATE = """# Day {i}, Advent of Code 2024
# Run for testing with: python day{i:02d}.py t
# If there are multiple test files like day{i:02d}test3.txt: python day{i:02d}.py t 3
# Run with real input: python day{i:02d}.py

from utils import load, time

lines, testing = load()


time()  # finalize and print all timing.
"""
TIMES = []


def load():
    TIMES.append(("", _time.time()))
    fn = next(s for s in sys.argv if s.endswith(".py"))
    testing = "t" in sys.argv

    try:
        num = str(int(sys.argv[-1]))
    except ValueError:
        num = ""

    base = fn.split("/")[-1].split(".")[0]
    fn = f"{base}{"test" if testing else "input"}{num}.txt"
    path = os.path.join(_dir, fn)
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    return lines, testing


def time(label=None, display=False):
    TIMES.append((label or "Done", _time.time()))

    if not label:
        t0 = TIMES[0][1]
        last_time = t0
        label_len = max(len(entry[0]) for entry in TIMES[1:])
        first_digit = 1 + max(0, math.floor(math.log10(TIMES[-1][1] - TIMES[0][1])))
        decimal_digits = max(0, 5 - first_digit)
        total_digits = first_digit + decimal_digits + 1
        num_spec = f"{total_digits}.{decimal_digits}f"
        print(num_spec)
        for labeli, ti in TIMES[1:]:
            interval = ti - last_time
            total = ti - t0
            print(
                f"{labeli:{label_len}} {interval:{num_spec}}  sec, "
                f"{total:{num_spec}} total"
            )
    elif display:
        interval = TIMES[-1][1] - TIMES[-2][1]
        total = TIMES[-1][1] - TIMES[0][1]
        print(f"{label} {interval:.3f} sec, {total:.3f} total")


def create(overwrite=False, start_day=1):
    for i in range(start_day, 26):
        for variant in ("input", "test"):
            fn = f"day{i:02d}{variant}.txt"
            path = os.path.join(_dir, fn)
            if overwrite or not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    f.write("\n")
        path = os.path.join(_dir, f"day{i:02d}.py")
        if overwrite or not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(TEMPLATE.format(i=i))
        if i < 10:
            for ext in ("input.txt", "test.txt", ".py"):
                path = os.path.join(_dir, f"day{i}{ext}")
                if os.path.exists(path):
                    os.remove(path)


if __name__ == "__main__":
    _overwrite = "overwrite" in sys.argv
    _create = "create" in sys.argv
    if _create or _overwrite:
        try:
            _start_day = int(sys.argv[-1])
            create(_overwrite, _start_day)
        except ValueError:
            create(_overwrite)
