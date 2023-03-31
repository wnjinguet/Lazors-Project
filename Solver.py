class Lazors_Game:
    def __init__(self, filename):
        #Read file
        self.file = open(filename, 'r').read()
    
    def raw_data_converter(self):
        #Separate file's data into individual lines
        data_lines = self.file.split('\n')
        raw_data = [] #Store raw data
        #Check every line of the data
        for line in data_lines:
            if '#' not in line and line != '':
                #Store useful raw data
                raw_data.append(line)
        pass
Other.
