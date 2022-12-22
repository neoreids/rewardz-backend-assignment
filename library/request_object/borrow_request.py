from dataclasses import dataclass


@dataclass
class BorrowRequest:
    user_id: int
    books: [int]
