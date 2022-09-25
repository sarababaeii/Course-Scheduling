class Period:
        def __init__(self, num, start, end):
                self.num = num
                self.start = start
                self.end = end

        def length(self):
                return self.end - self.start

        def has_intersec_with(self, p):
                return (self.start >= p.start and  self.start <= p.end) or (p.start >= self.start and  p.start <= self.end)

        def is_2_hours(self):
                return self.length() == 2

        def get_string(self):
                if self.start == 7.45:
                        return "7:45 - 9:15"
                elif self.start == 9.15:
                        return "9:15 - 10:45"
                elif self.start == 10.45:
                        return "10:45 - 12:15"
                elif self.start == 13.30:
                        return "13:30 - 15"
                elif self.end == 16.30:
                        return "15 - 16:30"
                else:
                        return str(self.start) + " - " + str(self.end)

        @staticmethod
        def get_index_of_num(n, array):
                for i in range(0, len(array)):
                        if array[i].num == n:
                                return i
                return -1
