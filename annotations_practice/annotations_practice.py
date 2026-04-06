from typing import Optional
from typing import Union
def multiply(a: int, b: int) -> int:
    return a * b

print(multiply(4, 8))

def sum_numbers(numbers: list[int]) -> int:
    return sum(numbers)
list_numbers = [4, 3, 8]
print(sum_numbers(list_numbers))

def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Пользователь найден"
    return None

print(find_user(None))

def process_input(value: Union[int, str]) -> str:
    return f"Ты передал: {value}"

print(process_input(234))

class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Привет, меня зовут {self.name}!"

user = User("Mira", 9)
print(user.greet())

def get_even_numbers(numbers: list[int]) -> list[int]:
    return [num for num in numbers if num % 2 == 0]

list_even_on_two_nums = [1, 2, 4, 6, 7, 8]
print(get_even_numbers(list_even_on_two_nums))