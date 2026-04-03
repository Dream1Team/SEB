from fastapi import APIRouter, Path, Depends

from api.categories.dao import db_cat
from api.categories.schemas import CategoryScheme
from kafka_config.dependencies import get_kafka_producer
from kafka_config.producer import ProductEventProducer

router = APIRouter(prefix='/categories', tags=['Категории'])


@router.get('/', summary='Получить список всех категорий услуг')
async def get_all_categories():
    categories = await db_cat.get_all_categories()
    return {'categories': categories}

@router.get('/{cat_id}', summary='Получить определенную категорию')
async def get_category(cat_id: int = Path(...)):
    category = await db_cat.get_category_by_id(cat_id)
    return {'category': category}

@router.post('/', summary='Добавить категорию')
async def add_category(new_cat: CategoryScheme,
                       producer: ProductEventProducer = Depends(get_kafka_producer)):
    new_category = await db_cat.create_category(**new_cat.model_dump())
    await producer.product_category_created(cat_name=new_cat.name, cat_id=new_category.id)

    return {'new_category': new_category}

@router.put('/{cat_id}', summary='Изменить категорию')
async def edit_category(updated_cat: CategoryScheme,
                        cat_id: int = Path(...),
                        producer: ProductEventProducer = Depends(get_kafka_producer)):
    updated_category = await db_cat.edit_category(_id=cat_id, **updated_cat.model_dump())
    await producer.product_category_updated(cat_name=updated_cat.name, cat_id=updated_category.id)

    return {'updated_category': updated_category}

@router.delete('/{cat_id}', summary='Удалить категорию')
async def delete_category(cat_id: int = Path(...),
                         producer: ProductEventProducer = Depends(get_kafka_producer)):
    deleted_category = await db_cat.delete_category(_id=cat_id)
    await producer.product_category_deleted(cat_id=cat_id)

    return {'Category was deleted': deleted_category}
