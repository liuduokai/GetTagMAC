import websockets
import asyncio
import logging


async def consumer_handler():
    async with websockets.connect('ws://10.44.68.179:6432/ws', ping_interval=None) as websocket:
        async for message in websocket:
            print(message)

if __name__ == '__main__':


    logging.basicConfig(filename='logger.log', level=logging.INFO)
    logging.debug('debug message')
    logging.info('info message')
    logging.warn('warn message')
    logging.error('error message')
    logging.critical('critical message')
    logger = logging.getLogger('websockets')
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())


    try:
        asyncio.get_event_loop().run_until_complete(consumer_handler())
    except OSError as err:
        print("连接中断", err)
        asyncio.get_event_loop().run_until_complete(consumer_handler())