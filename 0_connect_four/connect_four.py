from enum import Enum
from typing import List, Tuple


class GridPosition(Enum):
  Empty = 0
  Red = 1
  Blue = 2


class Grid:

  def __init__(self, n_rows: int, n_cols: int) -> None:
    self._n_rows = n_rows
    self._n_cols = n_cols
    self.init_grid()

  def init_grid(self) -> None:
    self._grid = [[GridPosition.Empty for _ in range(self._n_cols)]
                  for _ in range(self._n_rows)]

  @property
  def grid(self) -> List[List[GridPosition]]:
    return self._grid

  @property
  def n_cols(self) -> int:
    return self._n_cols

  def place_piece(self, col: int, color: GridPosition) -> int:
    if col < 0 or col >= self._n_cols:
      raise ValueError("Invalid column!")
    if color == GridPosition.Empty:
      raise ValueError("Invalid piece color!")
    for row_idx in range(self._n_rows - 1, -1, -1):
      if self._grid[row_idx][col] == GridPosition.Empty:
        self._grid[row_idx][col] = color
        return row_idx
    print("Column is full, try another column!")
    return -1

  def print_board(self) -> None:
    print("Board:")
    for row_idx in range(self._n_rows):
      this_row = []
      for col_idx in range(self._n_cols):
        if self._grid[row_idx][col_idx] == GridPosition.Empty:
          this_row.append('0')
        elif self._grid[row_idx][col_idx] == GridPosition.Red:
          this_row.append('R')
        elif self._grid[row_idx][col_idx] == GridPosition.Blue:
          this_row.append('B')
        else:
          raise Error("invalid value for grid[{}][{}]".format(
              row_idx, col_idx))
      print(' '.join(this_row))

  def is_connected(self, color: GridPosition, n: int, row_idx: int,
                   col_idx: int) -> bool:
    # connected by same column
    if self._n_rows - row_idx >= n:
      row_connected = True
      for i in range(row_idx + 1, row_idx + n):
        if self._grid[i][col_idx] != color:
          row_connected = False
          break
      if row_connected:
        return True

    # check by same row
    count = 0
    for j in range(self._n_cols):
      if self._grid[row_idx][j] == color:
        count += 1
      else:
        count = 0
      if count == n:
        return True

    # check by positive diagonal
    count = 0
    for r in range(self._n_rows):
      c = row_idx + col_idx - r
      if c >= 0 and c < self._n_cols and self._grid[r][c] == color:
        count += 1
      else:
        count = 0
      if count == n:
        return True

    # check by negative diagonal
    count = 0
    for r in range(self._n_rows):
      c = -row_idx + col_idx + r
      if c >= 0 and c < self._n_cols and self._grid[r][c] == color:
        count += 1
      else:
        count = 0
      if count == n:
        return True

    return False


class Player:

  def __init__(self, name: str, color: GridPosition) -> None:
    self._name = name
    self._color = color

  @property
  def color(self) -> GridPosition:
    return self._color

  @property
  def name(self) -> str:
    return self._name


class Game:

  def __init__(self, board_rows: int, board_cols: int, target_score: int,
               connect_to_win: int) -> None:
    self._grid = Grid(board_rows, board_cols)
    self._max_moves = board_rows * board_cols
    self._players = []
    self._players.append(Player("Player 1", GridPosition.Red))
    self._players.append(Player("Player 2", GridPosition.Blue))
    self._target_score = target_score
    self._connect_to_win = connect_to_win
    self._score = {}
    for player in self._players:
      self._score[player.name] = 0

  def play_move(self, player: Player) -> Tuple[int, int]:
    while True:
      self._grid.print_board()
      col_idx = int(
          input("Enter column idx from 0 to {} to add your piece".format(
              self._grid.n_cols)))
      row_idx = self._grid.place_piece(col_idx, player.color)
      if row_idx != -1:
        break
    return (row_idx, col_idx)

  def play_one_match(self) -> Player:
    for _ in range(self._max_moves):
      for player in self._players:
        row_idx, col_idx = self.play_move(player)
        if self._grid.is_connected(player.color, self._connect_to_win, row_idx,
                                   col_idx):
          self._score[player.name] += 1
          is_game_finished = True
          return player

  def play_game(self) -> None:
    max_score = 0
    winner = None
    while max_score < self._target_score:
      round_winner = self.play_one_match()
      print('round winner: {}'.format(round_winner.name))
      max_score = max(max_score, self._score[round_winner.name])
      self._grid.init_grid()
    print('Final winner: {}'.format(round_winner.name))


game = Game(6, 7, 2, 4)
game.play_game()
