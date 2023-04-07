import copy
import time 
from PIL import ImageDraw, Image
from sympy.utilities.iterables import multiset_permutations


def bff_convertor(file_name):
    grid_coordinates = []
    raw_grid = []
    temp_grid = []
    num_a_blocks = 0
    num_b_blocks = 0
    num_c_blocks = 0
    lazor_start = []
    end_point_positions = []
    content = []

    # Open and read the file
    with open(file_name, 'r') as f:
        # Get all the lines in the file
        lines = list(f)

        # Remove trailing white spaces from each line
        for i in range(len(lines)):
            lines[i] = lines[i].strip()

            # Convert each line into a list of characters
            content.append(list(lines[i]))

    # Extract useful information
    for i in range(len(content)):
        for j in range(len(content[i])):

            # Set up some temporary lists
            temp_a = []
            temp_b = []
            temp_c = []

            # Get the number of available A-block
            if content[i][j] == 'A' and not str.isalpha(content[i][j + 1]):
                for k in range(len(content[i])):
                    if str.isdigit(content[i][k]):
                        temp_a.append(content[i][k])
                        num_a_blocks = int(''.join(temp_a))
            # Get the number of available B-block
            if content[i][j] == 'B' and not str.isalpha(content[i][j + 1]):
                for k in range(len(content[i])):
                    if str.isdigit(content[i][k]):
                        temp_b.append(content[i][k])
                        num_b_blocks = int(''.join(temp_b))
            # Get the number of available C-block
            if content[i][j] == 'C' and not str.isalpha(content[i][j + 1]):
                for k in range(len(content[i])):
                    if str.isdigit(content[i][k]):
                        temp_c.append(content[i][k])
                        num_c_blocks = int(''.join(temp_c))
            # Get the positions of the start point and direction of lazor
            if content[i][j] == 'L' and not str.isalpha(content[i][j + 1]):
                temp_l = lines[i].strip().split(' ')
                temp_l.remove('L')
                lazor_start.append([int(temp_l[0]), int(temp_l[1]),
                                    int(temp_l[2]), int(temp_l[3])])
            # Get the positions of the end points
            if content[i][j] == 'P' and not str.isalpha(content[i][j - 1]):
                temp_p = lines[i].strip().split(' ')
                temp_p.remove('P')
                end_point_positions.append([int(temp_p[0]), int(temp_p[1])])

        # Get the raw grid from the file
        if lines[i] == 'GRID START':
            grid_start = i + 1
            while lines[grid_start] != 'GRID STOP':
                temp_grid.append(content[grid_start])
                grid_start += 1

    # Remove the spaces of the raw grid
    for i in range(len(temp_grid)):
        grid_line = [x for x in temp_grid[i] if x != ' ']
        grid_coordinates.append(grid_line)
    # Get the original grid which will be used to draw a picture
    for i in range(len(temp_grid)):
        grid_line = [x for x in temp_grid[i] if x != ' ']
        raw_grid.append(grid_line)
    # Fulfill the grid with 'x' to get the full grid
    grid_full = grid_coordinates.copy()
    row = len(grid_full)
    column = len(grid_full[0])
    insert = ['x'] * (2 * column + 1)
    for i in range(0, row):
        for j in range(0, column + 1):
            grid_full[i].insert(2 * j, 'x')
    for i in range(0, row + 1):
        grid_full.insert(2 * i, insert)

    if len(lazor_start) == 0:
        raise Exception('No lazor detected!')
    if (num_a_blocks + num_b_blocks + num_c_blocks) == 0:
        raise Exception('No available blocks related to ABC!')
    if (num_a_blocks + num_b_blocks + num_c_blocks) >= row * column:
        raise Exception('The blocks is more than spaces!')
    # No lasers

    for i, end_point in enumerate(end_point_positions):
        # Check if end point is within the grid boundaries
        if not (0 <= end_point[0] <= column * 2 and 0 <= end_point[1] <= row * 2):
            raise Exception(f'End point {i} is out of bounds!')

    for i, start_point in enumerate(lazor_start):

        # Check if laser start point is within the grid boundaries
        if not (0 <= start_point[0] <= column * 2 and 0 <= start_point[1] <= row * 2):
            raise Exception(f'Start point of laser {i} is out of bounds!')

        # Check if laser direction is valid
        if not (start_point[2] in [-1, 1] and start_point[3] in [-1, 1]):
            raise Exception(f'Direction of laser {i} is invalid!')

        # Check if laser format is correct
        if len(start_point) != 4:
            raise Exception(f'Incorrect format for laser {i}!')

    # Check if there are end points
    if not end_point_positions:
        raise Exception('No end points!')

    # Check if all characters in the grid are valid
    valid_chars = {'x', 'o', 'A', 'B', 'C'}
    for i, row in enumerate(grid_coordinates):
        for j, char in enumerate(row):
            if char not in valid_chars:
                raise Exception(f'Invalid character "{char}" at ({j}, {i}) in the grid!')

    # Return the necessary variables
    return grid_full, num_a_blocks, num_b_blocks, num_c_blocks, lazor_start, end_point_positions, raw_grid


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


