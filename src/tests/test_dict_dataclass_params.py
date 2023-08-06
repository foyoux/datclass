from dataclasses import dataclass
from typing import List

from datclass import DatClass


@dataclass
class Student(DatClass):
    name: str = None
    age: int = None


@dataclass
class Class(DatClass):
    name: str = None
    teacher: str = None
    students: List[Student] = None


def test_dict_dataclass_params():
    Class(**{'name': 'class1', 'teacher': 'teacher1', 'students': [{'name': 'student1', 'age': 18}]})
    Class(name='class1', teacher='teacher1', students=[Student(name='student1', age=18)])
    Class(**{'name': 'class1', 'teacher': 'teacher1', 'students': [Student(name='student1', age=18)]})
