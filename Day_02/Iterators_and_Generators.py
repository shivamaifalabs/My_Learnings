# #Iterator Class:- 

# class Counter:
#     def __init__(self, low, high):
#         self.current = low
#         self.high = high

#     def __iter__(self):
#         return self

#     def __next__(self):
#         if self.current > self.high:
#             raise StopIteration
#         else:
#             number = self.current
#             self.current += 1
#             return number

# for number in Counter(1,5):
#     print(number)

# 02. Same using Generators:-
# def Counter(start,end):
#     while start<=end:
#         yield start
#         start+=1
# for number in Counter(1,5):
#     print(number)


# 03. Generators Using Large File:-

# def read_large_file(filename):
#     with open(filename) as f:
#         for line in f:
#             yield line.strip()

# for line in read_large_file("large_datasets.txt"):
#     print(line)


# 04. Generator Expressions:-

result=(x**2 for x in range(1,6))
print(next(result))
print(next(result))
print(next(result))
print(next(result))
print(next(result))
