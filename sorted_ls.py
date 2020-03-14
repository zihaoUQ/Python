#!/usr/bin/env python 3

# sort a collection of lists by a position in the lists

# sort the collection of lists by the index 3 (4th position) in the lists

ls1 = [[1,2,3,4], [4,3,2,1], [2,4,1,3]]
ls1_sorted_by_index_3 = sorted(ls1, key=lambda index_value: index_value[3])
print('{}'.format(ls1_sorted_by_index_3))

# use the operator module to sort lists, tuples, dicts by multiple keys

from operator import itemgetter


# first sort the lists by index position 3, and then while maintaining this
# sorted order, further sort the lists by the values in index position 0

ls1_sorted_by_index_3_and_0 = sorted(ls1, key=itemgetter(3, 0))
print('{}'.format(ls1_sorted_by_index_3_and_0))

class Student:

    def _init_(self, name, grade, age):
        self.name = name
        self.grade = grade
        self.age = age

    def __repr__(self):
        return repr((self.name, self.grade, self.age))

student_objects = [Student('John', 'A', 15), Student('Jane', 'B', 12),
                   Student('dave', 'B', 10)]
print(sorted(student_objects, key=lambda student:student.age))