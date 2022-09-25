from enum import Enum


class Day(Enum):
        Saturday = 1
        Sunday = 2
        Monday = 3
        Tuesday = 4
        Wednesday = 5

        def get_string(self):
                if self == Day.Saturday:
                        return "Saturday"
                elif self == Day.Sunday:
                        return "Sunday"
                elif self == Day.Monday:
                        return "Monday"
                elif self == Day.Tuesday:
                        return "Tuesday"
                elif self == Day.Wednesday:
                        return "Wednesday"
                
        @staticmethod
        def get_day_with_value(val):
                switcher = {
                        1: Day.Saturday,
                        2: Day.Sunday,
                        3: Day.Monday,
                        4: Day.Tuesday,
                        5: Day.Wednesday
                        }
                return switcher.get(val, "nothing")