def solver(fptr):
    data = bff_convertor(fptr)
    grid = data[0]
    num_cols = data[1]
    num_rows = data[2]
    num_holes = data[3]
    lazors = data[4]
    holes = data[5]
    small_grid = data[6]

    # Find the positions of the occupied spots in the grid
    occupied_spots = find_occupied_spots(small_grid)

    # Solve the puzzle and find the path of the lazors
    solution, lazor_path = path_seek(grid, num_cols, num_rows, num_holes, lazors, holes, occupied_spots)[:2]

    # Create a new grid with the lazors and holes
    new_grid = copy.deepcopy(small_grid)
    lazor_index = 0
    for row in range(len(new_grid)):
        for col in range(len(new_grid[0])):
            if new_grid[row][col] == 'o':
                new_grid[row][col] = lazor_path[lazor_index]
                lazor_index += 1

    # Generate output image
    image_output(solved_board=new_grid, answer_lazor=solution, lazor_info=lazors,
                 holes=holes, filename=fptr)
    output_filename = '.'.join(fptr.split('.')[0:-1])
    print('The puzzle has been solved and saved as {}'.format(
        output_filename + '_solved.png'))
    return new_grid, solution, lazor_path


def solution_color():
    return {
        0: (200, 200, 200),
        'A': (255, 255, 255),
        'B': (50, 50, 50),
        'C': (255, 0, 0),
        'o': (150, 150, 150),
        'x': (100, 100, 100),
    }


def image_output(solved_board, answer_lazor, lazor_info, holes, filename, block_size=50):
    n_blocks_x = len(solved_board[0])
    n_blocks_y = len(solved_board)
    dim_x = n_blocks_x * block_size
    dim_y = n_blocks_y * block_size
    colors = solution_color()

    # Define the set of valid colors
    valid_colors = set(solution_color().keys())

    # Check if all the board values are valid colors
    if not all(set(row).issubset(valid_colors) for row in solved_board):
        raise ValueError("Invalid board value found!")

    img = Image.new("RGB", (dim_x, dim_y), color=(0, 0, 0))

    for jy in range(n_blocks_y):
        for jx in range(n_blocks_x):
            x = jx * block_size  # calculate x-coordinate of block
            y = jy * block_size  # calculate y-coordinate of block

            # loop through each pixel within the block
            for i in range(block_size):
                for j in range(block_size):
                    # determine the color of the pixel based on the value in the solved board
                    color = colors[solved_board[jy][jx]]

                    # set the color of the pixel at (x+i, y+j) in the image
                    img.putpixel((x + i, y + j), color)

    img_new = ImageDraw.Draw(img)

    for i in range(n_blocks_y - 1):
        y = (i + 1) * block_size
        shape = [(0, y), (dim_x, y)]
        img_new.line(shape, fill=colors.get(0, 0), width=5)

    for i in range(n_blocks_x - 1):
        x = (i + 1) * block_size
        shape = [(x, 0), (x, dim_y)]
        img_new.line(shape, fill=colors.get(0, 0), width=5)

    for i in range(len(lazor_info)):
        lazor_pos = (lazor_info[i][0], lazor_info[i][1])
        img_new.ellipse([lazor_pos[0] * block_size / 2 - 10, lazor_pos[1] * block_size / 2 - 10,
                         lazor_pos[0] * block_size / 2 + 10, lazor_pos[1] * block_size / 2 + 10], fill=(255, 0, 0))

    for i in answer_lazor:
        for point in range(len(i)):
            co_start = (i[point][0] * block_size / 2,
                        i[point][1] * block_size / 2)
            if point + 1 < len(i):
                co_end = (i[point + 1][0] * block_size / 2,
                          i[point + 1][1] * block_size / 2)
            else:
                co_end = co_start
            img_new.line([co_start, co_end], fill=(255, 0, 0), width=5)

    for hole in holes:
        x, y = hole[0] * block_size / 2, hole[1] * block_size / 2
        coordinates = (x - 10, y - 10, x + 10, y + 10)
        img_new = ImageDraw.Draw(img)
        img_new.ellipse(coordinates, fill=(255, 255, 255), outline="red", width=2)

    # Name the result image
    if not filename.endswith(".png"):
        filename = '.'.join(filename.split(".")[0:-1])
        filename += "_solved.png"

    img.save("%s" % filename)


if __name__ == "__main__":
    t0 = time.time()
    solver('showstopper_4.bff')
    solver('tiny_5.bff')
    solver('mad_7.bff')
    solver('dark_1.bff')
    solver('mad_1.bff')
    solver('mad_4.bff')
    solver('numbered_6.bff')
    t1 = time.time()
    print(f'Solved in {t1 - t0:.2f} seconds')


