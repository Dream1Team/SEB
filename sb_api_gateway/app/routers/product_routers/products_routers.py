from fastapi import APIRouter, Request, Path, Depends, Body
from fastapi.params import Query
from starlette.responses import JSONResponse

from app.schemes.products_schemes import ProductScheme, ProductsQuery
from app.services.product_service import product_service
# from dependencies import get_current_admin

router = APIRouter(prefix="/products", tags=["Products"])


# Products
@router.get("/products")
async def get_products(request: Request):
    """Получение товаров"""
    result = await product_service.get_products(request)
    # result.update(request.headers.get("Cookie"))
    return JSONResponse(content=result)


@router.get("/products/filter")
async def get_products_by_filter(request: Request,
                                 params: ProductsQuery = Query(...)):
    """Получение товаров по фильтру"""
    result = await product_service.get_products_by_filter(request=request,
                                                          params=params.model_dump())

    return JSONResponse(content=result)


@router.get("/products/subcategory/{subcat_id}")
async def get_products_by_subcategory_id(request: Request,
                                         subcat_id: int = Path(...)):
    """Получение товаров по ID подкатегории"""
    result = await product_service.get_products_by_subcategory_id(request, subcat_id)

    return JSONResponse(content=result)


@router.get("/products/{product_id}")
async def get_product_by_id(request: Request,
                            product_id: int = Path(...)):
    """Получение товара по ID"""
    result = await product_service.get_product_by_id(request, product_id)
    return JSONResponse(result)


@router.post("/products")
async def create_product(request: Request,
                         product_data: ProductScheme = Body(...)):
    """Добавление товаров"""
    result = await product_service.create_product(request, product_data=product_data.model_dump(by_alias=True))

    return JSONResponse(content=result)

@router.put("/products/{product_id}")
async def update_product(request: Request,
                          product_data: ProductScheme = Body(...),
                          product_id: int = Path(...)):
    result = await product_service.update_product(request,
                                                  product_id=product_id,
                                                  product_data=product_data.model_dump(by_alias=True))
    return JSONResponse(content=result)

@router.delete("/products/{product_id}")
async def delete_product(request: Request,
                         product_id: int = Path(...)):
    result = await product_service.delete_product(request, product_id)

    return JSONResponse(content=result)


@router.get("/health")
async def health(request: Request):
    pass