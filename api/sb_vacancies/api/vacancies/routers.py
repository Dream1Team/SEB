from fastapi import APIRouter, Path, Query, Depends

from api.vacancies.dao import db_vac
from api.vacancies.schemas import VacancyScheme, VacanciesQuery
from kafka_config.dependencies import get_kafka_producer
from kafka_config.producer import VacancyEventProducer

router = APIRouter(prefix='/vacancies',tags=['Вакансии'])


@router.get('/', summary='Получить список всех вакансии')
async def get_all_vacancies():
    vacancies = await db_vac.get_all_vacancies()
    return {'vacancies': vacancies}

@router.get('/filter')
async def get_vacancies_by_filters(query: VacanciesQuery = Query(...)):
    vacancies = await db_vac.get_vacancies_by_filters(**query.model_dump())
    return {'vacancies': vacancies}

@router.get('/{vacancy_id}', summary='Получить конкретную вакансию')
async def get_vacancy(vacancy_id: int = Path(...)):
    vacancy = await db_vac.get_vacancy_by_id(vacancy_id)
    return {'vacancy': vacancy}

@router.get('/subcategory/{subcategory_id}', summary='Получение вакансий по подкатегории')
async def get_vacancies_by_subcategory(subcategory_id: int = Path(...)):
    vacancies = await db_vac.get_vacancies_by_subcategory_id(subcat_id=subcategory_id)
    return {'subcategory_id': subcategory_id, 'vacancies': vacancies}

@router.post('/', summary='Добавить вакансию')
async def add_vacancy(_new_vacancy: VacancyScheme,
                       producer: VacancyEventProducer = Depends(get_kafka_producer)):
    new_vacancy = await db_vac.create_vacancy(**_new_vacancy.model_dump())
    await producer.vacancy_created(vacancy_id=new_vacancy.id)

    return {'new_vacancy': new_vacancy}

@router.put('/{vacancy_id}', summary='Изменить вакансию')
async def edit_vacancy(_updated_vacancy: VacancyScheme,
                        vacancy_id: int = Path(...),
                       producer: VacancyEventProducer = Depends(get_kafka_producer)):
    updated_vacancy = await db_vac.edit_vacancy(_id=vacancy_id, **_updated_vacancy.model_dump())
    await producer.vacancy_updated(vacancy_id=updated_vacancy.id)

    return {'updated_vacancy': updated_vacancy}

@router.delete('/{vacancy_id}', summary='Удалить вакансию')
async def delete_vacancy(vacancy_id: int = Path(...),
                       producer: VacancyEventProducer = Depends(get_kafka_producer)):
    deleted_vacancy = await db_vac.delete_vacancy(_id=vacancy_id)
    await producer.vacancy_deleted(vacancy_id=vacancy_id)

    return {'Vacancy was deleted': deleted_vacancy}
