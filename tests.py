import unittest

from ogmain import Maze

class Tests(unittest.TestCase):
  def test_maze_create_cells(self):
    num_cols = 12
    num_rows = 10
    m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
    self.assertEqual(
      len(m1._cells),
      num_cols,
    )
    self.assertEqual(
      len(m1._cells[0]),
      num_rows,
    )

  def test_maze_create_cells_large(self):
    num_cols = 20
    num_rows = 16
    m1 = Maze(20, 20, num_rows, num_cols, 5, 5)
    self.assertEqual(
      len(m1._cells),
      num_cols
    )
    self.assertEqual(
      len(m1._cells[0]),
      num_rows
    )

  def test_maze_break_entrance_and_exit(self):
    num_cols = 8
    num_rows = 8
    m1 = Maze(4, 1, num_rows, num_cols, 1, 1)
    self.assertEqual(
      m1._cells[0][0].has_top_wall,
      False
    )
    self.assertEqual(
      m1._cells[num_cols - 1][num_rows - 1].has_bottom_wall,
      False
    )

  def test_maze_reset_cells_visited(self):
    num_cols = 4
    num_rows = 14
    m1 = Maze(3, 2, num_rows, num_cols, 2, 1)
    for i in range(num_cols):
      for j in range(num_rows):
        self.assertEqual(
          m1._cells[i][j].visited,
          False
        )

if __name__ == "__main__":
  unittest.main()
