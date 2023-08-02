import request
import config
from time import time
import threading
import logging
from people import People


def log_config():
    # 配置日志格式
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # 创建一个文件处理器，将日志输出到名为 app.log 的文件中
    file_handler = logging.FileHandler('app.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # 创建一个终端处理器，将日志输出到终端
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # 定义日志格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 获取根日志记录器，并添加处理器
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


def print_ticket():
    # 获取票价信息，默认从最低价开始
    logging.info(f"seat_plans(now):{request.get_seat_plans(show_id, session_id)}")
    # 获取座位余票信息，默认从最低价开始
    logging.info(f"seat_count(now):{request.get_seat_count(show_id, session_id)}")


def get_common_info():
    # 获取场次的item
    sessions_item = request.get_sessions(show_id)[session]
    session_id_info = sessions_item["bizShowSessionId"]
    session_status = sessions_item["sessionStatus"]
    logging.info(f"session_id:{session_id_info} session_status:{session_status} session_sale_time:{session_sale_time}")
    # 获取票价信息，默认从最低价开始
    seat_plans = request.get_seat_plans(show_id, session_id_info)
    logging.info(f"seat_plans:{seat_plans}")
    # 获取座位余票信息，默认从最低价开始
    seat_count = request.get_seat_count(show_id, session_id_info)
    logging.info(f"seat_count:{seat_count}")
    seat_plan_id_info = seat_plans[ticket_price]["seatPlanId"]
    price_info = seat_plans[ticket_price]["originalPrice"]
    logging.info(f"seat_plan_id:{seat_plan_id_info} price:{price_info}")
    return session_id_info, seat_plan_id_info, price_info


def get_info(token) -> People:
    # 获取观演人信息
    audiences = request.get_audiences(token)
    audience_ids = [audiences[i]["id"] for i in audience_idx]
    logging.info(f"audience_ids:{audience_ids}")
    # deliver_method = request.get_deliver_method(token, show_id, session_id, seat_plan_id, price, buy_count)
    logging.info(f"deliver_method:{deliver_method}")
    # 获取默认收货地址
    address = request.get_address(token)
    logging.info(f"address:{address}")
    address_id = address["addressId"]  # 地址id
    location_city_id = address["locationId"]  # 460102
    receiver = address["username"]  # 收件人
    cellphone = address["cellphone"]  # 电话
    detail_address = address["detailAddress"]  # 详细地址
    # 获取快递费用
    express_fee = request.get_express_fee(token, show_id, session_id, seat_plan_id, price, buy_count, location_city_id)
    logging.info(f"express_fee:{express_fee}")
    return People(token, audience_ids, address_id, location_city_id, receiver, cellphone, detail_address,
                  express_fee)


def create_order(people: People):
    logging.info(f"{threading.current_thread().name}开始下订单")
    if deliver_method == "EXPRESS":
        request.create_order(people.token, show_id, session_id, seat_plan_id, price, buy_count,
                             deliver_method, people.express_fee["priceItemVal"], people.receiver,
                             people.cellphone, people.address_id, people.detail_address, people.location_city_id,
                             people.audience_ids)
    elif deliver_method == "VENUE_E":
        request.create_order(people.token, show_id, session_id, seat_plan_id, price, buy_count,
                             deliver_method, 0, None, None, None, None, None, [])
    elif deliver_method == "VENUE" or deliver_method == "E_TICKET":
        request.create_order(people.token, show_id, session_id, seat_plan_id, price, buy_count,
                             deliver_method, 0, None, None, None, None, None, people.audience_ids)
    else:
        logging.info(f"不支持的deliver_method:{deliver_method}")


tokens = config.tokens
show_id = config.show_id
buy_count = config.buy_count
ticket_price = config.ticket_price
session = config.session
audience_idx = config.audience_idx
deliver_method = config.deliver_method
session_sale_time = config.session_sale_time
session_id = ''
seat_plan_id = ''
price = 0
try:
    log_config()
    peoples_info = []
    logging.info('init program')
    session_id, seat_plan_id, price = get_common_info()
    for item in tokens:
        peoples_info.append(get_info(item))
    while True:
        # 获取当前时间的时间戳
        current_time = int(time() * 1000)
        # 当前时间大于等于开售时间
        if current_time < session_sale_time:
            continue
        logging.info(f"循环条件跳出 current_time:{current_time}")
        # 打印票信息，启动线程
        threading.Thread(target=print_ticket).start()
        break
    threads = []
    for people_info in peoples_info:
        # 多线程下单
        thread = threading.Thread(target=create_order, args=(people_info, ))
        thread.start()
        threads.append(thread)
        # create_order(people_info)

    # 等待所有子线程结束
    for thread in threads:
        thread.join()
    logging.info(f"finish program")
except Exception as e:
    logging.info(f"program exception:{e}")
