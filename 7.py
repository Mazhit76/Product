# """Обычный класс и класс со слотами"""
#
from pympler import asizeof
from timeit import timeit


class BasicClass:
    """
    В обычной ситуации в Python в объекты можно добавлять
    новые атрибуты вне описания класса
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calc(self):
        return self.x ** self.y


bc = BasicClass(5, 6)
print(bc.__dict__)
print(asizeof.asizeof(bc))
bc.z = 7
print(bc.__dict__)
print(asizeof.asizeof(bc))

print('=' * 80)
"""
The class variable __slots__:
1.) reduces memory size of instances
2.) prevents automatic creation of __dict__ and disallows adding new attributes to instances
3.) reduces access time to attributes of class instances
"""
#
from timeit import timeit



class BasicClassSlots:
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calc(self):
        return self.x ** self.y


bc_slots = BasicClassSlots(5, 6)
print(bc_slots.__slots__)
print(asizeof.asizeof(bc_slots))
# BCS_OBJ.param_z = 7
# print(bs_slots_object.__dict__)


print('=' * 80)
"""
3.) reduces access time to attributes of class instances
"""
print(timeit(bc.calc))
print(timeit(bc_slots.calc))


print('=' * 80)
"""
4.) In the case of using __slots__, we cannot add an instance attribute of the class,
    but we can add a class attribute.
"""

BasicClassSlots.CLASS_ATTR = 555
print(bc_slots.CLASS_ATTR)


