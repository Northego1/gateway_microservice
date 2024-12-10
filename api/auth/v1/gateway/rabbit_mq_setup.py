import asyncio
import importlib
import pkgutil

from exceptions.server_exceptions import RabbitMqError, ServerError
from rabbit_mq_manager.connection_manager import connection_manager
from logger import service_logger as serv_log
from aio_pika import ExchangeType
from config import settings
from rabbit_mq_manager import pool



def load_consumers(package_name: str) -> None:
    '''
    Импортирует все модули внутри указанного пакета.
    Это выполняет декораторы внутри импортируемых модулей.
    
    :param package_name: Имя пакета, содержащего модули с маршрутами.
    '''
    try:
        serv_log.info('Trying to load tasks route endpoints')
        package = importlib.import_module(package_name)
        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            importlib.import_module(f"{package_name}.{module_name}")
            serv_log.info(f'Loaded module {module_name!r}')
    except Exception as e:
        serv_log.error(f"Failed to load routes from package {package_name}")
        raise ServerError() from e
    serv_log.info(f'Successfully loaded tasks modules')


async def shutdown():
    """
    Корректное завершение приложения:
    закрытие каналов и соединения с RabbitMQ.
    """
    serv_log.warning('Shutting down microservice...')
    try:
        await pool.producer_channel_pool.close_all_channels()
        await pool.consumer_channel_pool.close_all_channels()
        await connection_manager.close()
        serv_log.warning('Microservice stopped.')
    except Exception as e:
        serv_log.error(f"Error during shutdown: {e}")


async def rabbit_mq_setup():
    '''
    Устанавливает соединение с RabbitMQ,
    инициализирует всех консьюмеров,
    подгружает декораторы эндпоинтов
    и запускает бесконечный цикл.
    '''
    serv_log.info('Starting microservice...')
    try:
        await connection_manager.connect()
        await pool.producer_channel_pool.add('base_channel')
        await pool.exchange_pool.add(
            name='DIRECT',
            type=ExchangeType.DIRECT,
            durable=True,
        )
        
        # await pool.consumer_channel_pool.add('base_channel')
        #Инициализация и запуск консьюмеров в ивент луп
        # await ExchangeStartPool.init()
        # await QueueStartPool.init()
        # load_consumers('api.auth.v1.receivers')

    except Exception as e:
        serv_log.error(f"Error in main loop: {e}")
        await shutdown()
        raise


