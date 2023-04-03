class Convert_Game_Data:
    def __init__(self, filename):
        #Read file
        self.file = open(filename, 'r').read()
    
    #Isolate the data for the grid
    def grid_data_converter(self):
        grid = [] #Raw grid data
        self.grid = [] #Corrected grid
        
        #Separate file's data into individual lines
        data_lines = self.file.split('\n')
        raw_data = [] #Store raw data
        #Check every line of the data
        for line in data_lines:
            #To prevent the mad_1 file
            if '#' not in line and line != '':
                #Store useful raw data
                raw_data.append(line)
               
        #Extract grid from START to STOP
        for index in range(len(raw_data)):
            if raw_data[index] == "GRID START":
                continue
            elif raw_data[index] == "GRID STOP":
                break
            else:
                #Puts all values in each grid together
                grid.append(''.join(raw_data[index].split()))
        
        #Separates each value in the raw grid data as a single element (nested list)
        for index in grid:
            temp_grid = [] #Temporary storage
            for value in index:
                temp_grid.append(value)
                self.grid.append(temp_grid) #Nested list
        
        #Removes grid from raw data
        for x in range(len(raw_data)):
            if raw_data[0] != 'GRID STOP':
                raw_data.remove(raw_data[0])
            else:
                raw_data.remove(raw_data[0])
                break 
        return raw_data
    
    #Record the blocks that will be used in the game
    def check_for_blocks(self):
        blocks = {}
        for row in raw_data:
            #Need to extract raw_data first?
        pass
    
####Test####
#a = Game('mad_4.bff')
#b = a.database()
#print(b)

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

class Grid(object):
    """
    generate various grids.

    Parameters:
        original_grid (list): A list of lists that represents the original grid.

    Attributes:
        original_grid (list): The original grid.
        length (int): The length of the original grid.
        width (int): The width of the original grid.
    """

    def __init__(self, original_grid):
        self.original_grid = original_grid
        self.length = len(original_grid)
        self.width = len(original_grid[0])

    def gen_grid(self, list_grid, position):

        # Make a copy of the list_grid so that we don't modify the original list
        blocks = list(list_grid)

        # Loop through each cell in the original grid
        for row in range(self.length):
            for column in range(self.width):
                # Check if the cell is not part of the specified position
                if [row, column] not in position:
                    # Check if the cell is not already filled with a block
                    if self.original_grid[row][column] != 'x':
                        # Place the next available block in the cell
                        self.original_grid[row][column] = blocks.pop(0)
                        # Stop the loop if all blocks have been placed
                        if not blocks:
                            return self.original_grid

        # Return the updated grid
        return self.original_grid


