import sys


file = sys.argv[1]


with open(file, "r") as f:
    code = f.read()


print(code)

