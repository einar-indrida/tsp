#!/usr/bin/python3

import random
import math
import sys


def gen_cities(num_cities, min_x, max_x, min_y, max_y):
    cities = []
    for i in range(0, num_cities):
        entry = ( random.randrange(min_x, max_x), random.randrange(min_y, max_y))
        cities.append(entry)

    return cities

        

def generate(n, A):
    c = []

    for i in range(0, n):
        c.append(0)

#    print("a: ", A)
    yield A

    i = 0
    while (i < n):
        if c[i] < i:
            if ((i % 2) == 0):
                # swap(A[0], A[i])
                X = A[0]
                A[0] = A[i]
                A[i] = X
            else:
                # swap(A[c[i]], A[i])
                X = A[c[i]]
                A[c[i]] = A[i]
                A[i] = X

#            print("a: ", A)
            yield A
            c[i] += 1
            i = 0
        else:
            c[i] = 0
            i += 1



def calc_eucledian_distance(my_cities, arr):
    length = 0.0
    for i in range(0, len(arr)-1):
        length += math.sqrt( pow(my_cities[arr[i]][0] - my_cities[arr[i+1]][0], 2) + pow(my_cities[arr[i]][1] - my_cities[arr[i+1]][1], 2))

    return length




# generate(10, [0,1,2,3,4,5,6,7,8,9])


how_many_cities = 10

if __name__ == '__main__':

    factorial = 1
    for i in range(1, how_many_cities+1):
        factorial *= i

    print("Factorial: %r" % factorial)

    my_cities = gen_cities(how_many_cities, 0, 100, 0, 100)

    print("my_cities: %r" % my_cities)

    cities_arr = []
    for i in range(0, len(my_cities)):
        cities_arr.append(i)

    min_length = 99999999.0
    min_arr = []

    for i in generate(len(cities_arr), cities_arr):
        factorial -= 1

#        print("i: %r\r" % i)
        length = calc_eucledian_distance(my_cities, i)
        if (length < min_length):
            print("i: %r (min_arr: %r), length: %f" % (i, min_arr, length) )
            min_length = length
            min_arr = i[:]

        if ((factorial % 1000000) == 0):
            print("remaining: %r" % factorial)
            print("i: %r (min_arr: %r), length: %f" % (i, min_arr, min_length) )
