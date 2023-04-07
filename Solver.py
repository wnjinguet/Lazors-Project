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
        
        print("self.grid:\n", self.grid) 
        
        #Removes grid from raw data
        for x in range(len(raw_data)):
            if raw_data[0] != 'GRID STOP':
                raw_data.remove(raw_data[0])
            else:
                raw_data.remove(raw_data[0])
                break 
        
        print("Raw data without grid:\n", raw_data)
        
        #return raw_data
    
    #Record the blocks that will be used in the game
    #WORK IN PROGRESS
    def check_for_blocks(self):
        blocks = {}
        for row in raw_data:
            #Need to extract raw_data first?
        pass
    
####Test for Class Convert_Game_Data:####
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
class Grid_part(object):

    def __init__(self, original_grid):
        self.list_grid = None
        self.length = len(original_grid)
        self.width = len(original_grid[0])
        self.original_grid = original_grid

    def generate_grid(self, list_grid, position):

        self.list_grid = list_grid
        for row in range(len(self.original_grid)):
            for column in range(len(self.original_grid[0])):
                if [row, column] not in position:
                    if self.original_grid[row][column] != 'x':
                        self.original_grid[row][column] = list_grid.pop(0)
        return self.original_grid


class Lazor_part(object):

    def __init__(self, grid, lazor_list, hole_list):
        self.point = None
        self.grid = grid
        self.lazor_list = lazor_list
        self.hole_list = hole_list

    def block(self, block_type):

        self.type = block_type
        new_direction = []

        # When the laser beam hits the reflect block
        if self.type == 'A':
            if self.point[0] % 2 == 0:
                new_direction = [self.direction[0] * (-1), self.direction[1]]
            else:
                new_direction = [self.direction[0], self.direction[1] * (-1)]

        # When the laser beam hits the opaque block
        elif self.type == 'B':
            new_direction = []

        # When the laser beam hits the refract block
        elif self.type == 'C':
            if self.point[0] % 2 == 0:
                new_direction = [self.direction[0], self.direction[1],
                                 self.direction[0] * (-1), self.direction[1]]
            else:
                new_direction = [self.direction[0], self.direction[1],
                                 self.direction[0], self.direction[1] * (-1)]

        # When the laser beam hits the crystal block
        elif self.type == 'D':
            if self.point[0] % 2 == 0:
                new_direction = [2, 0,
                                 self.direction[0], self.direction[1]]
            else:
                new_direction = [0, 2,
                                 self.direction[0], self.direction[1]]

        # When the laser beam hits the blank space or unavailable space
        elif self.type == 'o' or self.type == 'x':
            new_direction = self.direction

        return new_direction

    def check_position(self, lazor_coordinate, direction):

        width = len(self.grid[0])
        length = len(self.grid)
        x = lazor_coordinate[0]
        y = lazor_coordinate[1]
        # Determine whether the position is in the grid
        if x < 0 or x > (width - 1) or y < 0 or y > (length - 1) or \
                (direction is None) or \
                (x + direction[0]) < 0 or \
                (x + direction[0]) > (width - 1) or \
                (y + direction[1]) < 0 or \
                (y + direction[1]) > (length - 1):
            return True
        else:
            return False

    def lazor_path(self):

        result = []
        lazor_list = []

        for p in range(len(self.lazor_list)):
            lazor_list.append([self.lazor_list[p]])

        for n in range(50):

            for k in range(len(lazor_list)):
                coordination_x, coordination_y, direction_x, direction_y = lazor_list[k][-1]
                coordination = [coordination_x, coordination_y]
                direction = [direction_x, direction_y]

                if self.check_position(coordination, direction):
                    continue
                else:

                    next_step = self.block_reflect(coordination, direction)

                    if not next_step:
                        lazor_list[k].append([coordination[0], coordination[1], 0, 0])
                        if (coordination in self.hole_list) and (coordination not in result):
                            result.append(coordination)

                    elif len(next_step) == 2:
                        direction = next_step
                        coordination = [coordination[0] + direction[0], coordination[1] + direction[1]]
                        lazor_list[k].append([coordination[0], coordination[1], direction[0], direction[1]])
                        if (coordination in self.hole_list) and (coordination not in result):
                            result.append(coordination)

                    elif len(next_step) == 4:
                        if next_step[0] == 0 or next_step[0] == 2:
                            direction = next_step
                            coordination = [coordination[0] + direction[0], coordination[1] + direction[1]]
                            lazor_list[k].append([coordination[0], coordination[1], direction[2], direction[3]])
                            if (coordination in self.hole_list) and (coordination not in result):
                                result.append(coordination)
                        else:
                            direction = next_step
                            coordination_new_lazor1 = [coordination[0] + direction[0], coordination[1] + direction[1]]
                            coordination_new_lazor2 = [coordination[0], coordination[1]]

                            # Create a new lazor list and add the straight line to it
                            new_lazor_list = [
                                [coordination_new_lazor1[0], coordination_new_lazor1[1], direction[0], direction[1]]]
                            lazor_list.append(new_lazor_list)

                            # Add the other part to the list under the original lazor
                            lazor_list[k].append(
                                [coordination_new_lazor2[0], coordination_new_lazor2[1], direction[2], direction[3]])
                            coordination = coordination_new_lazor2
                            if (coordination in self.hole_list) and (coordination not in result):
                                result.append(coordination)
                    else:
                        print('Wrong solution!')
        if len(result) == len(self.hole_list):
            return lazor_list
        else:
            return 0

    def block_reflect(self, point, direction):
        self.point = point
        self.direction = direction

        x1, y1 = point[0], point[1] + direction[1]
        x2, y2 = point[0] + direction[0], point[1]

        if point[0] & 1 == 1:

            block_type = self.grid[y1][x1]
            new_direction = self.block(block_type)
        else:

            block_type = self.grid[y2][x2]
            new_direction = self.block(block_type)

        return new_direction


