from tkinter import Tk, BOTH, Canvas
import time
import random

class Window():
  def __init__(self, width, height):
    self.root= Tk()
    self.root.title("Maze Solver")
    self.root.protocol("WM_DELETE_WINDOW", self.close)
    self.canvas = Canvas(self.root, bg="white", width=width, height=height)
    self.canvas.pack(fill=BOTH, expand=1)
    self.running = False

  def redraw(self):
    self.root.update_idletasks()
    self.root.update()

  def wait_for_close(self):
    self.running = True
    while self.running:
      self.redraw()
    print("window closed...")

  def draw_line(self, line, fill_color="black"):
    line.draw(self.canvas, fill_color)

  def close(self):
    self.running = False



  

class Point():
  def __init__(self, x, y):
    self.x = x
    self.y = y  



class Line():
  def __init__(self, point1, point2):
    self.point1 = point1
    self.point2 = point2

  def draw(self, canvas, fill_color):
    canvas.create_line(
      self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2
    )




class Cell():
  def __init__(self, win=None):
    self.has_left_wall = True
    self.has_right_wall = True
    self.has_top_wall = True
    self.has_bottom_wall = True
    self.x1 = None
    self.x2 = None
    self.y1 = None
    self.y2 = None
    self.win = win
    self.visited = False

  def draw(self, x1, y1, x2, y2):
    if self.win is None:
      return
    self.x1 = x1
    self.x2 = x2
    self.y1 = y1
    self.y2 = y2
    if self.has_left_wall:
      self.win.draw_line(Line(Point(x1, y1), Point(x1, y2)))
    else:
      self.win.draw_line(Line(Point(x1, y1), Point(x1, y2)), "white")
    if self.has_top_wall:
      self.win.draw_line(Line(Point(x1, y1), Point(x2, y1)))
    else:
      self.win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "white")
    if self.has_right_wall:
      self.win.draw_line(Line(Point(x2, y1), Point(x2, y2)))
    else:
      self.win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "white")
    if self.has_bottom_wall:
      self.win.draw_line(Line(Point(x1, y2), Point(x2, y2)))
    else:
      self.win.draw_line(Line(Point(x1, y2), Point(x2, y2)), "white")
  
  def draw_move(self, to_cell, undo=False):
    xcenter = (self.x1 + self.x2) // 2
    ycenter = (self.y1 + self.y2) // 2
    centerpoint = Point(xcenter, ycenter)

    xcenter2 = (to_cell.x1 + to_cell.x2) // 2
    ycenter2 = (to_cell.y1 + to_cell.y2) // 2
    centerpoint2 = Point(xcenter2, ycenter2)

    fill_color = "red"
    if undo:
      fill_color = "grey"
    
    self.win.draw_line(Line(centerpoint, centerpoint2), fill_color=fill_color)
    