class Lazor(object):

    # identify the correct grid and returning a lazor path.

    def __init__(self, grid, lazor_list, hole_list):
        self.grid = grid
        self.lazor_list = lazor_list
        self.hole_list = hole_list

    def block(self, block_type):
        """
        identify the function of different blocks.
        **Parameters**
            block_type: *str*
                This represents different blocks:
                'A': Reflect block
                'B': Opaque block
                'C': Refract block
                'D': Crystal block
                'o': Blank space
                'x': Unavailable space
        **Return**
            new_direction: *list*
                The new direction of the lazor.
        """
        new_direction = []
        if block_type == 'A':
            if self.point[0] & 1 == 0:
                new_direction = [self.direction[0] * (-1), self.direction[1]]
            else:
                new_direction = [self.direction[0], self.direction[1] * (-1)]
        elif block_type == 'B':
            pass
        elif block_type == 'C':
            if self.point[0] & 1 == 0:
                new_direction = [self.direction[0], self.direction[1],
                                 self.direction[0] * (-1), self.direction[1]]
            else:
                new_direction = [self.direction[0], self.direction[1],
                                 self.direction[0], self.direction[1] * (-1)]
        elif block_type == 'D':
            if self.point[0] & 1 == 0:
                new_direction = [2, 0,
                                 self.direction[0], self.direction[1]]
            else:
                new_direction = [0, 2,
                                 self.direction[0], self.direction[1]]
        elif block_type in ('o', 'x'):
            new_direction = self.direction

        return new_direction

    def meet_block(self, point, direction):

        # check whether the lazor encounters a functional block and return the new direction of the lazor.
        # Check if the point and direction are valid
        if not isinstance(point, list) or len(point) != 2 or not isinstance(direction, list) or len(direction) != 2:
            raise ValueError("Invalid input for point or direction")

        # Calculate the next position of the laser
        x1, y1 = point[0], point[1] + direction[1]
        x2, y2 = point[0] + direction[0], point[1]

        # Obtain the block the laser touches
        if point[0] & 1 == 1:
            # Check if y1 is within the grid bounds
            if y1 < 0 or y1 >= len(self.grid):
                raise ValueError("Invalid position for y1")
            block_type = self.grid[y1][x1]
            new_direction = self.block(block_type)
        else:
            # Check if x2 is within the grid bounds
            if x2 < 0 or x2 >= len(self.grid[0]):
                raise ValueError("Invalid position for x2")
            block_type = self.grid[y2][x2]
            new_direction = self.block(block_type)

        return new_direction

    def check_position(self, lazor_coordinate, direction):
        """
        Check if the laser and its next step are inside the grid, if not,
        return to the last step.
        """
        width = len(self.grid[0])
        length = len(self.grid)
        x = lazor_coordinate[0]
        y = lazor_coordinate[1]

        # Determine whether the position is in the grid.
        if x < 0 or x > (width - 1) or y < 0 or y > (length - 1) or \
                (x + direction[0]) < 0 or (x + direction[0]) > (width - 1) or \
                (y + direction[1]) < 0 or (y + direction[1]) > (length - 1):
            return True
        else:
            return False

    # simulate the path of a lazor beam as it passes through a grid of blocks, and initialize an empty result
    # list and a lazor list, which contains a nested list with a lazor starting coordinates and direction for each
    # lazor in self.lazor_list.
    def lazor_path(self):

        # Initialize empty result list and lazor list
        result = []
        lazor_list = [[l] for l in self.lazor_list]

        # Maximum number of iterations to avoid infinite loop
        max_iter = 30

        # Iterate through the lazor in the list
        for n in range(max_iter):
            for k, lazor in enumerate(lazor_list):
                # Get the current coordination and direction of the lazor
                coordination_x, coordination_y, direction_x, direction_y = lazor[-1]
                coordination = [coordination_x, coordination_y]
                direction = [direction_x, direction_y]

                # Check if the lazor is inside the boundary
                if self.check(coordination, direction):
                    continue
                else:
                    # Get the next coordination and direction of the lazor after a step
                    next_step = self.meet_block(coordination, direction)

                    # If there are no elements in the list, it indicates it is block B
                    if not next_step:
                        lazor.append([coordination[0], coordination[1], 0, 0])
                        if coordination in self.hole_list and coordination not in result:
                            result.append(coordination)

                    # If there are 2 elements, it is "o" or A block
                    elif len(next_step) == 2:
                        direction = next_step
                        coordination = [coordination[0] + direction[0], coordination[1] + direction[1]]
                        lazor.append([coordination[0], coordination[1], direction[0], direction[1]])
                        if coordination in self.hole_list and coordination not in result:
                            result.append(coordination)

                    # If there are 4 elements, it is C block or D block
                    elif len(next_step) == 4:
                        # If the first two elements in next_step have the same x-coordinate, it's a straight line
                        if next_step[0] == next_step[2]:
                            direction = next_step
                            coordination = [coordination[0] + direction[0], coordination[1] + direction[1]]
                            lazor.append([coordination[0], coordination[1], direction[2], direction[3]])
                            if coordination in self.hole_list and coordination not in result:
                                result.append(coordination)
                        else:
                            direction = next_step
                            coordination_new_lazor1 = [coordination[0] + direction[0], coordination[1] + direction[1]]
                            coordination_new_lazor2 = [coordination[0], coordination[1]]
                            new_lazor = [
                                [coordination_new_lazor1[0], coordination_new_lazor1[1], direction[0], direction[1]]]
                            lazor_list.append(new_lazor)
                            lazor.append(
                                [coordination_new_lazor2[0], coordination_new_lazor2[1], direction[2], direction[3]])
                            coordination = coordination_new_lazor2
                            if coordination in self.hole_list and coordination not in result:
                                result.append(coordination)

                    # If next_step has other lengths, something is wrong
                    else:
                        print('Wrong')

            # Check if all holes have been reached
            if len(result) == len(self.hole_list):
                return lazor_list

        # If not all holes have been reached after max_iter iterations, return 0
        return 0

Block (Wilkins)

class Block:
 # This represents a block
    def __init__(self, type):
    # This iinitializes the class
    
    self.type = type
   
  def placable(self): 

    


Solver (Everyone) (find path, find fixed block, solver)
