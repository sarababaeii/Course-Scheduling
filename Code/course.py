from file_manager import FileManager
from date import Date
from day import Day
from math import *


class Course:
        def __init__(self, num, name, unit, lecturer_num):
                self.num = num
                self.name = name
                self.unit = unit
                self.lecturer_num = lecturer_num
                self.scheduled_dates = []

        def get_class_num(self):
                return ceil(self.unit / 2)

        def is_3_units(self):
                return self.unit == 3

        def insert_date(self, day, period_num):
                self.scheduled_dates.append(Date(day, period_num))
                
        @staticmethod
        def get_index_of_num(n, array):
                for i in range(0, len(array)):
                        if array[i].num == n:
                                return i
                return -1
        
        @staticmethod
        def create_courses(file_name):
                rows = FileManager.read_from_csv(file_name)
                courses = []
                for row in rows:
                        courses.append(Course(int(row[0]), row[1], int(row[2]), 0))
                return courses

        @staticmethod
        def set_lecturers(file_name, courses):
                rows = FileManager.read_from_csv(file_name)
                for row in rows:
                        i = Course.get_index_of_num(int(row[1]), courses)
                        if i >= 0:
                                courses[i].lecturer_num = int(row[2])
