from enum import Enum
from pydantic import BaseModel

class TypeItem(Enum):
    ELECTRONICS = "Электроника"
    CLOTHES = "Одежда"
    BOOKS = "Книги"

class Product(BaseModel):
    name: str
    price: float
    type_product: list[TypeItem]
    in_stock: bool

product = Product(name="MacBook", price=81499.99, type_product=[TypeItem.ELECTRONICS] ,in_stock=True)
json_data = product.model_dump_json()
print(json_data)
new_data = Product.model_validate_json(json_data)
print(new_data)