def find_occupied_spots(small_grid):
    positions = []
    for i in range(len(small_grid)):
        for j in range(len(small_grid[0])):
            block = small_grid[i][j]
            if block in ['A', 'B', 'C']:
                positions.append([i * 2 + 1, j * 2 + 1])
    return positions


def obvious_skip(grid, possibles, lst, holes):
    for i in range(len(holes)):
        x = holes[i][1]
        y = holes[i][0]
        if ((grid[x][y + 1] in ['A', 'B']) and (grid[x][y - 1] in ['A', 'B'])) or \
                ((grid[x + 1][y] in ['A', 'B']) and (grid[x - 1][y] in ['A', 'B'])):
            return False
        else:
            return True


def path_seek(grid, num_blocks_of_type_a, num_blocks_of_type_b, num_blocks_of_type_c, lazor_list, hole_list, position):
    blocks = []
    # Extract the blank positions and replace them with blocks
    for row in grid:
        for element in row:
            if element == 'o':
                blocks.append(element)
    for i in range(num_blocks_of_type_a):
        blocks[i] = 'A'
    for i in range(num_blocks_of_type_a, (num_blocks_of_type_a + num_blocks_of_type_b)):
        blocks[i] = 'B'
    for i in range((num_blocks_of_type_a + num_blocks_of_type_b),
                   (num_blocks_of_type_a + num_blocks_of_type_b + num_blocks_of_type_c)):
        blocks[i] = 'C'
    # Generate a list of permutations of blocks and blank positions
    block_permutations = list(multiset_permutations(blocks))

    while len(block_permutations) != 0:
        blocks_temp = block_permutations[-1]
        blocks_temp_save = copy.deepcopy(blocks_temp)
        block_permutations.pop()
        # Generate a board from the grid function
        original_grid = Grid_part(grid)
        test_board = original_grid.generate_grid(blocks_temp, position)
        # Test the board with the obvious_skip function and run it through Lazor to see if it is the right board
        if obvious_skip(test_board, block_permutations, blocks_temp, hole_list):
            lazor = Lazor_part(test_board, lazor_list, hole_list)
            solution = lazor.lazor_path()
            # Return 0 if the board is wrong and return a list with the path of lazor if it's right
            if solution != 0:
                return solution, blocks_temp_save, test_board
            else:
                continue
