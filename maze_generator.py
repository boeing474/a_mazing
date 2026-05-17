class MazeGenerator:
    def __init__(self):
        pass
        
    def generate_grid(self, qnt_cells):
        self.cells = []
        for cell in range(qnt_cells):
            self.cells.append(Cell())

        for cell in range(len(self.cells)):
            self.cells[cell].show_cell()


class Cell:
    def __init__(self):
        self.visited = False
        self.north = 0
        self.east = 0
        self.south = 0
        self.west = 0

    def show_cell(self):
        print(f"{self.north}{self.east}{self.south}{self.west}", end="")
