from abc import ABC
from typing import Callable, Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.name = None

    def __set_name__(self, owner: Callable, name: int) -> None:
        self.name = f"_{name}"

    def __get__(self, instance: Callable, owner: Callable) -> Any:
        return getattr(instance, self.name)

    def __set__(self, instance: Callable, value: int) -> None:
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"Value must be between {self.min_amount} and {self.max_amount}")
        setattr(instance, self.name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self,
                 age: IntegerRange,
                 height: IntegerRange,
                 weight: IntegerRange) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14),
    height=IntegerRange(80, 120),
    weight=IntegerRange(20, 50)



class AdultSlideLimitationValidator(SlideLimitationValidator):
    age=IntegerRange(14, 60),
    height=IntegerRange(120, 220),
    weight=IntegerRange(50, 120)


class Slide:
    def __init__(self, name: str, limitation_class: Callable) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.height, visitor.weight)
        except ValueError:
            return False
        return True

