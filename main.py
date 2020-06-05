# -*- coding: UTF-8 -*-
import asyncio
import websockets
import cx_Oracle as cx


def GetTagID(message):
    m_hex = message.hex()
    tag_id_rev = m_hex[16:28]
    i = 5
    tag_id = ''
    while i >= 0:
        tag_id += tag_id_rev[(2*i):(2*i+2)]

        if i != 0:
            tag_id += ':'

        tag_id = tag_id.upper()
        i -= 1
    return tag_id


async def consumer_handler():
    async with websockets.connect('ws://10.44.68.179:6432/ws', ping_interval=None) as websocket:
        async for message in websocket:
            tag_id = GetTagID(message)
            #print(tag_id)
            if tag_id in tag_id_set:
                pass
            else:
                tag_id_set.add(tag_id)
                print('检测到新的ID', tag_id)
                print('共获取到'+str(len(tag_id_set))+"个ID")


if __name__ == '__main__':
    tag_id_set = set()
    asyncio.get_event_loop().run_until_complete(consumer_handler())