class Maze():
  def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
    self._cells = []
    self._x1 = x1
    self._y1 = y1
    self._num_rows = num_rows
    self._num_cols = num_cols
    self._cell_size_x = cell_size_x
    self._cell_size_y = cell_size_y
    self._win = win
    if seed:
      random.seed(seed)
    self._create_cells()
    self._break_entrance_and_exit()
    self._break_walls_r(0, 0)
    self._reset_cells_visited()

  def _create_cells(self):
    for i in range(self._num_cols):
      col_cells = []
      for j in range(self._num_rows):
        col_cells.append(Cell(self._win))
      self._cells.append(col_cells)
    for i in range(self._num_cols):
      for j in range(self._num_rows):
        self._draw_cell(i, j)
  
  def _draw_cell(self, i, j):
    if self._win is None:
      return
    x1 = self._x1 + i * self._cell_size_x
    y1 = self._y1 + j * self._cell_size_y
    x2 = x1 + self._cell_size_x
    y2 = y1 + self._cell_size_y
    self._cells[i][j].draw(x1, y1, x2, y2)
    self._animate()
    
  def _animate(self):
    if self._win is None:
        return
    self._win.redraw()
    time.sleep(0.01)

  def _break_entrance_and_exit(self):
    self._cells[0][0].has_top_wall = False
    self._draw_cell(0,0)
    self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
    self._draw_cell(self._num_cols - 1, self._num_rows - 1)

  def _break_walls_r(self, i, j):
    self._cells[i][j].visited = True
    while True:
      next_index_list = []

      # determine which cell(s) to visit next
      # left
      if i > 0 and not self._cells[i - 1][j].visited:
        next_index_list.append((i - 1, j))
      # right
      if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
        next_index_list.append((i + 1, j))
      # up
      if j > 0 and not self._cells[i][j - 1].visited:
        next_index_list.append((i, j - 1))
      # down
      if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
        next_index_list.append((i, j + 1))

      # if there is nowhere to go from here
      # just break out
      if len(next_index_list) == 0:
        self._draw_cell(i, j)
        return

      # randomly choose the next direction to go
      direction_index = random.randrange(len(next_index_list))
      next_index = next_index_list[direction_index]

      # knock out walls between this cell and the next cell(s)
      # right
      if next_index[0] == i + 1:
        self._cells[i][j].has_right_wall = False
        self._cells[i + 1][j].has_left_wall = False
      # left
      if next_index[0] == i - 1:
        self._cells[i][j].has_left_wall = False
        self._cells[i - 1][j].has_right_wall = False
      # down
      if next_index[1] == j + 1:
        self._cells[i][j].has_bottom_wall = False
        self._cells[i][j + 1].has_top_wall = False
      # up
      if next_index[1] == j - 1:
        self._cells[i][j].has_top_wall = False
        self._cells[i][j - 1].has_bottom_wall = False

      # recursively visit the next cell
      self._break_walls_r(next_index[0], next_index[1])
  
  def _reset_cells_visited(self):
    for i in range(self._num_cols):
      for j in range(self._num_rows):
        self._cells[i][j].visited = False

  def solve(self):
    self._solve_r(0, 0)

  def _solve_r(self, i, j):
    self._animate()
    self._cells[i][j].visited = True
    if i == self._num_cols - 1 and j == self._num_rows - 1:
      return True
    # move left
    if i > 0 and not self._cells[i][j].has_left_wall and not self._cells[i - 1][j].visited:
      self._cells[i][j].draw_move(self._cells[i - 1][j])
      if self._solve_r(i - 1, j):
        return True
      else:
        self._cells[i][j].draw_move(self._cells[i - 1][j], True)
    # move right
    if i < self._num_cols - 1 and not self._cells[i][j].has_right_wall and not self._cells[i + 1][j].visited:
      self._cells[i][j].draw_move(self._cells[i + 1][j])
      if self._solve_r(i + 1, j):
        return True
      else:
        self._cells[i][j].draw_move(self._cells[i + 1][j], True)
    # move up
    if j > 0 and not self._cells[i][j].has_top_wall and not self._cells[i][j - 1].visited:
      self._cells[i][j].draw_move(self._cells[i][j - 1])
      if self._solve_r(i, j - 1):
        return True
      else:
        self._cells[i][j].draw_move(self._cells[i][j - 1], True)
    # move down
    if j < self._num_rows and not self._cells[i][j].has_bottom_wall and not self._cells[i][j + 1].visited:
      self._cells[i][j].draw_move(self._cells[i][j + 1])
      if self._solve_r(i, j + 1):
        return True
      else:
        self._cells[i][j].draw_move(self._cells[i][j + 1], True)
    
    return False

def main():
  num_rows = 12
  num_cols = 16
  margin = 50
  screen_x = 800
  screen_y = 600
  cell_size_x = (screen_x - 2 * margin) / num_cols
  cell_size_y = (screen_y - 2 * margin) / num_rows
  win = Window(screen_x, screen_y)

  maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, 10)
  maze.solve()
  win.wait_for_close()

main()