"""2-D array representation of seats inside a zone."""

from typing import List, Optional, Tuple


class SeatGrid:
    """Row-major 2-D seat array with O(1) indexed access."""

    def __init__(self, zone_id: str, rows: int, cols: int) -> None:
        self.zone_id = zone_id
        self.rows = rows
        self.cols = cols
        self._cells: List[List[Optional[str]]] = [[None for _ in range(cols)] for _ in range(rows)]

    def seat_code(self, row: int, col: int) -> str:
        return f"{self.zone_id}-R{row:02d}-C{col:02d}"

    @staticmethod
    def parse_code(code: str) -> Tuple[str, int, int]:
        zone, rpart, cpart = code.split("-")
        return zone, int(rpart[1:]), int(cpart[1:])

    def is_free(self, row: int, col: int) -> bool:
        return self._cells[row][col] is None

    def get(self, row: int, col: int) -> Optional[str]:
        return self._cells[row][col]

    def assign(self, row: int, col: int, user_id: str) -> bool:
        if self._cells[row][col] is not None:
            return False
        self._cells[row][col] = user_id
        return True

    def release(self, row: int, col: int) -> None:
        self._cells[row][col] = None

    def free_count(self) -> int:
        return sum(1 for row in self._cells for cell in row if cell is None)

    def occupied_count(self) -> int:
        return self.rows * self.cols - self.free_count()

    def all_seats(self):
        for r in range(self.rows):
            for c in range(self.cols):
                yield r, c, self._cells[r][c]

    def seats_for_user(self, user_id: str) -> List[str]:
        return [self.seat_code(r, c) for r, c, holder in self.all_seats() if holder == user_id]
