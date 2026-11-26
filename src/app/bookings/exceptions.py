class BookingFileError(Exception):
    """"""


class VinColumnNotFoundError(BookingFileError):
    def __str__(self) -> str:
        return 'Не нашли столбец "VIN"'


class TooManyRowsError(BookingFileError):
    def __init__(self, row_count: int) -> None:
        self.row_count = row_count

    def __str__(self) -> str:
        return f"В файле {self.row_count} строк, можно до 200"


class PastDateError(BookingFileError):
    def __str__(self) -> str:
        return "Нельзя записать на прошедшую дату"
