import sys

print(f'Script Name is: {sys.argv[0]}')

if len(sys.argv) < 3:
    print("No arguments passed by the user!")
else:
    a = int(sys.argv[1])
    b = int(sys.argv[2])

    if a > b:
        print(f'{a} is greater than {b}')
    elif a < b:
        print(f'{b} is greater than {a}')
    else:
        print(f'Both numbers are equal: {a} = {b}')
