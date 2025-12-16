from typing import List, Tuple, Dict, Optional,Union

numbers: List[int] = ['a', 2, 3]
print(numbers)
coordinates: Tuple[int, int] = (10, 20)
user: Dict[str, int] = {"age": 25, "score": 90}

age: Optional[int] = None
value: Union[int, float] = 3.14

print(f'List of Numbers: {numbers}\nTuple: {coordinates}\nUser: {user}\nAge: {age}\nValue: {value}')


#Type-Hints using Function:--

def greet(name: str, age: int) -> str:
    return f"Hello {name}, you are {age} years old."

print(greet("Shivam", 22))
