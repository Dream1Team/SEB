from fastapi import APIRouter, Path, Depends

from api.subcategories.dao import db_subcat
from api.subcategories.schemas import SubcategoryScheme
from kafka_config.dependencies import get_kafka_producer
from kafka_config.producer import VacancyEventProducer

router = APIRouter(prefix='/subcategories', tags=['Подкатегории'])

@router.get('/', summary='Получить список всех подкатегорий услуг')
async def get_all_subcategories():
    subcategories = await db_subcat.get_all_subcategories()
    return {'subcategories': subcategories}

@router.get('/{subcat_id}', summary='Получить определенную подкатегорию')
async def get_subcategory(subcat_id: int = Path(...)):
    subcategory = await db_subcat.get_subcategory_by_id(subcat_id)
    return {'subcategory': subcategory}

@router.get('/category/{cat_id}', summary='Получить подкатегорию по ID категории')
async def get_subcategory_by_category_id(cat_id: int = Path(...)):
    subcategories = await db_subcat.get_subcategories_by_category(cat_id=cat_id)
    return {'category_id': cat_id, 'subcategories': subcategories}

@router.post('/', summary='Добавить подкатегорию')
async def add_subcategory(new_subcat: SubcategoryScheme,
                       producer: VacancyEventProducer = Depends(get_kafka_producer)):
    new_subcategory = await db_subcat.create_subcategory(**new_subcat.model_dump())
    # await producer.vacancy_subcategory_created(subcategory_id=new_subcategory.id)

    return {'new_subcategory': new_subcategory}

@router.put('/{subcat_id}', summary='Изменить подкатегорию')
async def edit_subcategory(updated_subcat: SubcategoryScheme,
                        subcat_id: int = Path(...),
                       producer: VacancyEventProducer = Depends(get_kafka_producer)):
    updated_subcategory = await db_subcat.edit_subcategory(_id=subcat_id, **updated_subcat.model_dump())
    await producer.vacancy_subcategory_updated(subcategory_id=updated_subcategory.id)

    return {'updated_subcategory': updated_subcategory}

@router.delete('/{subcat_id}', summary='Удалить подкатегорию')
async def delete_subcategory(subcat_id: int = Path(...),
                       producer: VacancyEventProducer = Depends(get_kafka_producer)):
    deleted_subcategory = await db_subcat.delete_subcategory(_id=subcat_id)
    await producer.vacancy_subcategory_deleted(subcategory_id=subcat_id)

    return {'Subcategory was deleted': deleted_subcategory}
