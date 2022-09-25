import csv


class FileManager:
        
        @staticmethod
        def read_from_csv(file_name):
                rows = []
                with open(file_name, 'r') as file:
                        csvreader = csv.reader(file)
                        header = next(csvreader)
                        for row in csvreader:
                                rows.append(row)
#                print(header)
 #               print(rows)
                return rows
