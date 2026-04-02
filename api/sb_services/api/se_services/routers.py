from fastapi import APIRouter, Path, Depends

from api.se_services.dao import db_serv
# from api.se_services.models import SEServices
from api.se_services.schemas import SEServicesScheme
from kafka_config.producer import SEServicesEventProducer
from kafka_config.dependencies import get_kafka_producer

router = APIRouter(prefix='/se_services',tags=['Услуги'])

@router.get('/', summary='Получить список всех услуг')
async def get_all_services():
    services = await db_serv.get_all_services()
    return {'services': services}

@router.get('/{service_id}', summary='Получить конкретную услугу')
async def get_service(service_id: int = Path(...)):
    service = await db_serv.get_service_by_id(service_id)
    return {'service': service}

@router.get('/subcategory/{subcat_id}', summary='Получить услуги по ID подкатегории')
async def get_services_by_subcategory_id(subcat_id: int = Path(...)):
    services = await db_serv.get_services_by_subcategory_id(subcat_id=subcat_id)
    return {'subcategory_id': subcat_id, 'services': services}

@router.post('/', summary='Добавить услугу')
async def add_service(new_service: SEServicesScheme,
                      producer: SEServicesEventProducer = Depends(get_kafka_producer)):
    new_service = await db_serv.create_service(**new_service.model_dump())
    await producer.service_created(service_id=new_service.id)

    return {'new_service': new_service}

@router.put('/{service_id}', summary='Изменить услугу')
async def edit_service(updated_service: SEServicesScheme,
                       service_id: int = Path(...),
                       producer: SEServicesEventProducer = Depends(get_kafka_producer)):
    updated_service = await db_serv.edit_service(_id=service_id, **updated_service.model_dump())
    await producer.service_updated(service_id=updated_service.id)

    return {'updated_service': updated_service}

@router.delete('/{service_id}', summary='Удалить услугу')
async def delete_service(service_id: int = Path(...),
                         producer: SEServicesEventProducer = Depends(get_kafka_producer)):
    deleted_service = await db_serv.delete_service(_id=service_id)
    await producer.service_deleted(service_id=service_id)

    return {'Service was deleted': deleted_service}
