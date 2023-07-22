import csv

# A class for registering the codes collected by the main code in a csv file.
class CodeCollector():
    def __init__(self):
        # Create an instance of the open file
        self.file = open('codes.csv', 'w')

        # Create an instance of the csv writer
        self.writer = csv.writer(self.file)

        # Create an instance of the csv reader
        self.reader = csv.reader(self.file)

        # opens and reads the csv file and registers all the codes to the self.codes list.
        self.codes = []

        for i, row in enumerate(self.reader, start=row[-10]):
            self.codes.append(row)
        
        


    # Checks if the code collected is already registered in the csv file and if not, writes it to the csv file.
    def register_code(self, code) -> bool:
        '''
        Checks if the code collected is already registered in the csv file and if not, writes it to
        the csv file.
        '''

        if code not in self.codes:
            # opens the csv file and check the first line to see if the code is already registered
            with open('codesdb.csv', 'a') as csvfile:
                    csvreader = csv.reader(csvfile)
                    csvwriter = csv.writer(csvfile)
                    # reads the first line to see if the code is already registered
                    first_line = csvreader.readline()
                    # if the code is already registered, don't append the code to the csv file
                    if first_line != code:
                        csvwriter.writerow(code)
                        self.codes.append(code)
                        return False
            

    def add_code(self, code:str):
        '''
        Adds the code to the csv file.
        '''

        # Checks the codes to see if they are 10 and pops the first if bigger
        if len(self.codes) > 10:
            self.codes.pop(0)

        with open('codesdb.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(code)
            
        self.register_code(code)
        self.codes.append(code)


    def get_codes(self):
        '''
        Returns the codes collected in the csv file.
        '''

        with open('codesdb.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            return csvreader.readline()

