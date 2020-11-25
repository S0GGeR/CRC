import random
from matplotlib import pyplot as plt
import numpy as np


# def check():
#     a_x = 2 ** 7 + 2 ** 5 + 2 ** 4 + 2 ** 3 + 2 ** 1 + 2 ** 0
#     g_x = 2 ** 4 + 2 ** 3 + 2 ** 2 + 2 ** 0
#     for j in range(0, 8):
#         randint = 2 ** 7 + 2 ** j
#         b_x = a_x ^ randint
#         if division_by_corner(b_x, g_x) == 0:
#             n = 0
#             for i in bin(randint):
#                 if i == '1':
#                     n += 1
#             if n < 4:
#                 print(bin(randint))


def code_words():
    g_x = int(input("Enter the g(x): "), 2)
    epsilon = float(input("Enter the epsilon: "))
    l = int(input('Enter the message length: '))
    probability = 0.1
    words_before = []
    words = []
    for m in range(0, 2 ** l, 1):
        model = CRCModel(g_x, epsilon, l, probability)
        model.m = m
        model.c_x = division_by_corner(model.m * (2 ** model.r), model.g_x)
        model.a_x = model.m * (2 ** model.r) + model.c_x
        print('m :{}'.format(bin(model.m)))
        print('a(x) :{}'.format(bin(model.a_x)))
        print('g(x) :{}'.format(bin(model.g_x)))
        print('с(x) :{}'.format(bin(model.c_x)))
        print('r :{}\n'.format(model.r))
        words.append(bin(model.a_x))
        words_before.append(bin(m))
    print(words_before)
    print(words)


def lineplot(arrays, x_label="X", y_label="Y", title="CRC"):
    """Graph initialization"""
    _, ax = plt.subplots()

    ax.plot(arrays[0][0], arrays[0][1], lw=2, color='blue', alpha=1)
    # ax.plot(arrays[1][0], arrays[1][1], lw=2, color='red', alpha=1)
    # ax.plot(arrays[2][0], arrays[2][1], lw=2, color='green', alpha=1)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.show()


def division_by_corner(dividend, divisor):
    """The function which realize division by corner"""
    if len(bin(dividend)) < len(bin(divisor)):
        return dividend
    temp_divisor = divisor << len(bin(dividend)) - len(bin(divisor))  # Left-aligning
    remainder = dividend ^ temp_divisor
    while len(bin(remainder)) >= len(bin(divisor)):
        temp_divisor = divisor << len(bin(remainder)) - len(bin(divisor))  # Left-aligning
        remainder = remainder ^ temp_divisor
    return remainder


def add_zero_to_ax(a_x, length):
    """Adding zeroes to beginning of A(x)"""
    return "0" * abs(len(a_x) - length) + a_x


class CRCModel:
    def __init__(self, g_x, epsilon, message_len, probability):
        """Initializing the input parameters"""
        self.g_x = g_x
        self.epsilon = epsilon
        self.message_len = message_len
        self.probability = probability
        self.r = len(bin(self.g_x)) - 3
        self.m, self.a_x, self.e, self.c_x, self.b_x = None, None, None, None, None

    def message_generate(self):
        self.m = random.getrandbits(self.message_len)

    def error_vector_generate(self, length):
        """Generating the error vector"""
        result = ''
        for _ in range(length):
            if random.uniform(0, 1.0) <= self.probability:
                result += '1'
            else:
                result += '0'
        self.e = int(result, 2)

    def error_vector_generate_c(self, sequence):
        """Generating the error vector for C task"""
        result = ''
        for bit in sequence:
            rand = random.uniform(0, 1.0)
            if rand <= self.probability and bit != '0':
                result += '1'
            else:
                result += '0'
        self.e = int(result, 2)


def main(mode):
    """Main program function"""
    g_x = int(input("Enter the g(x): "), 2)
    epsilon = float(input("Enter the epsilon: "))
    message_len = int(input('Enter the message length: '))
    graph_parameters = []

    probabilities = []
    e_probabilities = []
    for probability in np.arange(0, 1 + 0.01, 0.01):
        model = CRCModel(g_x, epsilon, message_len, probability)
        ne = 0
        n = int(9 // (4 * model.epsilon ** 2))
        for _ in range(n + 1):
            model.message_generate()
            model.c_x = division_by_corner(model.m * (2 ** model.r), model.g_x)
            model.a_x = model.m * (2 ** model.r) + model.c_x
            if mode:
                model.error_vector_generate_c(add_zero_to_ax(bin(model.a_x)[2::], model.message_len + model.r))
            else:
                model.error_vector_generate(model.message_len + model.r)

            model.b_x = model.a_x ^ model.e
            if division_by_corner(model.b_x, model.g_x) == 0 and model.e != 0:
                ne += 1
        try:
            e_probability = ne / n
        except ZeroDivisionError:
            e_probability = 0
        e_probabilities.append(e_probability)
        probabilities.append(probability)
    graph_parameters.append([probabilities, e_probabilities])
    lineplot(graph_parameters, 'P', 'Pe', 'CRC')


if __name__ == "__main__":
    main(0)

