from testClass import algo
import sys
print(sys.path)

al = algo()
a = al.create_random_array(10000, 2, 9000)
print(a)

b = al.bubble_sort(a)
print(b)