def fill_zero_left(number):
    binary_number = bin(int(number))
    return '%016d' % int(binary_number[2:])