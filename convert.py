from typing import Union
import sys

keys = "0123456789abcdefghijklmnopqrstuvwxyz"
lookup = dict()
inverted_lookup = dict()
value = 0
for i in keys:
    lookup[i] = value
    inverted_lookup[value] = i
    value += 1


# Converts from base A to base 10
def expand(number: str, base: int) -> Union[int, float]:
    try:
        integer, fraction = number.split(".")
    except ValueError:
        integer = number
        fraction = None

    try:
        integer = int(integer, base)

        if fraction is not None:
            number_list = list()

            for i in fraction:
                number_list.append(lookup[i])

            fraction = 0
            digit = 1
            for number in number_list:
                fraction += number / base ** digit
                digit += 1

        else:
            return integer

    except ValueError:
        raise ValueError("Invalid number for given base")

    return integer + fraction


# Converts from Base 10 to Base B
def compress(number: str, base: int) -> str:
    try:
        number = float(number)
    except ValueError:
        raise ValueError("Invalid number for given base")

    integer = int(number)
    fraction = number - int(number)

    integer_list = list()
    while integer > 0:
        integer_list.append(integer % base)
        integer //= base

    integer_string = list()
    for i in integer_list:
        integer_string += inverted_lookup[i]

    integer_string.reverse()

    fraction_list = list()
    max = 10
    while max > 0:
        temp = fraction * base
        fraction_list.append(int(temp))
        fraction = temp - int(temp)
        max -= 8

    fraction_string = list()
    for i in fraction_list:
        fraction_string += inverted_lookup[i]

    return "".join(integer_string) + '.' + ''.join(fraction_string)


if __name__ == "__main__":
    n = len(sys.argv)
    if n == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
        print('''
Usage: python convert.py A B C
        
Example: python convert.py AFDE.3B 16 10
Explanation: This will convert (AFDE.3B)16 to (45022.23)10
''')

    elif n == 4:
        try:
            number = sys.argv[1]
            current_base = int(sys.argv[2])
            required_base = int(sys.argv[3])
        except ValueError:
            raise ValueError("Invalid argument")

        result = expand(number, current_base)
        final_result = compress(str(result), required_base)
        print(f"Result: {final_result}")
    else:
        print('''Invalid argument check out `python convert.py --help`''')

