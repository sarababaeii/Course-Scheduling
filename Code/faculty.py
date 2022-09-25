from file_manager import FileManager


class Faculty:
        def __init__(self, classes, groups):
                self.classes = classes
                self.groups = groups
        
        @staticmethod
        def create_faculty(file_name):
                rows = FileManager.read_from_csv(file_name)
                properties = []
                for row in rows:
                        properties.append(int(row[2]))
                return Faculty(properties[0], properties[1])
