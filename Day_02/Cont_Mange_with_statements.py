#Basic Context Mangament and with statment:-
# with open("greet.txt","r") as f:
#     data=f.read()
#     print(data)


# 2. Using __enter__ and __exit__ Methods:-

# class MyContextExample:
#     def __enter__(self):
#         print("Entering the context!")
#         return 'Block Completed'

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print("Exiting the context!")
#         if exc_type:
#             print(f"An exception occurred: {exc_val}")
#         print("Cleanup complete.")
#         return False
    
# with MyContextExample() as c:
#     print(c)
#     print('Inside the Context!!!')
#     #raise ValueError('Something Wrong...')


# 3. Using contextlib.contextmanager:-    
from contextlib import contextmanager

@contextmanager
def my_context():
    print('entering the context!')
    yield "Resource Ready"
    print("Exiting the context!")

with my_context() as data:
    print(data)
    print('hi')
