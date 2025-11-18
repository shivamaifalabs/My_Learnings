# Reference- Counting:--

import sys
x = []
print(sys.getrefcount(x))


# Garbage- Collector ( Circular-Reference ):--

a = []
b = []
a.append(b)
b.append(a)


# 1.) __slots__ (Memory Optimization for Classes):--

class User:
    __slots__ = ["name", "age"]

    def __init__(self, name, age):
        self.name = name
        self.age = age

# 2.) weakref (Avoid Memory Leaks):--

import weakref

class A:
    pass

obj = A()
r = weakref.ref(obj)

print(r())    # Access object
del obj
print(r())    # None (object is destroyed)
