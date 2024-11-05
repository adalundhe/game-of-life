import sys


class Cell:

    def __init__(
        self,
        x: int,
        y: int
    ) -> None:
        self.x = x
        self.y = y
        self.neighbors: list[tuple[int, int]] = []
        self.alive: bool = True

    def __str__(self) -> str:
        return 'O' if self.alive else 'X'

class Grid:

    def __init__(self) -> None:
        self.x_max = 0
        self.x_min = 0
        self.y_max = 0
        self.y_min = 0
        self._grid_width: int = 0
        self._grid_height: int = 0

        self._grid: list[list[Cell]] = []

    def parse_and_add_cell(
        self,
        x: str,
        y: str,
        file_line_number: int,
    ):
        cells: list[Cell] = []
        try:
            cell = Cell(
                int(x),
                int(y)
            )
            
            if cell.x > self.x_max:
                self.x_max = cell.x

            elif cell.x <= self.x_min:
                self.x_min = cell.x
            
            if cell.y > self.y_max:
                self.y_max =cell.y

            elif cell.y <= self.y_min:
                self.y_min = cell.y

            cells.append(cell)

        except TypeError:
            raise Exception(f'Err. - Could not parse coordinate at line - {file_line_number}.')
        
        self._grid_width = abs(self.x_max - self.x_min)
        self._grid_height = abs(self.y_max - self.y_min)

        grid_dimensions = max(self._grid_width, self._grid_height)

        self._grid = [[None] * grid_dimensions] * grid_dimensions

        for cell in cells:
            self._grid[cell.x][cell.y] = str(cell)

    def __str__(self):
        return '\n'.join([
            self._join_grid_line()
        ])
    
    def _join_grid_line(
        self,
        line: list[str]
    ):
        joined_line = '|'.join(line)
        return f'|{joined_line}|'

    @classmethod
    def create_grid(
        cls,
        lines: list[str],
        delimiter: str = ' ',
    ):

        grid = Grid()
        
        for file_line_number, raw_coordinates in enumerate(lines[1:]):
            coordinates = raw_coordinates.split(delimiter)

            if len(coordinates) < 2:
                raise Exception('Err. - Invalid coordinate pair.')
            
            grid.parse_and_add_cell(
                coordinates[0],
                coordinates[1],
                file_line_number,
            )

        return grid

def read_gamefile():
    game_file = sys.stdin.readlines()
    
    if len(game_file) < 1:
        raise Exception('Err. - supplied empty file.')
    
    if not game_file[0].startswith('#'):
        raise Exception('Err. - Invalid Life1.06 format - missing header')
    
    grid = Grid.create_grid(game_file)

    print(grid._grid_width, grid._grid_height)
    

read_gamefile()