class Block:
    
    # This class represents a block
   
    def __init__(self, type):
       
        # This is the class initializer

        # **Parameters**

            # type: *str*
                # the type of block
       
        self.type = type

    def placable(self):
        
        # Return if the block can be placed somewhere

        # **Returns**

            # flag: *bool*
                # Indicate if the block can be placed somewhere

       
        return self.type == "o"

    def place(self, type):
        
        # Replace self's type with te type parameter

        # **Parameters**

            # type: *str*
                # the type of block

       
        self.type = type

    def react(self, lazor, dfs):
        
        # Call dfs to react what will happen according to the lazor and the block

        # **Parameters**

            # lazor: *Lazor class*
                # The moving lazor
            # dfs: *function*
                # DFS function

       
        if self.type == "o" or self.type == "x":  # only go through
            dfs(lazor.step())
        elif self.type == "A":  # reflect
            dfs(lazor.reflect())
        elif self.type == "C":  # go through and reflect
            dfs(lazor.step())
            dfs(lazor.reflect())
            
class Solver:
    
    # The class to solve a BFF puzzle

    def __init__(self, bff: BFF):
        
        #The class initializer

        # **Parameters**

            # bff: *BFF class*
                #the bff

   
        self.bff = bff
        # map to Block class
        self.board = [[Block(t) for t in x] for x in bff.board]
        # map to Lazor class
        self.lazors = [Lazor(x, y, dx, dy) for x, y, dx, dy in bff.lazors]

    def solve(self):
       
        # Return a solution or None

        # **Returns**

            # board: *(2-D list of str) or None*
                # A solution or None

      
        blockMap = ["A", "B", "C"]

        blocks = self.bff.blocks
        board = self.board
        h = len(board)
        w = len(board[0])
        
        def dfs(prv_b, prv_pos):
            # find the type of a remaining block that can be placed
            b = next((i for i, v in enumerate(blocks) if v != 0), None)

            # if not found(means blocks = [0,0,0]), it means we place all
            # blocks, so we can test whether the current board solve the puzzle
            if b is None:
                return self.solved()

            # When using a block, subtract it by 1
            blocks[b] -= 1
            for x in range(h):
                for y in range(w):
                    # This is to optimize the search by checking if previous
                    # used block is the same and the position has been searched
                    # If it is, we can skip
                    # This optimization can shrink time complexity by A!B!C!
                    if prv_b == b and x * w + y <= prv_pos:
                        continue

                    # If the (x, y) block is not placable, skip
                    if not board[x][y].placable():
                        continue
                    board[x][y].place(blockMap[b])

                    # Place a block and keep placing by doing DFS
                    if dfs(b, x * w + y):
                        # If dfs returns True, it means it found a solution,
                        # so stop searching
                        return True
                    board[x][y].place("o")

            # After current search finishes, add the block back
            blocks[b] += 1
            return False
        # The board's items are mapped back from Block class to str
        return [[b.type for b in x] for x in board] if dfs(-1, -1) else None

    def solved(self):
        
        # Return if the current board is a solution

        # **Returns**

           # flag: *bool*
                # Indicate if the current board is a solution

       
        board = self.board

        # record the remaining points that the lazors haven't passed
        points = set(self.bff.points)

        # coordinates of positions and directions that the lazors have passed
        passed = set()

        def dfs(lazor):
            # if the lazor is in passed, skip it
            # otherwise, it would cause an infinite cycle.
            if lazor in passed:
                return
            passed.add(lazor)

            hit_point = (lazor.x, lazor.y)
            # remove the current point from points
            if hit_point in points:
                points.remove(hit_point)
            # if the target points all have been passed, stop searching
            if not points:
                return

            # handle the lazor hitting the block
            block = lazor.hit_block(board)
            if block:
                block.react(lazor, dfs)

        for lazor in self.lazors:
            dfs(lazor)

        # If all points have been passed, the current board is a solution
        return not points

