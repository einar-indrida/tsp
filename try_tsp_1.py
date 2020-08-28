#!/usr/bin/python3

import random
import math
import sys



# if you want to create fixed cities - not randomly generated each time
# use:  return [ (x1,y1), (x2, y2), (x3, y3) ]
# where the x and y are the co-oridinations in question
def gen_cities(num_cities, min_x, max_x, min_y, max_y):
    return [(0, 58), (99, 4), (24, 89), (90, 96), (58, 8), (62, 22), (98, 65), (20, 22), (45, 34), (64, 51)]

    cities = []
    for i in range(0, num_cities):
        entry = ( random.randrange(min_x, max_x), random.randrange(min_y, max_y))
        cities.append(entry)

    return cities

        

# you *could* use itertool here to generate 
# all the permutations
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


# room for improvement here: memoization of the entries, into a table, then look it up...
# but for now... just calculate it every time
def calc_eucledian_distance(my_cities, arr):
    length = 0.0
    for i in range(0, len(arr)-1):
        length += math.sqrt( pow(my_cities[arr[i]][0] - my_cities[arr[i+1]][0], 2) + pow(my_cities[arr[i]][1] - my_cities[arr[i+1]][1], 2))

    # close the trip...
    length += math.sqrt( pow(my_cities[arr[0]][0] - my_cities[arr[len(arr)-1]][0], 2) + pow(my_cities[arr[0]][1] - my_cities[arr[len(arr)-1]][1], 2))
    
    return length




# generate(10, [0,1,2,3,4,5,6,7,8,9])


how_many_cities = 10

if __name__ == '__main__':

    factorial = 1
    for i in range(1, how_many_cities+1):
        factorial *= i

    print("Factorial: %r" % factorial)

    my_cities = gen_cities(how_many_cities, 0, 100, 0, 100)

    how_many_cities = len(my_cities)

    print("my_cities: %r" % my_cities)
    print("len(my_cities): %r" % how_many_cities)

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

    for i in range(0, len(my_cities)):
        print("(%r, %r) -> " % (my_cities[i][0], my_cities[i][1]), end='')

    print("(%r, %r)\n" % (my_cities[0][0], my_cities[0][1]) )

