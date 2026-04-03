from itertools import product

from fastapi import APIRouter, Path, Query, Request, Response, Depends

from api.products.dao import db_prod
from api.products.schemas import ProductScheme, ProductsQuery
from kafka_config.dependencies import get_kafka_producer
from kafka_config.producer import ProductEventProducer

router = APIRouter(prefix='/products',tags=['Товары'])


@router.get('/', summary='Получить список всех товаров')
async def get_all_products():
    products = await db_prod.get_all_products()
    return {'products': products}

@router.get('/filter')
async def get_products_by_filters(query: ProductsQuery = Query(...)):
    products = await db_prod.get_products_by_filters(**query.model_dump())
    return {'products': products}

@router.get('/{product_id}', summary='Получить конкретный товар')
async def get_product(product_id: int = Path(...)):
    products = await db_prod.get_product_by_id(product_id)
    return {'products': products}

@router.get('/subcategory/{subcat_id}', summary='Получить товары по ID подкатегории')
async def get_products_by_subcategory_id(subcat_id: int = Path(...)):
    products = await db_prod.get_products_by_subcategory_id(subcat_id=subcat_id)
    return {'subcategory_id': subcat_id, 'products': products}

@router.post('/', summary='Добавить товар')
async def add_product(new_prod: ProductScheme,
                      request: Request,
                      producer: ProductEventProducer = Depends(get_kafka_producer)):

    new_product = await db_prod.create_product(**new_prod.model_dump())
    await producer.product_created(product_id=new_product.id, product_name=new_prod.name)
    return {'new_product': new_product}

@router.put('/{product_id}', summary='Изменить товар')
async def edit_product(updated_prod: ProductScheme,
                       product_id: int = Path(...),
                       producer: ProductEventProducer = Depends(get_kafka_producer)):

    updated_product = await db_prod.edit_product(_id=product_id, **updated_prod.model_dump())
    await producer.product_updated(product_id=updated_product.id, product_name=updated_prod.name)
    return {'updated_product': updated_product}

@router.delete('/{product_id}', summary='Удалить товар')
async def delete_product(product_id: int = Path(...),
                         producer: ProductEventProducer = Depends(get_kafka_producer)):

    deleted_product = await db_prod.delete_product(_id=product_id)
    await producer.product_deleted(product_id=product_id)
    return {'Product was deleted': deleted_product}
