from dataclasses import dataclass
from typing import List

from datclass import DatClass


@dataclass
class Student(DatClass):
    name: str = None
    age: int = None


@dataclass
class Teacher(DatClass):
    name: str = None
    age: int = None


@dataclass
class Class(DatClass):
    name: str = None
    teacher: str = None
    students: List[Student] = None


@dataclass
class Class2(DatClass):
    name: str = None
    teacher: Teacher = None
    students: List[Student] = None


def test_dict_dataclass_params():
    Class(**{'name': 'class1', 'teacher': 'teacher1', 'students': [{'name': 'student1', 'age': 18}]})
    Class(name='class1', teacher='teacher1', students=[Student(name='student1', age=18)])
    Class(**{'name': 'class1', 'teacher': 'teacher1', 'students': [Student(name='student1', age=18)]})


def test_dict_dataclass_params2():
    Class2(
        **{
            'name': 'class2',
            'teacher': {'name': 'teacher1', 'age': 18},
            'students': [{'name': 'student1', 'age': 18}]
        }
    )
    Class2(
        name='class2',
        teacher=Teacher(name='teacher1', age=18),
        students=[Student(name='student1', age=18)]
    )
    Class2(
        **{
            'name': 'class2',
            'teacher': Teacher(name='teacher1', age=18),
            'students': [Student(name='student1', age=18)]
        }
    )
