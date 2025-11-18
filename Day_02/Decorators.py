#Basic Decorator:-
# def decorator(func):
#     def wrapper():
#         print('Good Morning!')
#         func('Shivam')
#         print('Have a Good Day!!!')
#     return wrapper

# @decorator
# def greet(name):
#     print(f'Hi, {name}')

# greet()


#Decorator with argument:-
# def repeat(n):
#     def decorator(func):
#         def wrapper(*args,**kwargs):
#             for _ in range(n):
#                 func(*args,**kwargs)
#         return wrapper
#     return decorator

# @repeat(3)
# def greet(name):
#     print(f"Hello, {name}!")

# greet("Shivam")



#Preserving Meta-Data Using functools.wraps:-
# from functools import wraps

# def my_decorator(func):
#     @wraps(func)
#     def wrapper():
#         print("Before execution")
#         func()
#         print("After execution")
#     return wrapper

# @my_decorator
# def say_hello():
#     ''' Greeting the User! '''
#     print("Hello!")

# say_hello()
# print(say_hello.__name__)
# print(say_hello.__doc__)
