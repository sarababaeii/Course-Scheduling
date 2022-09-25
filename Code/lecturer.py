from file_manager import FileManager
from date import Date
from day import Day


class Lecturer:
        def __init__(self, num, availabe_dates):
                self.num = num
                self.availabe_dates = availabe_dates
        
        @staticmethod
        def create_lecturers(file_name):
                rows = FileManager.read_from_csv(file_name)
                lecturers = []
                for i in range (1, len(rows)):
                        availabe_dates = []
                        for j in range(0, 45):
                                if rows[i][j + 1] == '1':
                                        d = Day.get_day_with_value(int(j / 9) + 1)
                                        h = (j % 9) + 1
                                        availabe_dates.append(Date(d, h))
                        lecturers.append(Lecturer(int(rows[i][0]), availabe_dates))
                return lecturers
