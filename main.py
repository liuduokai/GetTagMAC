# -*- coding: UTF-8 -*-
import asyncio
import websockets
import con_oracle
import logging



# 获取打印版本的MAC地址
def get_print_version_mac(message):
    m_hex = message.hex()
    tag_id_p_rev = m_hex[16:28]
    i = 5
    tag_id_p = ''
    while i >= 0:
        tag_id_p += tag_id_p_rev[(2 * i):(2 * i + 2)]

        if i != 0:
            tag_id_p += ':'

        tag_id_p = tag_id_p.upper()
        i -= 1
    return tag_id_p


# 获取MAC转化为数字的结果
def get_tag_mac(message):
    m_hex = message.hex()
    tag_id_rev = m_hex[16:28]
    i = 5
    tag_id = ''
    while i >= 0:
        tag_id += tag_id_rev[(2 * i):(2 * i + 2)]
        i -= 1
    return int(tag_id, 16)


async def consumer_handler():
    async with websockets.connect('ws://10.44.68.179:6432/ws', ping_interval=None) as websocket:
        async for message in websocket:
            # 获取打印格式MAC
            try:
                tag_mac_p = get_print_version_mac(message)
            except OSError as err:
                logging.error("获取格式化MAC出错")
                logging.error(message)
                logging.error(tag_mac_p)

            # 获取数字版本MAC
            try:
                tag_mac = get_tag_mac(message)
            except OSError as err:
                logging.error("获取mac id出现错误")
                logging.error(err)
                logging.error(message)
                logging.error(tag_mac)

            # 是否是新检测到的标签
            if tag_mac in tag_mac_set:
                pass
            else:
                tag_mac_set.add(tag_mac)
                print('********检测到新的标签********')
                print('tag MAC:', tag_mac_p)

                # 查询MAC对应的TAG ID
                try:
                    tag_id = con_oracle.get_tag_id(tag_mac)
                except OSError as err:
                    logging.error("获取tag id出现错误")
                    logging.error(err)
                    logging.error(message)
                    logging.error(tag_mac)
                    logging.error(tag_id)
                # print(mac_id)
                print('tag_id:', tag_id)
                print('共检测到' + str(len(tag_mac_set)) + "个标签")
                print('---------------------------')


if __name__ == '__main__':
    logging.basicConfig(filename='logger.log', level=logging.INFO)
    tag_mac_set = set()
    asyncio.get_event_loop().run_until_complete(consumer_handler())
