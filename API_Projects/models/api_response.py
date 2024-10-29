from typing import List
from dataclasses import dataclass
from models.product import Product


@dataclass
class APIResponse:
    products: List[Product]
    total: int
    skip: int
    limit: int


