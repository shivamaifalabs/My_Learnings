# Lambda:-
add=lambda x,y:x+y
print(add(10,20))

# OR---------------------------------------------

print((lambda x:x**2)(5))

# Map:-

nums = [1,2,3,4,5]
squares = list(map(lambda x: x*x,nums))
print(squares)

# Filter:-
nums = [10,15,20,25,30]
evens = list(filter(lambda x: x % 2 == 0,nums))
print(evens)

# Reduce:-

from functools import reduce

nums = [1,2,3,4,5]
product = reduce(lambda x, y: x * y,nums)
print(product)
