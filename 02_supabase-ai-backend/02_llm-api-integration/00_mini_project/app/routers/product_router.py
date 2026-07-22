from fastapi import APIRouter
from app.schemas.product_schema import ProductPublic
from app.services.product_service import (
    product_create as create_product,
    product_get as get_product,
    product_get_all,
)

product_router = APIRouter()

@product_router.post("/product/create")
def product_create(product: ProductPublic) -> ProductPublic:
    return create_product(product)

@product_router.get("/product/get/{product_id}")
def product_get(product_id: int) -> ProductPublic:
    return get_product(product_id)

@product_router.get("/product/getall")
def product_all() -> list[ProductPublic]:
    return product_get_all()
