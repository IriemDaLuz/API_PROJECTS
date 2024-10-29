import datetime

from dataclasses import dataclass
@dataclass
class Review:
    rating: int
    comment: str
    date: datetime
    reviewer_name: str
    reviewer_email: str

