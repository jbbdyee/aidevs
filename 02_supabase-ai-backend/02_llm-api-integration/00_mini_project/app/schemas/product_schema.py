from pydantic import BaseModel, Field



class ProductPublic(BaseModel):
    id: int
    name: str   
    price: int
