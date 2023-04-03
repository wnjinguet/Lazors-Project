class Convert_Game_Data:
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
        
        grid = [] #Raw grid data
        #Extract grid from START to STOP
        for index in range(len(raw_data)):
            if raw_data[index] == "GRID START":
                continue
            elif raw_data[index] == "GRID STOP":
                break
            else:
                #Puts all values in each grid together
                grid.append(''.join(raw_data[index].split()))
        
        self.grid = [] #Corrected grid
        #Separates each value in the raw grid data as a single element (nested list)
        for index in grid:
            temp_grid = []
            for value in index:
                temp_grid.append(value)
                self.grid.append(temp_grid)
        
#Test
a = Game('mad_4.bff')
b = a.database()
print(b)

class Game_Board:
    def __init__(self, grid, starting_point):
        self.grid = grid
        self.starting_point = starting_point
        
    #Available coordinates for the blocks
    def blocks_coord(self, grid):
        blocks_positions = []
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] == 'o':
                    blocks_positions.append(tuple((x,y)))
        return blocks_positions

Laser (Mingyu)

Block (Wilkins)

class Block:
 # This represents a block
    def __init__(self, type):
    # This iinitializes the class
    
    self.type = type
   
  def placable(self): 

    


Solver (Everyone) (find path, find fixed block, solver)
