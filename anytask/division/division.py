def long_division(dividend, divider):
    number = dividend
    lines = str(dividend) + "|" + str(divider) + '\n'
    digits = []
    while dividend > 0:
        digits.append(dividend % 10)
        dividend //= 10
    dividend = digits[::-1]
    answer = []
    remainder = 0
    is_first_step = True
    step_counter = 0
    line_counter = 1
    last_step_place = 0
    if number < divider:
        lines += str(number) + '|' + str(number // divider) + '\n'
    else:
        for current_number in dividend:
            step_counter += 1
            current_number += remainder * 10
            whole = current_number // divider
            if whole:
                last_step_place = step_counter
                line_counter += 1
                subtract_number = whole * divider
                remainder = current_number % divider
                answer.append(whole)
                is_first_step = False
                if line_counter == 2:
                    lines += str(subtract_number) \
                             + (len(dividend) - len(str(current_number))) \
                             * ' ' + '|*' + '\n'
                    continue
                lines += (step_counter - len(str(current_number))) * ' ' \
                    + str(current_number) + '\n'
                lines += (step_counter - len(str(subtract_number))) * ' ' \
                    + str(subtract_number) + '\n'
            else:
                if not is_first_step:
                    answer.append(0)
                remainder = current_number
        if remainder == 0:
            lines += (last_step_place - len(str(remainder))) * ' ' \
                     + str(remainder)
        else:
            lines += (step_counter - len(str(remainder))) * ' ' \
                     + str(remainder)

    str_answer = ''
    for i in answer:
        str_answer += str(i)
    lines = lines.replace('*', str_answer)
    return lines


def main():
    print(long_division(123, 123))
    print()
    print(long_division(1, 1))
    print()
    print(long_division(15, 3))
    print()
    print(long_division(3, 15))
    print()
    print(long_division(12345, 25))
    print()
    print(long_division(1234, 1423))
    print()
    print(long_division(87654532, 1))
    print()
    print(long_division(24600, 123))
    print()
    print(long_division(4567, 1234567))
    print()
    print(long_division(246001, 123))
    print()
    print(long_division(100000, 50))
    print()
    print(long_division(123456789, 531))
    print()
    print(long_division(425934261694251, 12345678))


if __name__ == '__main__':
    main()
