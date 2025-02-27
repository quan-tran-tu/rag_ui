from pydantic import BaseModel

class Product(BaseModel):
    id: str
    name: str
    image: str
    price: str
    merchantDomain: str
    merchantLogoPath: str
    provins: str
    isOutOfStock: bool
    directUrl: str
